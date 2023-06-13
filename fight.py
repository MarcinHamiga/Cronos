import pygame
from time import time, sleep
from inventory import Item_card


class FightScreen:
    def __init__(self, game):

        self.game = game
        self.current_command = 1
        self.player_creature = game.PLAYER.creatures[game.PLAYER.designated_creature]
        self.enemy_creature = None
        self.player_creature_stats = PlayerCreatureStats(game)
        self.enemy_creature_stats = EnemyCreatureStats(game, self.enemy_creature)
        self.player_action_menu = PlayerActionMenu(game)
        self.action_log = ActionLog(game)
        self.last_key_press = time()
        self.cooldown = 0.1
        self.player_turn = True

    def set_enemy(self, enemy):
        self.enemy_creature = enemy
        self.enemy_creature_stats.creature = self.enemy_creature

    def _handle_input(self, keys):
        cur_time = time()

        if keys[pygame.K_DOWN] and self.current_command < 4 and cur_time - self.last_key_press > self.cooldown:
            self.current_command += 1
            self.last_key_press = cur_time

        if keys[pygame.K_UP] and self.current_command > 1 and cur_time - self.last_key_press > self.cooldown:
            self.current_command -= 1
            self.last_key_press = cur_time

        if keys[pygame.K_SPACE] and cur_time - self.last_key_press > self.cooldown and self.player_turn:
            match self.current_command:
                case 1:
                    self.turn()
            self.last_key_press = cur_time

    def update(self, keys):
        self._handle_input(keys)
        if not self.player_turn and self.enemy_creature is not None:
            self.turn()

    def switch_turns(self):
        if self.player_turn:
            self.player_turn = False
        else:
            self.player_turn = True

    def turn(self):
        cur_time = time()
        if self.current_command == 1:
            if self.player_turn:
                self.player_attack()
                self.switch_turns()
                self.time_of_player_turn = time()

        if not self.player_turn and cur_time - self.time_of_player_turn > 1.5:
            self.enemy_attack()
            self.switch_turns()

        if self.player_creature.check_if_down() or self.enemy_creature.check_if_down():
            self.game.STATE_MANAGER.change_state(3)
            self.enemy_creature = None
            self.enemy_creature_stats.creature = self.enemy_creature

    def player_attack(self):
        reaction = self.player_creature.attack_target(self.enemy_creature)
        self.action_log.get_action("attack", reaction, self.player_creature)

    def enemy_attack(self):
        reaction = self.enemy_creature.attack_target(self.player_creature)
        self.action_log.get_action("attack", reaction, self.enemy_creature)


    def draw(self):

        self.game.SCREEN.fill((0, 0, 0))
        self.player_creature_stats.draw()
        self.enemy_creature_stats.draw()
        self.player_action_menu.draw()
        self.action_log.draw()

        surface, surface_rect = self.player_creature_stats.get_surface_rect()
        self.game.SCREEN.blit(surface, surface_rect)

        surface, surface_rect = self.enemy_creature_stats.get_surface_rect()
        self.game.SCREEN.blit(surface, surface_rect)

        surface, surface_rect = self.player_action_menu.get_surface_rect()
        self.game.SCREEN.blit(surface, surface_rect)

        surface, surface_rect = self.action_log.get_surface_rect()
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
        self.surface.fill((128, 0, 35))
        crt_name, crt_name_rect = self.game.FONT.render(f"{self.creature.__class__.__name__}", size=40)
        crt_name_rect.center = self.surface_rect.w // 2, 25
        crt_hp, crt_hp_rect = self.game.FONT.render(f"HP {self.creature.get_complete_hp()}", size=36)
        crt_hp_rect.center = self.surface_rect.w // 2, 75
        crt_sp, crt_sp_rect = self.game.FONT.render(f"SP {self.creature.get_complete_sp()}", size=36)
        crt_sp_rect.center = self.surface_rect.w // 2, 125

        self.surface.blit(crt_name, crt_name_rect)
        self.surface.blit(crt_hp, crt_hp_rect)
        self.surface.blit(crt_sp, crt_sp_rect)

    def get_surface_rect(self):
        return self.surface, self.surface_rect


