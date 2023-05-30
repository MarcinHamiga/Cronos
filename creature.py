from random import randint

class Creature:
    def __init__(self, level, health, action_points, attack, defense):
        self._is_down = False
        self._is_defending = False
        self._level = level
        self._health = health
        self._max_health = health
        self._action_points = action_points
        self._attack = attack
        self._defense = defense
        self._guard_bonus = int(defense * 0.2)
        self._statuses = []
        self._moves = []
        self._hidden_moves = []

    def attack(self, target):
        target_def = target.get_defense()
        target_agi = target.get_agility()
        if self._attack > target_def:
            return target.take_damage(randint(0, self._attack))
        elif self._attack < target_def:
            damage = self._attack - target_def
            if damage < 0:
                damage = 0
            return target.take_damage(randint(self._attack - target_def))
    
    def use_skill(self, skill, target):
        skill.
            
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
        
        

class Flametorch(Creature):
    def __init__(self, level, health, action_points, attack, defense, hidden_moves):
        super().__init__(level, health, action_points, attack, defense)
        self._hidden_moves = hidden_moves