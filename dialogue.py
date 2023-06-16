import pygame
from random import choice


class DialogueLine:
    def __init__(self, content: str, next_):
        self.content = content
        self._next = next_

    def set_next(self, next_):
        self._next = next_

    def get_next(self):
        return self._next

    def get_content(self):
        return self.content


class DialogueTree:

    def __init__(self, tree_name, starting_line):
        self.tree_name = tree_name
        self.current_line = starting_line
        self.__go_next = False

    def flip_go_to_next(self):
        self.__go_next = True

    def go_to_next(self):
        if self.__go_next:
            self.current_line = self.current_line.get_next()
            self.__go_next = False

    def get_content(self):
        return self.current_line.get_content()

    def get_current_line(self):
        return self.current_line

    def has_next(self):
        if self.current_line.get_next() is None:
            return False
        else:
            return True


class RadiantTree(DialogueTree):

    def __init__(self, tree_name: str, dialogue_list: list):
        super().__init__(tree_name, None)
        self.dialogue_list = dialogue_list

    def choose_random(self):
        self.current_line = choice(self.dialogue_list)
