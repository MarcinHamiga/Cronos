import pygame
from statuses import *
from random import randint


class Skill:
    def __init__(self, sp_cost, icon, desc):
        self.sp_cost = sp_cost
        self.icon = icon
        self.desc = desc

    def use(self, target):
        pass


class Firebreath(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon, "Spew fire at the enemy, dealing guaranteed damage.")
        self.base_damage = 10

    def use(self, user, target):
        damage = randint(self.base_damage, int(user.attack * 1.5))
        target.take_damage(target)
        roll = randint(0, 100)
        if roll < 40:
            target.apply_status(Aflame(3))


class SkillDict:
    def __init__(self, assets):
        self.skill_dict = {
            "FIREBREATH": Firebreath(7, assets["SKL_FIREBREATH"])
        }

    def get_skill(self, skill):
        skill = skill.upper()
        return self.skill_dict[skill]
