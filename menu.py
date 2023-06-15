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
        self.buttons = [Button("Play/Resume"), Button("Settings"), Button("Quit")]
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

        if keys[pygame.K_RETURN] and cur_time - self.last_click > self.click_cooldown:
            if self.game.MENU.current_button == 0:
                self.game.STATE_MANAGER.change_state(3)
            if self.game.MENU.current_button == 1:
                self.game.STATE_MANAGER.change_state("SETTINGS")
            if self.game.MENU.current_button == 2:
                pygame.quit()

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


class Settings:

    def __init__(self, game):
        self.game = game
        self.buttons = [Button("-", 80, 80), Button("+", 80, 80)]
        self.scale_surface = pygame.Surface((480, 80))
        self.scale_surface_rect = self.scale_surface.get_rect()
        self.scale_surface_rect.center = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 2
        self.is_adding = True

        self.last_click = time()
        self.cooldown = 0.15

    def draw(self):

        self.game.SCREEN.fill((0, 0, 0))
        surface, surface_rect = self.buttons[0].draw_button(self.game.FONT, not self.is_adding)
        surface_rect.center = self.game.SCR_WIDTH // 2 - 300, self.game.SCR_HEIGHT // 2
        self.game.SCREEN.blit(surface, surface_rect)

        surface, surface_rect = self.buttons[1].draw_button(self.game.FONT, self.is_adding)
        surface_rect.center = self.game.SCR_WIDTH // 2 + 300, self.game.SCR_HEIGHT // 2
        self.game.SCREEN.blit(surface, surface_rect)

        text, text_rect = self.game.FONT.render(f"Scale: {self.game.scale}", size=36, fgcolor=(255, 255, 255))
        self.scale_surface.fill((128, 0, 35))
        text_rect.center = 240, 40
        self.scale_surface.blit(text, text_rect)
        self.game.SCREEN.blit(self.scale_surface, self.scale_surface_rect)

    def update(self, keys):
        self._handle_input(keys)

    def _handle_input(self, keys):
        cur_time = time()

        if keys[pygame.K_RIGHT] and self.game.scale < 4 and cur_time - self.last_click > self.cooldown:
            self.game.scale += 1
            self.last_click = cur_time
            if not self.is_adding:
                self.is_adding = True

        if keys[pygame.K_LEFT] and self.game.scale > 1 and cur_time - self.last_click > self.cooldown:
            self.game.scale -= 1
            self.last_click = cur_time
            if self.is_adding:
                self.is_adding = False

