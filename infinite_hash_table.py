from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None: # initialise the hash table
        self.table = ArrayR(self.TABLE_SIZE)
        self.level = 0
        self.count = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
         """
        current = self.table
        location = self.get_location(key)
        for i in location:
            current = current[i]
        return current


    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        current = self.table

        position = self.hash(key)

        while True:


            if isinstance(current[position], ArrayR):
                current = current[position]
                self.level += 1

            elif isinstance(current[position], tuple): #if table is tuple
                
                old_variable = current[position]
                current[position] = ArrayR(27)
                self.level += 1                     # old var = (key,value) # curr table = arrayr
                current[self.hash(old_variable[0])] = old_variable


            elif current[position] is None: #if table is none
                current[position] = (key,value)
                self.level = 0 
                self.count += 1
                break
         

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """

        index = self.hash(key)

        aim_key = self.table[index]

        if aim_key is None:
            raise KeyError('Key is not found')
        
        elif type(aim_key) is InfiniteHashTable:
            del aim_key[key]
            
            if len(aim_key) == 1:
                one = [i for i in aim_key.table if i is not None][0]
                assert type(one) is list
                self.table[index] = one
                self.count += 1
        
        else:
            assert type(aim_key) is list
            
            original_k = aim_key[0]
            original_v = aim_key[1]

            if original_k[self.level] == key[self.level]:
                self.table[index] = None
                self.count -= 1

            else:
                raise KeyError('Key is not found')
                     


    def __len__(self):

        return self.count
        
    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """

        location = [] #list of positions
        current = self.table # initialiases the current table

        position = self.hash(key) 

        while True:

                
            if isinstance(current[position], ArrayR):  # if its a table
                location.append(position)
                current = current[position]
                self.level += 1
                print('stop')
                print(location)

            elif isinstance(current[position], tuple): # if its a item
                print('yes')
                location.append(position)
                self.level = 0
                return location

            #if table is none
            elif current[position] is None:
                print('no')
                self.level = 0 
                raise KeyError('Key is not found')

    def __contains__(self, key: K) -> bool:
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
