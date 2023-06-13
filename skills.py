import pygame
from statuses import *
from random import randint


class Skill:
    def __init__(self, sp_cost, icon):
        self.sp_cost = sp_cost
        self.icon = icon

    def use(self, target):
        pass


class Firebreath(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon)
        self.base_damage = 10

    def use(self, user, target):
        damage = randint(self.base_damage, int(user.attack * 1.5))
        target.take_damage(target)
        roll = randint(0, 100)
        if roll < 40:
            target.apply_status(Aflame(3))