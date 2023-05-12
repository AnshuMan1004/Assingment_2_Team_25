from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures import stack_adt

from data_structures import referential_array

from data_structures import linked_stack

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
        """
        Removes the mountain at the beginning of this series.

        store of trail class is already set to none, which allows us to setting the mountain as none 

        :complexity: O(1)
        
        """
        return self.following.store
    
    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Adds a mountain in series before the current one.
        
        input: mountain
        output: trail series with the new mountain added before the current one

        :complexity: O(1)
        
        """
        return TrailSeries(mountain, Trail(self)) 

    def add_empty_branch_before(self) -> TrailStore:
        """
        Adds an empty branch, where the current trailstore is now the following path.
        
        :complexity: O(1)

        """
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore: 
        """
        Adds a mountain after the current mountain, but before the following trail.

        :complexity: O(1)

        """
        return TrailSeries(self.mountain, self.following.add_mountain_before(mountain)) 
        
    def add_empty_branch_after(self) -> TrailStore:
        """
        Adds an empty branch after the current mountain, but before the following trail.
        
        :complexity: O(1)

        """
        return TrailSeries(self.mountain, self.following.add_empty_branch_before())
    
TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Adds a mountain before everything currently in the trail.
        
        input: mountain
        output: trail series with the new mountain added before the current one

        :complexity: O(1)

        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        
        Adds an empty branch before everything currently in the trail.

        :complexity: O(1)

        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.
        
        input: personality
        output: none

        :complexity: O(n), where n is the number of mountains in the trail

        """
        
        self.s1 = linked_stack.LinkedStack(999)

        store = self.store
        while True:

            
            if store is None: #if trail is empty 
                if self.s1.is_empty() is True: #if stack is empty
                    break
                else:

                    store = self.s1.pop() #set the current store to the following store

            elif isinstance(store, TrailSeries): #if trail is a series

                    personality.add_mountain(store.mountain) #add mountain to the personality
                    store = store.following.store

            elif isinstance(store, TrailSplit): #if trail is a split
                
                self.s1.push(store.path_follow.store) #push the following path to the stack

                if personality.select_branch(store.path_top, store.path_bottom) is True: #if personality selects top branch (True)
                    
                    store = store.path_top.store #top branch
                else:
                    store= store.path_bottom.store #bottom branch
            else:
                raise ValueError("Invalid TrailStore")

    def collect_all_mountains(self) -> list[Mountain]:
        """
        Returns a list of all mountains on the trail.

        :complexity: O(n), where n is the number of mountains in the trail

        """
        def collect_mountains_from_trail_store(store) -> list[Mountain]:
            if store is None:
                return []
            elif isinstance(store, TrailSeries):
                return [store.mountain] + collect_mountains_from_trail_store(store.following.store)
            elif isinstance(store, TrailSplit):
                return (collect_mountains_from_trail_store(store.path_top.store) + collect_mountains_from_trail_store(store.path_bottom.store) + collect_mountains_from_trail_store(store.path_follow.store))
            else:
                raise ValueError("Invalid TrailStore")
        return collect_mountains_from_trail_store(self.store)

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        
        input: k (number of mountains in the path)
        output: list of all paths of containing exactly k mountains

        :complexity: O(n)

        """
        def _length_k_paths(store, path=None):
            if path is None :
                path = []
            
            if isinstance(store, TrailSeries):
                path.append(store.mountain.name)
                if len(path) == k:
                    paths.append(path.copy())
                elif len(path) < k:
                    _length_k_paths(store.following.store, path)
                path.pop()

            elif isinstance(store, TrailSplit):
                _length_k_paths(store.path_top.store, path.copy())
                _length_k_paths(store.path_bottom.store, path.copy())
                _length_k_paths(store.path_follow.store, path.copy())
                
            elif store is None: 
                return
            else:
                raise ValueError("Invalid TrailStore")
            
        paths = []
        _length_k_paths(self.store)
        return [','.join(path) for path in paths]