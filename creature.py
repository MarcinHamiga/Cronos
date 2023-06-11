from random import randint
import pygame

class Creature(pygame.sprite.Sprite):
    def __init__(self, level, health, special_points, attack, defense, name):
        self.image = None
        self.rect = None
        self.name = name
        self._is_down = False   # Zmienna oznaczająca że stworek jest niezdatny do walki
        self._is_defending = False  # Zmienna określająca czy w danej turze stworek broni się zwiększając swoją obronę
        self._level = level # Poziom stworka
        self._health = health
        self._max_health = health
        self._special_points = special_points
        self._max_special_points = special_points
        self._attack = attack
        self._defense = defense
        self._guard_bonus = int(defense * 0.2)
        self._statuses = []   # Lista zawierająca wszystkie nałożone na stworka statusy
        self._moves = []    # Lista ruchów dostępnych dla stworka
        self._hidden_moves = None # Lista ruchów które stworek odblokuje na kolejnych poziomach

    def attack(self, target):
        target_def = target.get_defense()
        # Jeżeli atak stworka jest większy niż obrona celu, ilość obrażeń losowana jest z pełnego przedziału od 0 do wartości ataku,
        # natomiast jeżeli atak stworka jest mniejszy niż obrona celu, obrażenia zostają zredukowane do 25% pierwotnej wartości
        damage = randint(0, self._attack)
        if self._attack > target_def:
            return target.take_damage(damage)
        else:
            return target.take_damage(damage // 4), damage
    
    def use_skill(self, skill, target):
        skill.use(target)
            
    def guard(self):
        self._defense += self._guard_bonus
        self._is_defending = True
        
    def end_guard(self):
        self._defense -= self._guard_bonus
        self._is_defending = False
    
    def check_if_down(self):
        if self._health <= 0:
            self._health = 0
            self._is_down = True
            
    def revive(self, revive_health = 1):
        self._is_down = False
        self._health = revive_health
        
    def take_damage(self, amount) -> int:
        if amount == 0:
            return 0
        self._health -= amount
        self.check_if_down()
        return 1
        
    def set_image(self, image):
        self._image = image
        self._set_rectangle()
    
    def _set_rectangle(self):
        self._rect = self._image.get_rect()
        self._rect.center = 24, 24
    
    def set_max_health(self, amount: int):
        self._max_health = amount
        
    def set_health(self, amount):
        if amount > self._max_health:
            self.health = self._max_health
        else:
            self.health = amount
    
    def get_health(self):
        return self._health
    
    def get_complete_hp(self):
        return f"{self._health}/{self._max_health}"
    
    def get_sp(self):
        return self._special_points
    
    def get_complete_sp(self):
        return f"{self._special_points}/{self._max_special_points}"
    

class Flametorch(Creature):
    def __init__(self, level, health, action_points, attack, defense, hidden_moves, name, image):
        super().__init__(level, health, action_points, attack, defense, name)
        self._hidden_moves = hidden_moves
        self.set_image(image)