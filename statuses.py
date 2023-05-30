class Status:
    def __init__(self, turns_left):
        self._turns_left = turns_left
        
    def decrement_turn(self):
        self._turns_left -= 1
        
    def extend_status(self, amount):
        self._turns_left += amount
        
    def get_turns_left(self):
        return self._turns_left
    
    
class Sleep(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)
        
        
class Confusion(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

        
class Lower_attack(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

        
class Lower_defense(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)