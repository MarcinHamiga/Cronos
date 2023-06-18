from random import randint
import pygame
import skills


class Creature:
    def __init__(self, level, health, special_points, attack, defense, hidden_skills, name, element):
        self.image = None
        self.rect = None
        self.name = name
        self.xp = 0
        self.is_down = False   # Zmienna oznaczająca że stworek jest niezdatny do walki
        self.is_defending = False  # Zmienna określająca czy w danej turze stworek broni się zwiększając swoją obronę
        self.level = level # Poziom stworka
        self.health = health
        self.max_health = health
        self.special_points = special_points
        self.max_special_points = special_points
        self.attack = attack
        self.defense = defense
        self._guard_bonus = int(self.defense * 0.2)
        self._statuses = []   # Lista zawierająca wszystkie nałożone na stworka statusy
        self.skills = []    # Lista ruchów dostępnych dla stworka
        self.hidden_skills = hidden_skills
        self.element = element

    def apply_status(self, applied_status):

        for status in self._statuses:
            if status.__class__.__name__ == applied_status.__class__.__name__:
                status.extend_status(applied_status.turns_left)
                return

        self._statuses.append(applied_status)

    def process_statuses(self):

        for idx, status in enumerate(self._statuses):
            status.take_effect(self)
            status.decrement_turn()
            if status.turns_left == 0:
                self._statuses.pop(idx)

    def clear_statuses(self):
        self._statuses = []

    def attack_target(self, target):
        target_def = target.get_defense()
        # Jeżeli atak stworka jest większy niż obrona celu, ilość obrażeń losowana jest z pełnego przedziału od 0 do wartości ataku,
        # natomiast jeżeli atak stworka jest mniejszy niż obrona celu, obrażenia zostają zredukowane do 25% pierwotnej wartości
        damage = randint(0, self.attack)
        if self.attack > target_def:
            return target.take_damage(damage)
        else:
            return target.take_damage(damage // 4)
    
    def use_skill(self, idx, target):
        skill = self.skills[idx]
        self.special_points -= skill.sp_cost
        return self.skills[idx].__class__.__name__, self.skills[idx].use(self, target)

    def add_skill(self, skill):
        self.skills.append(skill)

    def add_hidden_skill(self, skill):
        if skill.get_req_level() <= self.level:
            self.skills.append(skill)
        else:
            self.hidden_skills.append(skill)
            
    def guard(self):
        self.defense += self._guard_bonus
        self.is_defending = True
        
    def end_guard(self):
        self.defense -= self._guard_bonus
        self.is_defending = False
    
    def check_if_down(self):
        if self.health <= 0:
            self.health = 0
            self.is_down = True
        return self.is_down
            
    def revive(self, revive_health=1):
        self.is_down = False
        self.health = revive_health
        
    def take_damage(self, amount) -> int:
        if amount == 0:
            return 0
        self.health -= amount
        self.check_if_down()
        return amount
        
    def heal(self, amount):
        self.set_health(self.health + amount)
    
    def recover_sp(self, amount):
        self.set_sp(self.special_points + amount)

    def revitalize(self):
        self.revive(self.max_health)
        self.recover_sp(self.max_special_points)
    
    def set_image(self, image):
        self.image = image
        self._set_rectangle()
        
    def _set_rectangle(self):
        self._rect = self.image.get_rect()
        self._rect.center = 24, 24

    def set_max_health(self, amount: int):
        self.max_health = amount

    def set_sp(self, amount):
        if amount > self.max_special_points:
            self.special_points = self.max_special_points
        else:
            self.special_points = amount

    def set_health(self, amount):
        if amount > self.max_health:
            self.health = self.max_health
        else:
            self.health = amount

    def get_health(self):
        return self.health
    
    def get_complete_hp(self):
        return f"{self.health}/{self.max_health}"
    
    def get_sp(self):
        return self.special_points
    
    def get_complete_sp(self):
        return f"{self.special_points}/{self.max_special_points}"

    def get_defense(self):
        return self.defense


class Flametorch(Creature):

    def __init__(self, level, image, name=""):
        super().__init__(level, 100, 35, 24, 10, [], name, "Fire")
        self.skills = []
        self.set_image(image)
        self.required_xp = 50 + (self.level - 1) * 50

    def level_up(self):
        self.xp = 0
        self.level += 1
        self.required_xp = 50 + (self.level - 1) * 50
        self.attack += 4
        self.defense += 2
        self.max_health += 15
        self.health = self.max_health
        self.max_special_points += 5
        self.special_points = self.max_special_points
        for idx, skill in enumerate(self.hidden_skills):
            if skill.get_req_level() <= self.level:
                self.skills.append(skill)
                self.hidden_skills.pop(idx)

    def check_for_level_up(self):
        if self.xp >= self.required_xp:
            self.level_up()

    def __str__(self):
        return f"Creature: {self.__class__.__name__}"


class Leafwing(Creature):
    
    def __init__(self, level, image, name):
        super().__init__(level, 110, 35, 23, 14, [], name, "Nature")
        self.skills = []
        self.set_image(image)
        self.required_xp = 50 + (self.level - 1) * 35
        
    def level_up(self):
        self.xp = 0
        self.level += 1
        self.required_xp = 50 + (self.level - 1) * 35
        self.attack += 3
        self.defense += 1
        self.max_health += 21
        self.health = self.max_health
        self.max_special_points += 7
        self.special_points = self.max_special_points
        for idx, skill in enumerate(self.hidden_skills):
            if skill.get_req_level() <= self.level:
                self.skills.append(self.hidden_skills.pop(idx))
                
    def check_for_level_up(self):
        if self.xp >= self.required_xp:
            self.level_up()

    def __str__(self):
        return f"Creature: {self.__class__.__name__}"


class Aquashade(Creature):

    def __init__(self, level, image, name):
        super().__init__(level, 95, 50, 27, 8, [], name, "Water")
        self.skills = []
        self.set_image(image)
        self.required_xp = 50 + (self.level - 1) * 45

    def level_up(self):
        self.xp = 0
        self.level += 1
        self.required_xp = 50 + (self.level - 1) * 35
        self.attack += 5
        self.defense += 1
        self.max_health += 14
        self.health = self.max_health
        self.max_special_points += 9
        self.special_points = self.max_special_points
        for idx, skill in enumerate(self.hidden_skills):
            if skill.get_req_level() <= self.level:
                self.skills.append(self.hidden_skills.pop(idx))

    def check_for_level_up(self):
        if self.xp >= self.required_xp:
            self.level_up()