class EnemyCreatureStats:

    def __init__(self, game, enemy):

        self.game = game
        self.creature = enemy
        self.surface = pygame.Surface((240, 150))
        self.surface.fill((128, 0, 35))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = game.SCR_WIDTH - 120, 75

    def draw(self):
        if self.creature is not None:
            self.surface.fill((128, 0, 35))
            crt_name, crt_name_rect = self.game.FONT.render(f"{self.creature.__class__.__name__}", size=40)
            crt_name_rect.center = self.surface_rect.w // 2, 25
            crt_hp, crt_hp_rect = self.game.FONT.render(f"HP {self.creature.get_complete_hp()}", size=36)
            crt_hp_rect.center = self.surface_rect.w // 2, 75
            crt_sp, crt_sp_rect = self.game.FONT.render(f"SP {self.creature.get_complete_sp()}", size=36)
            crt_sp_rect.center = self.surface_rect.w // 2, 125

            self.surface.blit(crt_name, crt_name_rect)
            self.surface.blit(crt_hp, crt_hp_rect)
            self.surface.blit(crt_sp, crt_sp_rect)

    def get_surface_rect(self):
        return self.surface, self.surface_rect


class PlayerActionMenu:

    def __init__(self, game):

        self.game = game
        self.surface = pygame.Surface((200, 200))
        self.activated_color = (160, 160, 160)
        self.background_color = (128, 0, 35)
        self.surface.fill(self.background_color)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = 100, game.SCR_HEIGHT - 100

    def draw(self):
        self.surface.fill((128, 0, 35))
        if self.game.FIGHTSCREEN.current_command == 1:
            attack, attack_rect = self.game.FONT.render("Attack", size=40, bgcolor=self.activated_color)
        else:
            attack, attack_rect = self.game.FONT.render("Attack", size=40, bgcolor=self.background_color)
        attack_rect.center = self.surface_rect.w // 2, 25

        if self.game.FIGHTSCREEN.current_command == 2:
            skill, skill_rect = self.game.FONT.render("Skill", size=40, bgcolor=self.activated_color)
        else:
            skill, skill_rect = self.game.FONT.render("Skill", size=40, bgcolor=self.background_color)
        skill_rect.center = self.surface_rect.w // 2, 75

        if self.game.FIGHTSCREEN.current_command == 3:
            item, item_rect = self.game.FONT.render("Item", size=40, bgcolor=self.activated_color)
        else:
            item, item_rect = self.game.FONT.render("Item", size=40, bgcolor=self.background_color)
        item_rect.center = self.surface_rect.w // 2, 125

        if self.game.FIGHTSCREEN.current_command == 4:
            run, run_rect = self.game.FONT.render("Run", size=40, bgcolor=self.activated_color)
        else:
            run, run_rect = self.game.FONT.render("Run", size=40, bgcolor=self.background_color)
        run_rect.center = self.surface_rect.w // 2, 175

        self.surface.blit(attack, attack_rect)
        self.surface.blit(skill, skill_rect)
        self.surface.blit(item, item_rect)
        self.surface.blit(run, run_rect)

    def get_surface_rect(self):
        return self.surface, self.surface_rect


class ActionLog:

    def __init__(self, game):
        self.game = game
        self.action = None
        self.reaction = None
        self.creature = None
        self.surface = pygame.Surface((game.SCR_WIDTH - 240, 100))
        self.surface_rect = self.surface.get_rect()
        self.surface.fill((70, 70, 70))

    def get_action(self, action, reaction, creature):
        self.action = action
        self.reaction = reaction
        self.creature = creature

    def draw(self):
        self.surface.fill((70, 70, 70))
        if self.action is not None:
            action, action_rect = self.game.FONT.render(f"{self.creature.__class__.__name__} uses {self.action}...", size=40)
            action_rect.center = self.surface_rect.w // 2, 25
            if self.reaction == 0:
                reaction, reaction_rect = self.game.FONT.render(f"It's ineffective!")
            else:
                reaction, reaction_rect = self.game.FONT.render(f"It deals {self.reaction} dmg!", size=40)
            reaction_rect.center = self.surface_rect.w // 2, 75

            self.surface.blit(action, action_rect)
            self.surface.blit(reaction, reaction_rect)

    def get_surface_rect(self):
        return self.surface, self.surface_rect


class ContentList:

    def __init__(self, game):
        self.game = game
        self.items = game.PLAYER.items
        self.item_cards
        # self.skills = game.PLAYER.creatures[game.PLAYER.designated_creature].moves
        self.surface = pygame.Surface(())

    def draw(self):
        pass