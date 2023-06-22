import pygame
from random import choice


class DialogueLine:
    def __init__(self, content: str, next_):
        self.content = content
        self._next = next_  # Następna linia dialogowa. Jeżeli brak, przyjąć None

    def set_next(self, next_):
        """Ustawia następną linię dialogową"""
        # Ta funkcja obecnie nie ma specjalnie zastosowania, powstała na wypadek
        # gdyby zostało mi wystarczająco czasu na dodanie drzew dialogowych i wyborów w dialogach
        self._next = next_

    def get_next(self):
        """Zwraca następną linię dialogową"""
        return self._next

    def get_content(self):
        """Zwraca nam łańcuch znakowy, który będzie wypisany na ekranie w czasie dialogu"""
        return self.content


class DialogueTree:

    def __init__(self, tree_name, starting_line):
        self.tree_name = tree_name
        self.current_line = starting_line
        self._go_next = False

    def flip_go_to_next(self):
        """Zmienia zmienną prywatną zmienną _go_next na True, co oznacza, ze dialog może iść dalej"""
        self._go_next = True

    def go_to_next(self):
        """Służy do progresji dialogu. Zmienia obecną linię dialogową na następną linię"""
        if self._go_next:
            self.current_line = self.current_line.get_next()
            self._go_next = False

    def get_content(self):
        """Wywołuje funkcję get_content obecnej linii dialogowej."""
        return self.current_line.get_content()

    def get_current_line(self):
        """Zwraca obiekt obecnej linii dialogowej"""
        return self.current_line

    def has_next(self):
        """Sprawdza czy obecna linia dialogowa posiada następną linię"""
        if self.current_line.get_next() is None:
            return False
        else:
            return True


class RadiantTree(DialogueTree):

    def __init__(self, tree_name: str, dialogue_list: list):
        super().__init__(tree_name, None)
        self.dialogue_list = dialogue_list

    def choose_random(self):
        """Funkcja ta losuje z listy dialogue_list linię dialogową, która zostanie zwrócona"""
        self.current_line = choice(self.dialogue_list)
