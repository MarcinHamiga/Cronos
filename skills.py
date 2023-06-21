import pygame
from statuses import *
from random import randint


class Skill:
    def __init__(self, sp_cost, icon, desc, element, req_level):
        self.sp_cost = sp_cost
        self.icon = icon
        self.desc = desc
        self.required_level = req_level
        self.element = element

    def __str__(self):
        return str(self.__class__.__name__)

    def get_icon(self):
        return self.icon

    def get_req_level(self):
        return self.required_level

    def use(self, target):
        pass


class Firebreath(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon, "Spew fire at the enemy, dealing guaranteed damage.", "Fire", 1)
        self.base_damage = 7
        self.dmg_multi = 1.25

    def use(self, user, target):
        base_damage = self.base_damage + (user.attack // 4)
        damage = randint(base_damage, int(user.attack * self.dmg_multi))
        if target.element == "Nature":
            damage = int(damage * 1.5)
        target.take_damage(damage)
        roll = randint(0, 100)
        if roll < 40:
            target.apply_status(Aflame(3))

        return damage

    def get_min_max_damage(self, user):
        base_damage = self.base_damage + (user.attack // 4)
        return base_damage, int(user.attack * self.dmg_multi)

class Firewhip(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon, "Use your tail to set enemy on fire, while dealing miniscule damage.", "Fire", 4)
        self.dmg_multi = 0.25
        self.base_damage = 0

    def use(self, user, target):
        damage = randint(0, int(user.attack * self.dmg_multi))
        if target.element == "Nature":
            damage = int(damage * 1.5)
        target.take_damage(damage)
        roll = randint(0, 100)
        if roll <= 75:
            target.apply_status(Aflame(4))

        return damage

    def get_min_max_damage(self, user):
        return 0, int(user.attack * self.dmg_multi)

class Whirlwind(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon, "Control the wind to strike thrice, but with reduced damage.", "Wind", 1)
        self.dmg_multi = 0.45

    def use(self, user, target):
        damage_1 = randint(0, int(user.attack * self.dmg_multi))
        damage_2 = randint(0, int(user.attack * self.dmg_multi))
        damage_3 = randint(0, int(user.attack * self.dmg_multi))

        target.take_damage(damage_1 + damage_2 + damage_3)

        return damage_1 + damage_2 + damage_3

    def get_min_max_damage(self, user):
        return 0, int(user.attack * self.dmg_multi * 3)


class Waterblast(Skill):

    def __init__(self, sp_cost, icon):
        super().__init__(sp_cost, icon, "Launch a powerful water blast at the enemy dealing incredible damage, but with a chance to miss altogether.", "Water", 1)
        self.dmg_multi = 1.5
        self.base_damage = 5

    def use(self, user, target):
        damage = randint(int(self.base_damage + (user.attack // 4)), int(user.attack * self.dmg_multi))
        roll = randint(0, 100)
        if roll < 30:
            return 0
        else:
            if target.element == "Fire":
                target.take_damage(int(damage * 1.5))
            else:
                target.take_damage(damage)

            return damage

    def get_min_max_damage(self, user):
        return self.base_damage + (user.attack // 4), int(user.attack * self.dmg_multi)


class SkillDict:
    def __init__(self, assets):
        self.skill_dict = {
            "FIREBREATH": Firebreath(7, assets["SKL_FIREBREATH"]),
            "FIREWHIP": Firewhip(9, assets["SKL_FIREWHIP"]),
            "WHIRLWIND": Whirlwind(6, assets["SKL_WHIRLWIND"]),
            "WATERBLAST": Waterblast(9, assets["SKL_WATERBLAST"])
        }

    def get_skill(self, skill):
        skill = skill.upper()
        return self.skill_dict[skill]


class SkillCard:

    def __init__(self, skill, fightmenu):

        self.icon = skill.get_icon()
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.center = 24, 36

        self.surface = pygame.Surface((240, 72))

        self.fightmenu = fightmenu
        self.skill = skill

    def draw_card(self, font, is_current: bool):
        match is_current:
            case True:
                self.surface.fill((255, 255, 255))

                self.surface.blit(self.icon, self.icon_rect)

                name, name_rect = font.render(f"Name: {str(self.skill)}", fgcolor=(90, 0, 0))
                name_rect.center = 144, 12

                self.surface.blit(name, name_rect)

                cost, cost_rect = font.render(f"Cost: {self.skill.sp_cost}", fgcolor=(0, 0, 0))
                cost_rect.center = 144, 36

                self.surface.blit(cost, cost_rect)

                min_dmg, max_dmg = self.skill.get_min_max_damage(self.fightmenu.player_creature)
                dmg, dmg_rect = font.render(f"Dmg/heal: {min_dmg}-{max_dmg}", fgcolor=(0, 0, 0))
                dmg_rect.center = 144, 60

                self.surface.blit(dmg, dmg_rect)

                return self.surface

            case False:
                self.surface.fill((128, 0, 35))

                self.surface.blit(self.icon, self.icon_rect)

                name, name_rect = font.render(f"Name: {str(self.skill)}")
                name_rect.center = 144, 12

                self.surface.blit(name, name_rect)

                cost, cost_rect = font.render(f"Cost: {self.skill.sp_cost}", fgcolor=(255, 255, 255))
                cost_rect.center = 144, 36

                self.surface.blit(cost, cost_rect)

                min_dmg, max_dmg = self.skill.get_min_max_damage(self.fightmenu.player_creature)
                dmg, dmg_rect = font.render(f"Dmg/heal: {min_dmg}-{max_dmg}", fgcolor=(255, 255, 255))
                dmg_rect.center = 144, 60

                self.surface.blit(dmg, dmg_rect)

                return self.surface
