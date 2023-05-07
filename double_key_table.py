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

        #create the underlying array. If sizes is not None, the provided array should replace the existing TABLE_SIZES to decide the size of the top-level hash table. If internal_sizes is not None, the provided array should replace the existing TABLE_SIZES for the internal hash tables (See hash_table.py for an example)).
        
        #self.sizes.index

        self.table = ArrayR(self.TABLE_SIZES[0]) # should be 0 for the first one (self.size) = 0 

        if sizes is not None:
            sizes = self.TABLE_SIZES

        elif internal_sizes is not None:
            internal_sizes = self.TABLE_SIZES
        

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

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        position = self.hash1(key1, self.table_size)

        count = 0

        for _ in range(self.table_size):
            if self.table[position] is None:
                break
            if self.table[position][0] == key1:
                return self.table[position][1]
            position = (position + 1) % self.table_size

            if count == self.table_size:
                raise FullError('Table is full')
            
            count += 1
        raise KeyError('Key is not found') 



    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
         
        if key is None:
            #iterates through top level keys if key is None
            for index in range(self.table_size()):
                if self.table[index] is not None:
                    yield self.table[index][0]
        else:
            #iterates through bottom level keys for specified top-level key
            position = self.hash1(key)
            if self.table[position] is not None:
                sub_table = self.table[position][1]
                for k in sub_table.iter_keys():
                    yield k

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
            #iterate through all values in the table if the key is None
            for index in range(self.table_size()):
                if self.table[index]is not None: 
                    sub_table = self.table[index][1]
                    for v in sub_table.values():
                        yield v
        else:
            #Iterate through all values for the specified top-level key
            position = self.hash1(key)
            if self.table[position] is not None:
                sub_table = self.table[position][1]
                for v in sub_table.values():
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
        position = self.hash1(key[0])
        if self.table[position] is not None:
            sub_table = self.table[position][1]
            return sub_table[key[1]]
        raise KeyError('Key is not found')
        

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        #set the value for the given key pair (key1,key2) in the hash table
        position = self.hash1(key[0])
        if self.table[position] is None:
            #If the position is empty, create a new sub-table and add the key-value pair
            sub_table = LinearProbeTable()
            sub_table[key[1]] = data
            self.table[position] = (key[0], sub_table)
        else:
            #If the position is occupied, add the key value pait to the existing sub_table 
            sub_table = self.table[position][1]
            sub_table[key[1]] = data

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        #delete the given key pair (key1,key2) from the hash table
        position = self.hash1(key[0])
        if self.table[position] is not None:
            sub_table = self.table[position][1]
            del sub_table[key[1]]
        else:
            raise KeyError('Key is not found')
        

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
