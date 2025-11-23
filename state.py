import re 
from enum import Enum 
from typing import List, Optional, Set, Dict, State


class State:
    _id_counter = 0
    
    def __init__(self, is_accept: bool = False):
        self.id = State._id_counter
        State._id_counter += 1
        self.is_accept = is_accept
        self.transitions: Dict[str, Set["State"]] = {}  # char -> set of states
        self.epsilon_transitions: Set["State"] = set()
    
    def add_transition(self, char: str, state: "State"):
        if char not in self.transitions:
            self.transitions[char] = set()
        self.transitions[char].add(state)
    
    def add_epsilon_transition(self, state: "State"):
        self.epsilon_transitions.add(state)
    
    def __repr__(self):
        return f"State({self.id}, accept={self.is_accept})"

class NFA:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept
    
    def get_epsilon_closure(self, states: Set[State]) -> Set[State]:
        """Get all states reachable via epsilon transitions"""
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for next_state in state.epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure
    
    def simulate(self, input_string: str) -> bool:
        """Simulate NFA on input string"""
        current_states = self.get_epsilon_closure({self.start})

        for char in input_string:
            next_states: Set[State] = set()
            for state in current_states:
                if char in state.transitions:
                    next_states.update(state.transitions[char])

            current_states = self.get_epsilon_closure(next_states)
            if not current_states:
                return False

        return any(state.is_accept for state in current_states)