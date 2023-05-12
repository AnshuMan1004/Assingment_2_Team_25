from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        index = self.mountains.index(old_mountain)
        self.mountains[index] = new_mountain

    def mountains_with_difficulty(self, diff: int):
        return [m for m in self.mountains if m.difficulty_level == diff]

    def group_by_difficulty(self):
        sorted_mountains = sorted(self.mountains, key=lambda m: m.difficulty_level)
        grouped_mountains = []

        for m in sorted_mountains:
            if not grouped_mountains or grouped_mountains[-1][0].difficulty_level != m.difficulty_level:
                grouped_mountains.append([m])
            else:
                grouped_mountains[-1].append(m)

        return grouped_mountains
