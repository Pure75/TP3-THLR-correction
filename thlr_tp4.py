from graphviz import Digraph
from display_automaton import export_automaton


# Non-deterministic finite automaton
class NFA:

    def __init__(self, all_states, initial_states, final_states,
                 alphabet, edges):
        # States: a set of integers
        self.all_states = set(all_states)
        # The alphabet: a set of strings
        # "" stands for epsilon
        self.alphabet = set(alphabet)
        if "" in self.alphabet:
            self.alphabet.remove("")
        # Initial and final states: two sets of integers
        self.initial_states = set(initial_states).intersection(self.all_states)
        self.final_states = set(final_states).intersection(self.all_states)
        # There must be an initial state; if there isn't, an initial state 0
        # is added
        if not self.initial_states:
            self.initial_states.add(0)
            self.all_states.add(0)
        # Edges: a dictionnary (origin, letter): set of destinations
        self.next_states = {(state, letter): set()
                            for state in self.all_states
                            for letter in self.alphabet}
        for edge in set(edges):
            if (edge[0] in self.all_states) and (edge[2] in self.all_states) \
                    and (edge[1] in self.alphabet):
                self.next_states[(edge[0], edge[1])].add(edge[2])

    # Returns the set of states reachable from the state 'origin'
    # by reading the input 'word'
    def reachable_states(self, origin, word):
        if not word:
            return set([origin])
        else:
            # Direct successors
            mid_states = set(self.next_states[(origin, word[0])])
            # Recursive application
            target_states = set()
            for mid in mid_states:
                for target in self.reachable_states(mid, word[1:]):
                    target_states.add(target)
            return target_states

    # Determines if the state 'target' is reachable from the state 'origin'
    def accessible(self, origin, target):
        visited = set()
        incoming = set()
        incoming.add(origin)
        while (len(incoming) > 0):
            current = incoming.pop()
            visited.add(current)
            if current == target:
                return True
            else:
                for letter in self.alphabet:
                    for next_state in self.next_states[(current, letter)]:
                        if not (next_state in visited):
                            incoming.add(next_state)
        return False

    # Determines if the state 'state' is useful
    def is_useful(self, state):
        is_accessible = any([self.accessible(initial, state) \
            for initial in self.initial_states])
        is_coaccessible = any([self.accessible(state, final) \
            for final in self.final_states])
        return (is_accessible and is_coaccessible)

    # Remove the state 'state' from the automaton
    def remove_state(self, state):
        if state in self.all_states:
            self.all_states.remove(state)
            for letter in self.alphabet:
                del self.next_states[(state, letter)]
                for origin in self.all_states:
                    if state in self.next_states[(origin, letter)]:
                        self.next_states[(origin, letter)].remove(state)
            if state in self.initial_states:
                self.initial_states.remove(state)
            if state in self.final_states:
                self.final_states.remove(state)

    # Prune the automaton
    def prune(self):
        old_states =self.all_states.copy()
        for state in old_states:
            if not self.is_useful(state):
                self.remove_state(state)

    # Question 1
    # Determines if the NFA is complete
    def is_complete(self):
        pass

    # Question 2
    # Determines if the NFA is deterministic
    def is_deterministic(self):
        pass

    # Question 3
    # Returns the set of states reachable from the states in 'origins'
    # by reading the letter 'letter'
    def reachable_set(self, origins, letter):
        pass

    # Question 4
    # Returns a DFA equivalent to the NFA
    def determinize(self):
        pass

    # Question 5
    # Returns the mirror of the current NFA
    def mirror(self):
        pass

    # Question 6
    # Returns the minimal DFA matched to the current NFA
    def minimization(self):
        pass