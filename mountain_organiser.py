from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains.extend(mountains)
        self.mountains.sort(key=lambda mountain: (mountain.length, mountain.difficulty_level, mountain.name))

    def cur_position(self, mountain: Mountain) -> int:
        for index, m in enumerate(self.mountains):
            if m.name == mountain.name and m.difficulty_level == mountain.difficulty_level and m.length == mountain.length :
                return index  
        raise KeyError("Mountain not found")

    
