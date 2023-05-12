from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        """
        initialises the list of mountains

        :complexity: O(1)

        """
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        """
        add a mountain to the manager

        :complexity: O(1)

        """
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        """
        remove a mountain from the manager

        :complexity: O(1)

        """
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        remove teh old mountain and add the new mountain

        :complexity: O(1)

        """
        index = self.mountains.index(old_mountain)
        self.mountains[index] = new_mountain

    def mountains_with_difficulty(self, diff: int):
        """
        return a list of all mountains with this difficulty
        
        :complexity: O(m), where m is the number of mountains
        """
        return [m for m in self.mountains if m.difficulty_level == diff]

    def group_by_difficulty(self):
        """
        return a list of lists of all mountains, grouped by and sorted by ascending difficulty

        :complexity: O(mlogm), where m is the number of mountains
        
        """
        sorted_mountains = sorted(self.mountains, key=lambda m: m.difficulty_level)
        grouped_mountains = []

        for m in sorted_mountains:
            if not grouped_mountains or grouped_mountains[-1][0].difficulty_level != m.difficulty_level:
                grouped_mountains.append([m])
            else:
                grouped_mountains[-1].append(m)

        return grouped_mountains
