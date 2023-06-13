from random import randint
import pygame


class Creature(pygame.sprite.Sprite):
    def __init__(self, level, health, special_points, attack, defense, name):
        super().__init__()
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
        self._moves = []    # Lista ruchów dostępnych dla stworka

    def apply_status(self, applied_status):

        for status in self._statuses:
            if status.__class__.__name__ == applied_status.__class__.__name__:
                status.extend_status(applied_status.turns_left)
                return

        self._statuses.append(status)

    def process_statuses(self):

        for idx, status in enumerate(self._statuses):
            status.take_effect(self)
            status.decrement_turn()
            if status.turns_left == 0:
                status.remove_effects(self)
                self._statuses.pop(idx)


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
        self.skill[idx].use(target)
            
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
        
    def set_image(self, image):
        self.image = image
        self._set_rectangle()
    
    def _set_rectangle(self):
        self._rect = self.image.get_rect()
        self._rect.center = 24, 24
    
    def set_max_health(self, amount: int):
        self.max_health = amount
        
    def set_health(self, amount):
        if amount > self.max_health:
            self.health = self.max_health
        else:
            self.health = amount

    def set_sp(self, amount):
        if amount > self.max_special_points:
            self.special_points = self.max_special_points
        else:
            self.special_points = amount

    def heal(self, amount):
        self.set_health(self.health + amount)

    def recover_sp(self, amount):
        self.set_sp(self.special_points + amount)

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

    def __init__(self, level, health, action_points, attack, defense, hidden_moves, name, image):
        super().__init__(level, health, action_points, attack, defense, name)
        self._hidden_moves = hidden_moves
        self.set_image(image)
        self.required_xp = 50 + (self.level - 1) * 50

    def level_up(self):
        self.xp = 0
        self._level += 1
        self.required_xp = 50 + (self.level - 1) * 50
        self.attack += 4
        self.defense += 2
        for move, idx in enumerate(self._hidden_moves):
            if move.required_level <= self.level:
                self.moves.append(self._hidden_moves.pop(idx))

    def __str__(self):
        return f"Creature: {self.__class__.__name__}"
