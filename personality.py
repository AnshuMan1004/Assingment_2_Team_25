from abc import ABC, abstractmethod
from mountain import Mountain
from trail import Trail

class WalkerPersonality(ABC):

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains.append(mountain)

    @abstractmethod
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> bool:
        """Selects a branch to take, True for top, False for bottom."""
        if top_branch is None:                                          #if top branch is none then the bottom branch is selcted, else if bottom branch is none then the top branch is selected
            return False
        elif bottom_branch is None:
            return True

class TopWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> bool:
        # Always select the top branch
        return True                                                                     #true means select top branch and false means select bottom branch

class BottomWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> bool:
        # Always select the bottom branch
        return False

class LazyWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> bool:
        """
        Try looking into the first mountain on each branch,
        take the path of least difficulty.
        """

        # isinstance breaks across imports if running the original file as main
        # So just check __class__.__name__ :(
        top_m = top_branch.store.__class__.__name__ == "TrailSeries"
        bot_m = bottom_branch.store.__class__.__name__ == "TrailSeries"
        if top_m and bot_m:
            return top_branch.store.mountain.difficulty_level < bottom_branch.store.mountain.difficulty_level
        # If one of them has a mountain, don't take it.
        # If neither do, then take the top branch.
        return not top_m
