import pygame

class FightScreen:
    def __init__(self, game):
        self.game = game
        self.current_command = 0

    def _handle_input(self, keys):
        if keys[pygame.K_DOWN] and self.current_command < 4:
            self.current_command += 1
        if keys[pygame.K_UP] and self.current_command > 0:
            self.current_command -= 1
    def update(self, keys):


    def draw(self, surface):
        pass


class PlayerCreatureStats:

    def __int__(self, game):
        self.game = game
        self.creature = game.PLAYER.creatures[game.PLAYER.designated_creature]
        self.surface = pygame.Surface((240, 160))
        self.surface.fill((128, 0, 35))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = 270, game.SCR_HEIGHT - 80

    def draw(self):
        crt_name, crt_name_rect = self.game.FONT.render(f"{self.creature.__class__.__name__}", size=40)
        crt_hp, crt_hp_rect = self.game.FONT.render(f"{self.creature.get_complete_hp()}", size=36)
        crt_sp, crt_sp_rect = self.game.FONT.render(f"{self.creature.get_complete_sp()}", size=36)



class EnemyCreatureStats:

    def __init__(self, game):
        pass


class PlayerActionMenu:

    def __init__(self, game):
        pass


class ActionLog:

    def __init__(self, game):
        pass
