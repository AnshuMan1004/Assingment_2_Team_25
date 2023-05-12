from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        """
        initialises the list of mountains
        
        :complexity: O(1)
        """
        self.mountains = []

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        adds mountains to the list of mountains to the organiser

        input: mountains(list of mountaina)
        output: None

        :complexity: O(nlogn)
        """
        self.mountains.extend(mountains)
        self.mountains.sort(key=lambda mountain: (mountain.length, mountain.difficulty_level, mountain.name))

    def cur_position(self, mountain: Mountain) -> int:
        """
        finds the rank of the provided mountain given all mountians included so far.

        input: mountain
        output: rank of the mountain

        :KeyError: if the mountain hasnt been added yet

        :complexity: O(n), where n is the number of mountains in the list
        """
        for index, m in enumerate(self.mountains):
            if m.name == mountain.name and m.difficulty_level == mountain.difficulty_level and m.length == mountain.length :
                return index  
        raise KeyError("Mountain not found")

    
