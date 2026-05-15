class Status:
    def __init__(self, turns_left):
        self.turns_left = turns_left

    def __str__(self):
        return str(self.__class__.__name__)

    def decrement_turn(self):
        """Odejmuje jedną turę z pozostałego czasu"""
        self.turns_left -= 1
        
    def extend_status(self, amount):
        """Wydłuża status o zadaną wartość"""
        self.turns_left += amount
        
    def get_turns_left(self):
        """Zwraca pozostałą ilość tur"""
        return self.turns_left

    def take_effect(self, host):
        """Jest to funkcja, którą należy nadpisać w zależności od potrzeb danego statusu."""
        pass


# Te statusy miały zostać wykorzystane, jednak zabrakło mi czasu na ich implementację
class Sleep(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

        
class Lower_attack(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

        
class Lower_defense(Status):
    def __init__(self, turns_left):
        super().__init__(turns_left)

# Ten status jest wykorzystywany w czasie gry
class Aflame(Status):

    def __init__(self, turns_left):
        super().__init__(turns_left)

    def take_effect(self, host):
        host.take_damage(6)