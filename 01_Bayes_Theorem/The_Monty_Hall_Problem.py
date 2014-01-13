#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from random import choice

STRATEGY_STICK  = 1
STRATEGY_SWITCH = 2

class MontyHall:
    DOOR_CLOSED   = 0
    DOOR_OPENED   = 1
    DOOR_SELECTED = 2

    def __init__(self, doors_num = 3, answer = None):
        self.initialze_doors(doors_num)
        self.set_answer(answer)
        # for debug
        self.doors_status = {
            self.DOOR_CLOSED: 'closed',
            self.DOOR_OPENED: 'opened',
            self.DOOR_SELECTED: 'selected',
        }
        return
    def initialze_doors(self, doors_num):
        self.doors = {}
        for i in range(doors_num):
            self.doors[i] = self.DOOR_CLOSED
        return
    def set_answer(self, answer = None):
        if answer == None:
            answer = choice(self.doors.keys())
        self.answer = answer
        return
    """
    1. 回答者がドアを選ぶ
    """
    def select_door(self, target_door = None):
        for door,status in self.doors.items():
            if status != self.DOOR_CLOSED:
                raise Exception("all doors have to be cloesd here!!")

        if target_door == None:
            target_door = choice(self.doors.keys())
        self.doors[target_door] = self.DOOR_SELECTED
        return

    """
    2. Monty が外れのドアを開ける
    """
    def monty_opens_door(self,):
        candidate_doors = [door for door in self.get_doors(self.DOOR_CLOSED) if door != self.answer]
        open_door = choice(candidate_doors)
        self.doors[open_door] = self.DOOR_OPENED
        return

    """
    3. 回答者がドアを変更するかどうかを選ぶ
    """
    def stick_or_switch(self, strategy):
        if strategy == STRATEGY_STICK:
            return
        if strategy == STRATEGY_SWITCH:
            # get selected door
            selected_door = self.get_door(self.DOOR_SELECTED)
            # get closed door
            closed_door = self.get_door(self.DOOR_CLOSED)
            # set selected door to closed
            self.doors[selected_door] = self.DOOR_CLOSED
            # set closed door to selected
            self.doors[closed_door] = self.DOOR_SELECTED
            return
        raise Exception("unknown strategy!!")

    """
    4. 正解を発表する
    """
    def open_answer(self,):
        return self.get_door(self.DOOR_SELECTED) == self.answer

    """
    Helper 関数
    """
    def get_doors(self, target_status):
        return [door for door,status in self.doors.items() if status == target_status]
    def get_door(self, target_status):
        doors = self.get_doors(target_status)
        if len(doors) != 1:
            raise Exception("there has to be one door %s, current_doors: %s"
                            %(self.doors_status[target_status],
                              [(door,self.doors_status[status]) for door,status in self.doors.items()]))
        return doors[0]

def try_n_times(strategy, n = 10000, debug = False):
    hit_kaisuu = 0
    for i in range(n):
        mh = MontyHall(doors_num = 3)
        # select one of the doors
        mh.select_door()
        # monty opens one of the doors
        mh.monty_opens_door()
        # select stick_or_switch
        mh.stick_or_switch(strategy)
        # open!!
        result = mh.open_answer()
        hit_kaisuu += result
    return hit_kaisuu

def main():
    n = 10000
    hit_kaisuu = try_n_times(STRATEGY_STICK, n)
    sys.stdout.write(u"STICK 戦略でのヒット回数: %d\n" %(hit_kaisuu))

    hit_kaisuu = try_n_times(STRATEGY_SWITCH, n)
    sys.stdout.write(u"SWITCH 戦略でのヒット回数: %d\n" %(hit_kaisuu))

if __name__ == '__main__':
    main()
