import pygame
from statuses import *
from random import randint


class Skill:
    def __init__(self, sp_cost, icon, desc, req_level):
        self.sp_cost = sp_cost
        self.icon = icon
        self.desc = desc
        self.required_level = req_level

    def get_icon(self):
        return self.icon

    def use(self, target):
        pass


class Firebreath(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon, "Spew fire at the enemy, dealing guaranteed damage.", 1)
        self.base_damage = 10
        self.dmg_multi = 1.5

    def use(self, user, target):
        damage = randint(self.base_damage, int(user.attack * self.dmg_multi))
        target.take_damage(damage)
        roll = randint(0, 100)
        if roll < 40:
            target.apply_status(Aflame(3))

        return damage


class SkillDict:
    def __init__(self, assets):
        self.skill_dict = {
            "FIREBREATH": Firebreath(7, assets["SKL_FIREBREATH"])
        }

    def get_skill(self, skill):
        skill = skill.upper()
        return self.skill_dict[skill]


class SkillCard:

    def __init__(self, skill, creature):

        self.icon = skill.get_icon()
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.center = 24, 36

        self.surface = pygame.Surface((240, 72))

        self.skill = skill
        self.creature = creature

    def draw_card(self, font, is_current: bool):
        match is_current:
            case True:
                self.surface.fill((255, 255, 255))

                self.surface.blit(self.icon, self.icon_rect)

                name, name_rect = font.render(f"Name: {self.skill.__class__.__name__}", fgcolor=(90, 0, 0))
                name_rect.center = 144, 12

                self.surface.blit(name, name_rect)

                cost, cost_rect = font.render(f"Cost: {self.skill.sp_cost}", fgcolor=(0, 0, 0))
                cost_rect.center = 144, 36

                self.surface.blit(cost, cost_rect)

                numerical_dmg = self.creature.attack
                dmg, dmg_rect = font.render(f"Dmg/heal: {self.skill.base_damage}-{int(self.creature.attack * self.skill.dmg_multi)}", fgcolor=(0, 0, 0))
                dmg_rect.center = 144, 60

                self.surface.blit(dmg, dmg_rect)

                return self.surface

            case False:
                self.surface.fill((128, 0, 35))

                name, name_rect = font.render(f"Name: {self.skill.__class__.__name__}")
                name_rect.center = 144, 12

                self.surface.blit(name, name_rect)

                cost, cost_rect = font.render(f"Cost: {self.skill.sp_cost}", size=24, fgcolor=(255, 255, 255))
                cost_rect.center = 144, 12

                self.surface.blit(cost, cost_rect)

                numerical_dmg = self.creature.attack
                dmg, dmg_rect = font.render(f"Dmg/heal: {self.skill.base_damage}-{int(self.creature.attack * self.skill.dmg_multi)}",
                                            size=24, fgcolor=(255, 255, 255))
                dmg_rect = 144, 36

                self.surface.blit(dmg, dmg_rect)

                return self.surface
