from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures import stack_adt

from data_structures import linked_stack

from data_structures.referential_array import ArrayR

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store  #store of trail class is already set to none, which allows us to setting the mountain as none 

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain, Trail(self)) #returns a new trail series with the new mountain added before the current one

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore: 
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, self.following.add_mountain_before(mountain)) 
        
    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, self.following.add_empty_branch_before())
    
TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        self.s1 = linked_stack.LinkedStack(999)

        while True:
            if self.store is None: #if trail is empty 
                if self.s1.is_empty(): #if stack is empty
                    break 
                else:
                    self.store = self.s1.pop()
                    
            elif isinstance(self.store, TrailSeries): #if trail is a series
                    self.store = self.store.add_mountain_before(personality.add_mountain(self.store.mountain)) #add mountain before the current mountain

            elif isinstance(self.store, TrailSplit): #if trail is a split
                if personality.select_branch(self.store.path_top, self.store.path_bottom) is True: #if personality selects top branch (True)
                    self.s1.push(self.store.path_top)#push the top branch to the stack
                    self.store = self.store.path_top.store
                else:
                    self.s1.push(self.store.path_bottom) #push the bottom branch to the stack
                    self.store = self.store.path_bottom.store
            else:
                raise ValueError("Invalid TrailStore")

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        def collect_mountains_from_trail_store(store) -> list[Mountain]:
            if isinstance(store, TrailSeries):
                return [store.mountain] + collect_mountains_from_trail_store(store.following.store)
            elif isinstance(store, TrailSplit):
                return collect_mountains_from_trail_store(store.path_top.store) + collect_mountains_from_trail_store(store.path_bottom.store)
            else:
                raise ValueError("Invalid TrailStore")
        return collect_mountains_from_trail_store(self.store,0)

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        # def _length_k_paths(store, count = 0) -> list[list[Mountain]]:
        #     if count == k:
        #         return []
        #     if isinstance(store, TrailSeries):
        #         return [[store.mountain]] + _length_k_paths(store.following.store, count + 1)
        #     elif isinstance(store, TrailSplit):
        #         return _length_k_paths(store.path_top.store, path) + _length_k_paths(store.path_bottom.store, count)
        #     else:
        #         raise ValueError("Invalid TrailStore")
        # return _length_k_paths(self.store)
        pass

        def _length_k_paths(store, path: list[Mountain] = []) -> list[list[Mountain]]:
            if len(path) == k:
                return [path]
            if store is None:
                return []
            if isinstance(store, TrailSeries):
                return _length_k_paths(store.following.store, path + [store.mountain])
            elif isinstance(store, TrailSplit):
                return _length_k_paths(store.path_top.store, path) + _length_k_paths(store.path_bottom.store, path)
            else:
                raise ValueError("Invalid TrailStore")

        return _length_k_paths(self.store)

        
   