#!/usr/bin/env python3

## Markov Decision Process simulator.
class MDP:
    @property
    def states(self):
        raise NotImplementedError

    @property
    def actions(self):
        raise NotImplementedError

    def actions_at(self, state):
        raise NotImplementedError

    def act(self, state, action):
        raise NotImplementedError
