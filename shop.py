import pygame

class Shopscreen:

    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT))
