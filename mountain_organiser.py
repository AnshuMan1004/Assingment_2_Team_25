from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        raise NotImplementedError()

    def cur_position(self, mountain: Mountain) -> int: 
        #Finds the rank of the provided mountain given all mountains included so far.
        #Raises KeyError if this mountain hasn't been added yet.
        raise NotImplementedError()

    def add_mountains(self, mountains: list[Mountain]) -> None: # adds a list of mountains to the organiser
        raise NotImplementedError()
