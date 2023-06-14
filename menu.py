import pygame
from time import time

class Button:

    def __init__(self, text, w=480, h=240):
        self.surface = pygame.Surface((w, h))
        self.surface_rect = self.surface.get_rect()
        self.text = text

    def set_center(self, x, y):
        self.surface_rect.center = x, y

    def draw_button(self, font, active=False):
        if active:
            surface, surface_rect = font.render(self.text, fgcolor=(0, 0, 0), size=48)
            surface_rect.center = self.surface_rect.w // 2, self.surface_rect.h // 2
            self.surface.fill((255, 255, 255))
            self.surface.blit(surface, surface_rect)
            return self.surface, self.surface_rect
        else:
            surface, surface_rect = font.render(self.text, fgcolor=(255, 255, 255), size=48)
            surface_rect.center = self.surface_rect.w // 2, self.surface_rect.h // 2
            self.surface.fill((128, 0, 35))
            self.surface.blit(surface, surface_rect)
            return self.surface, self.surface_rect


class Menu:

    def __init__(self, game):
        self.game = game
        self.buttons = [Button("Play/Resume"), Button("Load"), Button("Quit")]
        self.odd = bool(len(self.buttons) % 2)
        self.current_button = 0
        self.click_cooldown = 0.2
        self.last_click = time()

        if self.odd:
            offset = len(self.buttons) // 2 * (self.buttons[0].surface_rect.h + 40)
        else:
            offset = len(self.buttons) // 2 * (self.buttons[0].surface_rect.h + 20)
        w, h = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 2
        for button in self.buttons:
            button.surface_rect.center = w, h - offset
            if self.odd:
                offset -= self.buttons[0].surface_rect.h + 40
            else:
                offset -= self.buttons[0].surface_rect.h + 20

    def update(self, keys):

        cur_time = time()

        if keys[pygame.K_DOWN] and self.current_button < len(self.buttons) - 1 and cur_time - self.last_click > self.click_cooldown:
            self.current_button += 1
            self.last_click = cur_time
        if keys[pygame.K_UP] and self.current_button > 0 and cur_time - self.last_click > self.click_cooldown:
            self.current_button -= 1
            self.last_click = cur_time

    def draw(self):
        self.game.SCREEN.fill((0, 0, 0))
        count = 0
        for button in self.buttons:
            if count == self.current_button:
                surface, surface_rect = button.draw_button(self.game.FONT, True)
                self.game.SCREEN.blit(surface, surface_rect)
            else:
                surface, surface_rect = button.draw_button(self.game.FONT, False)
                self.game.SCREEN.blit(surface, surface_rect)
            count += 1

