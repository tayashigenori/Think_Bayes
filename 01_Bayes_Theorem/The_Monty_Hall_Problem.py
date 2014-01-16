#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from random import choice

class Door:
    DOOR_CLOSED   = 0
    DOOR_OPEN     = 1
    DOOR_SELECTED = 2

    def __init__(self, status = None):
        if status == None:
            status = self.DOOR_CLOSED
        self.__status = status
        self.__is_hit = False
        return

    def get_status(self, status):
        return self.__status
    def __set_status(self, status):
        self.__status = status
        return
    def close(self,):
        self.__set_status(self.DOOR_CLOSED)
        return
    def open(self,):
        self.__set_status(self.DOOR_OPEN)
        return
    def select(self,):
        self.__set_status(self.DOOR_SELECTED)
        return

    def __is_status(self, status):
        return self.__status == status
    def is_closed(self,):
        return self.__is_status(self.DOOR_CLOSED)
    def is_open(self,):
        return self.__is_status(self.DOOR_OPEN)
    def is_selected(self,):
        return self.__is_status(self.DOOR_SELECTED)

    def set_hit(self,):
        self.__is_hit = True
        return
    def unset_hit(self,):
        self.__is_hit = False
        return
    def is_hit(self,):
        return self.__is_hit == True

    def get_status_str(self,):
        door_status = {
            self.DOOR_CLOSED: "閉じ\t\t|",
            self.DOOR_OPEN: "開き\t\t|",
            self.DOOR_SELECTED: "選\t-->\t|",
        }
        return door_status[self.__status]
    def get_hit_str(self,):
        is_hit = {
            True: "■当たり",
            False: "□はずれ",
        }
        return is_hit[self.__is_hit]

class Doors:
    def __init__(self, doors_num = 3):
        self.__list = self.initialize_doors(doors_num)
        self.__hit = self.set_hit()
        return
    def initialize_doors(self, doors_num):
        l = []
        for d_int in range(doors_num):
            l.append(Door())
        return l

    def get_all_doors(self,):
        return self.__list
    def get_closed_doors(self,):
        return [d_obj for d_obj in self.__list if d_obj.is_closed()]
    def get_open_doors(self,):
        return [d_obj for d_obj in self.__list if d_obj.is_open()]
    def get_selected_doors(self,):
        return [d_obj for d_obj in self.__list if d_obj.is_selected()]

    def get_closed_door(self,):
        doors = self.get_closed_doors()
        if len(doors) != 1:
            raise Exception("there has to be one door closed, current_doors: %s"
                            %[d_obj.get_status_str() for d_obj in self.__list])
        return doors[0]
    def get_open_door(self,):
        doors = self.get_open_doors()
        if len(doors) != 1:
            raise Exception("there has to be one door open, current_doors: %s"
                            %[d_obj.get_status_str() for d_obj in self.__list])
        return doors[0]
    def get_selected_door(self,):
        doors = self.get_selected_doors()
        if len(doors) != 1:
            raise Exception("there has to be one door selected, current_doors: %s"
                            %[d_obj.get_status_str() for d_obj in self.__list])
        return doors[0]

    def set_hit(self, hit = None):
        if hit == None:
            hit = choice(self.__list)
        return hit.set_hit()

class MontyHallProblem:
    STRATEGY_STICK  = 1
    STRATEGY_SWITCH = 2

    def __init__(self, doors_obj):
        self.__doors = doors_obj
        return
    def set_strategy_stick(self,):
        self.__strategy = self.STRATEGY_STICK
        return
    def set_strategy_switch(self,):
        self.__strategy = self.STRATEGY_SWITCH
        return
    """
    1. 回答者がドアを選ぶ
    """
    def select_door(self, target_door_int = None):
        for door_obj in self.__doors.get_all_doors():
            if door_obj.is_closed() == False:
                raise Exception("all doors have to be cloesd here!!")

        target_door_obj = choice(self.__doors.get_all_doors())
        if isinstance(target_door_int, int):
            target_door_obj = self.__doors.get_all_doors()[target_door_int]
        return target_door_obj.select()
    """
    2. Monty が外れのドアを開ける
    """
    def monty_opens_door(self,):
        candidate_doors = [door_obj for door_obj in self.__doors.get_closed_doors()
                           if door_obj.is_hit() == False]
        target_door_obj = choice(candidate_doors)
        return target_door_obj.open()
    """
    3. 回答者がドアを変更するかどうかを選ぶ
    """
    def stick_or_switch(self,):
        if self.__strategy == self.STRATEGY_STICK:
            return
        if self.__strategy == self.STRATEGY_SWITCH:
            selected_door_obj = self.__doors.get_selected_door()
            closed_door_obj = self.__doors.get_closed_door()
            # set selected door to closed
            selected_door_obj.close()
            # set closed door to selected
            closed_door_obj.select()
            return
        raise Exception("unknown strategy!!")

    """
    4. 正解を発表する
    """
    def open_answer(self,):
        return self.__doors.get_selected_door().is_hit()
    def show_results(self,):
        for door_obj in self.__doors.get_all_doors():
            sys.stderr.write("%s" %door_obj.get_status_str())
            if door_obj.is_hit():
                sys.stderr.write("%s" %door_obj.get_hit_str())
            sys.stderr.write("\n")
        sys.stderr.write("------------\n")

def try_n_times(strategy_stick = False, n = 10000, debug = False):
    hit_kaisuu = 0
    for i in range(n):
        doors_obj = Doors(doors_num = 3)
        mh = MontyHallProblem(doors_obj)
        # 回答者がドアを選ぶ
        mh.select_door()
        # モンティが外れのドアを開ける
        mh.monty_opens_door()
        # 回答者がいまのドアのまま(STICK)か変更する(SWITCH)かを選ぶ
        if strategy_stick:
            mh.set_strategy_stick()
        else:
            mh.set_strategy_switch()
        mh.stick_or_switch()
        # 正解発表！
        result = mh.open_answer()
        if debug == True:
            mh.show_results()
        hit_kaisuu += result
    return hit_kaisuu

def main():
    n = 10000
    hit_kaisuu = try_n_times(strategy_stick = True, n = 10000, debug = True)
    sys.stdout.write("STICK 戦略でのヒット回数: %d\n" %(hit_kaisuu))

    hit_kaisuu = try_n_times(strategy_stick = False, n = 10000, debug = True)
    sys.stdout.write("SWITCH 戦略でのヒット回数: %d\n" %(hit_kaisuu))

if __name__ == '__main__':
    main()
