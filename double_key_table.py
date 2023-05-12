from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        
        #Creating the underlying array 
        if sizes is not None: 
            self.TABLE_SIZES = sizes
        else: 
            self.TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]
        
        #checking internal sizes 
        if internal_sizes is not None:
            self.internal_TABLE_SIZES = internal_sizes
        else:
            self.internal_TABLE_SIZES = self.TABLE_SIZES

        #Initialising the empty hash table 
        self.table = [None] * self.TABLE_SIZES[0]
        self.internal_tables = [[None] * size for size in self.internal_TABLE_SIZES]

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value
    def _resize_if_needed(self, index1:int):
        #check the load factor of the table
        num_entries = sum(1 for _ in self.iter_keys())
        if num_entries / len(self.table) > 0.5:
            self._resize_table()

        #check the load factor of the specific internal table
        sub_table = self.table[index1]
        if sub_table and len(sub_table.table) / len(sub_table.table_size) > 0.5:
            self._resize_internal_table(index1)
    
    def _resize_table(self):
        #Double the size of the top-level table
        self.table = self.table + [None] * len(self.table)
    
    def _resize_internal_table(self, index1:int):
        #Double the size of the specific internal table
        sub_table = self.table[index1]
        sub_table.table = sub_table.table + [None] * len(sub_table.table)
        sub_table.table_size *= 2


    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        # Calculate the hash values
        index1 = self.hash1(key1)
        index2 = self.hash2(key2)

    # Create the internal table if it doesn't exist
        if self.table[index1] is None:
            if is_insert:
                self.table[index1] = LinearProbeTable()
            else:
                raise KeyError(f"Key1: {key1} is not in the table.")

    # Find the index in the internal table
        internal_table = self.table[index1]
        while internal_table[index2] is not None and internal_table[index2][0] != key2:
            index2 = (index2 + 1) % len(internal_table)

    # Check if the key2 is not in the table
        if internal_table[index2] is None and not is_insert:
            raise KeyError(f"Key2: {key2} is not in the table.")

    # If we are inserting, check if the tables need to be resized
        if is_insert:
            self._resize_if_needed()

        return index1, index2

    
    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None: 
            #Yield all the top-level keys
            for k1 in self.table:
                if k1 is not None:
                    yield k1
        else:
            #Yield all bottom-level keys for the specified top-level key
            index1 = self.hash1(key)
            if self.table[index1] is not None:
                raise KeyError("key is not in the table")
            
            sub_table = self.table[index1]
            for k2 in sub_table:
                if k2 is not None:
                    yield k2

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        #return a list of keys by converting the iterator from iter_kyes to a list
        return list(self.iter_keys(key))

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None: 
            #yield all calues in the table
            for sub_table in self.table:
                if sub_table is not None:
                    for v in sub_table.table.values():
                        yield
        else:
            #yield all values for the provided top-level key
            index1 = self.hash1(key)
            if self.table[index1] is None:
                raise KeyError("key1 is not in the table")
            
            sub_table = self.table[index1]
            for v in sub_table.table.values():
                yield v

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        #return a list of values by converting the iterator from iter_values to a list
        return list(self.iter_values(key))

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        #get values for the given key pair (key1,key2)
        index1, index2 = self._linear_probe(key[0], key[1], False)
        return self.table[index1][1][index2][1]
        

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        #set the given key pair (key1,key2) to the given value
        index1, index2 = self._linear_probe(key[0], key[1], True)
        if self.table[index1] is None:
            self.table[index1] = (key[0],LinearProbeTable())
        self.table[index1][1][index2] = (key[1],data)

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        #delete the given key pair (key1,key2) from the hash table
        index1, index2 = self._linear_probe(key[0], key[1], False)
        del self.table[index1][1][index2]
        #if the internal table is empty, clear it out 
        if not any(self.table[index1][1]):
            self.table[index1] = None
        

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        #Resize the table and reinsert all values
        old_table = self.table
        new_table_size = self.TABLE_SIZES[self.TABLE_SIZES.index(self.table_size())+1]
        self.table = ArrayR(new_table_size)

        #Reinsert values from the old table to the new table 
        for index in range(len(old_table)):
            if old_table[index] is not None:
                self[old_table[index][0]] = old_table[index][1]

    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        #Calculate the number of key value pairs in the hash table
        count = 0 
        for index in range(self.table_size()):
            if self.table[index] is not None:
                sub_table = self.table[index][1]
                count += len(sub_table)
        return count
        

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        #Building a string representation of the hash table
        output = "{"
        for index in range(self.table_size()):
            if self.table[index] is not None:
                key1 = self.table[index][0]
                sub_table = self.table[index][1]
                for key2 in sub_table:
                    #add the key value pair to the output string
                    output += f"({key1},{key2}):{sub_table[key2]}, "
        #remove the trailing commas and spaces 
        return output[:-2] + "}" 
