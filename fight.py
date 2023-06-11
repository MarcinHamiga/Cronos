import pygame


class FightScreen:
    def __init__(self, game):
        self.game = game
        self.current_command = 0
        self.player_creature_stats = PlayerCreatureStats(game)
        self.enemy_creature_stats = EnemyCreatureStats(game)
        self.player_action_menu = PlayerActionMenu(game)
        self.action_log = ActionLog(game)

    def _handle_input(self, keys):
        if keys[pygame.K_DOWN] and self.current_command < 4:
            self.current_command += 1
        if keys[pygame.K_UP] and self.current_command > 0:
            self.current_command -= 1

    def update(self, keys):
        self._handle_input(keys)

    def draw(self):
        self.game.SCREEN.fill((0,0,0))
        self.player_creature_stats.draw()
        surface, surface_rect = self.player_creature_stats.get_surface_rect()
        self.game.SCREEN.blit(surface, surface_rect)


class PlayerCreatureStats:

    def __init__(self, game):
        self.game = game
        self.creature = game.PLAYER.creatures[game.PLAYER.designated_creature]
        self.surface = pygame.Surface((240, 150))
        self.surface.fill((128, 0, 35))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = 320, game.SCR_HEIGHT - 75

    def draw(self):
        crt_name, crt_name_rect = self.game.FONT.render(f"{self.creature.__class__.__name__}", size=40)
        crt_name_rect.center = 120, 25
        crt_hp, crt_hp_rect = self.game.FONT.render(f"HP {self.creature.get_complete_hp()}", size=36)
        crt_hp_rect.center = 120, 75
        crt_sp, crt_sp_rect = self.game.FONT.render(f"SP {self.creature.get_complete_sp()}", size=36)
        crt_sp_rect.center = 120, 125

        self.surface.blit(crt_name, crt_name_rect)
        self.surface.blit(crt_hp, crt_hp_rect)
        self.surface.blit(crt_sp, crt_sp_rect)

    def get_surface_rect(self):
        return self.surface, self.surface_rect

class EnemyCreatureStats:

    def __init__(self, game):
        pass


class PlayerActionMenu:

    def __init__(self, game):
        pass


class ActionLog:

    def __init__(self, game):
        pass
