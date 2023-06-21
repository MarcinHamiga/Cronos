class Status:
    def __init__(self, turns_left):
        self.turns_left = turns_left

    def __str__(self):
        return str(self.__class__.__name__)

    def decrement_turn(self):
        self.turns_left -= 1
        
    def extend_status(self, amount):
        self.turns_left += amount
        
    def get_turns_left(self):
        return self.turns_left

    def take_effect(self, host):
        pass

    
    
class Sleep(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

        
class Lower_attack(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

        
class Lower_defense(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)


class Aflame(Status):

    def __init__(self, turns_left):
        super().__init__(turns_left)

    def take_effect(self, host):
        host.take_damage(6)