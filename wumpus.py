#!/usr/bin/env python3

from enum import Enum
from mdp import MDP
import itertools
import numpy as np


class Actions(Enum):
    UP=1
    DOWN=2
    LEFT=3
    RIGHT=4
    PICK_UP=5


_TXT = {
    Actions.UP: "^^",
    Actions.DOWN: "vv",
    Actions.LEFT: "<<",
    Actions.RIGHT: ">>",
    Actions.PICK_UP: "[]"
}


_UP = np.array([0, -1])
_DOWN = np.array([0, 1])
_LEFT = np.array([-1, 0])
_RIGHT = np.array([1, 0])


class WumpusState:
    def __init__(self, x, y, has_gold, has_immunity):
        self.x = x
        self.y = y
        self.has_gold = has_gold
        self.has_immunity = has_immunity

    @property
    def pos(self):
        return np.array([self.x, self.y])


def _clip(p, max_x, max_y):
    p = np.array(max(min(p[0], max_x), 1),
                 max(min(p[0], max_y), 1))


class WumpusMDP(MDP):
    def __init__(self, w, h, cost):
        self._w = w
        self._h = h
        self._cost = cost
        self._objs = {
            'pit': {},
            'gold': {},
            'immune': {},
            'goal': {},
            'wumpus': {}
        }

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def states(self):
        return itertools.product(
            range(self.width), range(self.height), (True, False), (True, False))

    @property
    def actions(self):
        return Actions

    def actions_at(self, state):
        a = [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN]
        if self.gold_at(state) or self.immunity_at(state):
            a += [Actions.PICK_UP]
        return a

    def act(self, state, action):
        if action in [Actions.PICK_UP]:
            return self.pick_up(state, action)
        elif action in [Actions.UP, Actions.DOWN, Actions.LEFT, Actions.RIGHT]
            return self.move(state, action)
        else:
            raise Exception("Invalid action specified: {}".format(action))

    def has_at(self, kind, pos):
        return tuple(pos) in self._objs[kind].keys()

    def reward_at(self, kind, pos):
        return self._objs[kind][tuple(pos)]

    def move(self, state, action):
        probs = [0.7, 0.15, 0.15]

        if action == Actions.UP:
            alst = [_UP, _LEFT, _RIGHT]
        elif action == Actions.DOWN:
            alst = [_DOWN, _RIGHT, _LEFT]
        elif action == Actions.LEFT:
            alst = [_LEFT, _UP, _DOWN]
        elif action == Actions.RIGHT:
            alst = [_RIGHT, _DOWN, _UP]

        new_p = _clip(state.pos + np.random.choice(alst, p=probs),
                      self.width, self.height)
        new_state = WumpusState(new_p[0], new_p[1], state.has_gold, state.has_immunity)

        reward = -self._cost
        is_terminal = False
        if state.has_gold and self.has_at('goal', new_state.pos):
            is_terminal = True
            reward = self.reward_at('goal', new_state.pos)
        elif not state.has_immunity and self.has_at('wumpus', new_state.pos):
            is_terminal = True
            reward = self.reward_at('wumpus', new_state.pos)
        return new_state

    def pick_up(self, state, action):
        has_gold = state.has_gold
        has_immunity = state.has_immunity
        if self.has_at('immunity', new_state.pos):
            pass

#     def __is_valid_state(self, s):
#         return True
#     @property
#     def states(self):
#         return filter(lambda x: self.__is_valid_state(x),
#                       itertools.product(range(1, self.__w+1), range(1, self.__h+1), range(2), range(2)))
#     def actions(self, s):
#         if self.is_gold(s) or self.is_immunity(s):
#             return ["left", "right", "up", "down", "pick up"]
#         else:
#             return ["left", "right", "up", "down"]
#     def is_terminal(self, s):
#         if self.is_goal(s) and self.has_gold(s):
#             return True
#         elif self.is_wumpus(s) and not self.has_immunity(s):
#             return True
#         else:
#             return False
#     def r(self, s, a=None):
#         if self.is_gold(s) and a == "pick up":
#             return self.__golds[s[:2]]
#         if self.is_pit(s):
#             return self.__pits[s[:2]]
#         if self.is_wumpus(s) and not self.has_immunity(s):
#             return self.__wumpus[s[:2]]
#         if self.is_goal(s) and self.has_gold(s):
#             return self.__goals[s[:2]]
#         # if self.is_immunity(s):
#         #     return self.__immunes[s[:2]]
#         return self.__cost
#     def p(self, s1, a, s2):
#         if a == "pick up" and s2 == self.move(s1, a):
#             return 1
#         else:
#             s3s = self.umove(self, s1, a)
#             if s2 in s3s:
#                 return \
#                     (0.8 if s3s[0] == s2 else 0)\
#                     + (0.1 if s3s[1] == s2 else 0)\
#                     + (0.1 if s3s[2] == s2 else 0)
#             else:
#                 return 0
#     def ps(self, s1, a):
#         if a == "pick up":
#             return [(self.move(s1, a), 1)]
#         else:
#             s2s = self.umove(s1, a)
#             return [(s2s[0], 0.8), (s2s[1], 0.1), (s2s[2], 0.1)]
#     def is_pit(self, s):
#         return s[:2] in self.__pits
#     def add_pit(self, x, r):
#         self.__pits[x] = r
#     def is_gold(self, s):
#         return not self.has_gold(s) and s[:2] in self.__golds
#     def add_gold(self, x, r):
#         self.__golds[x] = r
#     def is_immunity(self, s):
#         return not self.has_immunity(s) and s[:2] in self.__immunes
#     def add_immunity(self, x):
#         self.__immunes[x] = 1
#     def is_goal(self, s):
#         return s[:2] in self.__goals
#     def add_goal(self, x, r):
#         self.__goals[x] = r
#     def is_wumpus(self, s):
#         return s[:2] in self.__wumpus
#     def add_wumpus(self, x, r):
#         self.__wumpus[x] = r
#     def has_gold(self, s):
#         return s[2]
#     def has_immunity(self, s):
#         return s[3]
#     def move(self, s, a):
#         s2 = []
#         if a == "pick up" and self.is_gold(s):
#             s2 = (s[0], s[1], 1, s[3])
#         elif a == "pick up" and self.is_immunity(s):
#             s2 = (s[0], s[1], s[2], 1)
#         elif a == "left" and s[0] > 1:
#             s2 = (s[0]-1, s[1], s[2], s[3])
#         elif a == "right" and s[0] < self.__w:
#             s2 = (s[0]+1, s[1], s[2], s[3])
#         elif a == "up" and s[1] < self.__h:
#             s2 = (s[0], s[1]+1, s[2], s[3])
#         elif a == "down" and s[1] > 1:
#             s2 = (s[0], s[1]-1, s[2], s[3])
#         if not s2:
#             return s
#         else:
#             return s2
#     def umove(self, s, a):
#         # pu = ["pick up"] if self.is_gold(s) or self.is_immunity(s) else []
#         if a == "left":
#             return map(lambda a2: self.move(s, a2), ["left", "up", "down"])
#         elif a == "right":
#             return map(lambda a2: self.move(s, a2), ["right", "up", "down"])
#         elif a == "up":
#             return map(lambda a2: self.move(s, a2), ["up", "left", "right"])
#         else:
#             return map(lambda a2: self.move(s, a2), ["down", "left", "right"])
