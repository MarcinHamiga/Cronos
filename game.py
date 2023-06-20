import random

import pygame
from pathlib import Path
from time import time

# Custom made modules
import map
import menu
import person
import statemanager
import inventory
import creature
import fight
import skills
from menu import Menu
from shop import Shopscreen


class Game:
    
    def __init__(self):
        
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        screen_info = pygame.display.get_desktop_sizes()
        self.SCR_WIDTH, self.SCR_HEIGHT = screen_info[0][0], screen_info[0][1]
        self.SCREEN = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT))

        self._running = True

        self.game_state = "MENU"
        self.STATE_MANAGER = statemanager.State_manager(self)
        self.STATE_MANAGER.change_state(3)

        self.MENU = Menu(self)

        self.FUNC_KEY_COOLDOWN = 0.2
        self.func_key_used = time()
        self.current_time = self.func_key_used

        self.scale = 1

        self.FONT = pygame.freetype.Font(Path.cwd() / Path("fonts") / Path ("VCR_OSD_MONO_1.001.ttf"), 16)
        self.ASSETS = {}
        self.PATH_TO_ASSETS = Path(Path.cwd()) / Path("assets")

        for asset in self.PATH_TO_ASSETS.iterdir():
            if asset.is_file():
                filename = asset.name[:-4]
                self.ASSETS[filename.upper()] = pygame.image.load(asset).convert_alpha()

        pygame.display.set_caption("Cronos")
        pygame.display.set_icon(self.ASSETS["ICN_CRONOS"])
        self.SKILLS_DICT = skills.SkillDict(self.ASSETS)


        # NPC
        self.BRIGITTE = person.Brigitte(self)
        self.THOMAS = person.Thomas(self)
        self.HEALER = person.Healer(self)
        self.TRADER = person.Trader(self)
        self.LAVENDER = person.Lavender(self)

        # Sekcja dotycząca gracza
        self.PLAYER = person.Player(self.ASSETS["CHAR_BLUE_EYES_PERSON"], self.SCR_WIDTH // 2, self.SCR_HEIGHT // 2, [self.ASSETS["CHAR_JEANS"], self.ASSETS["CHAR_STRIPED_SHIRT"], self.ASSETS["CHAR_WHITERED_SNEAKERS"], self.ASSETS["CHAR_RED_FULLCAP"]])

        self.PLAYER.read_scale(self.scale)

        self.PLAYER.add_creature(self.spawn_aquashade(2))
        self.PLAYER.add_creature(self.spawn_flametorch(5))
        self.PLAYER.add_creature(self.spawn_leafwing(5))
        self.PLAYER.add_creature(self.spawn_flametorch(10))
        self.PLAYER.set_designated_creature(0)

        # Sekcja dotycząca ekwipunku
        self.INVENTORY = inventory.Inventory(self)
        
        self.INVENTORY.add_item("Candy", 5)
        self.INVENTORY.add_item("Small HP Restore", 5)
        self.INVENTORY.add_item("Small SP Restore", 5)
        self.INVENTORY.add_item("HP restore", 5)
        self.INVENTORY.add_item("SP restore", 5)
        self.INVENTORY.add_item("Catcher", 5)
        self.INVENTORY.add_item("Junk", 10)

        # Sekcja inicjalizująca ekran walki
        self.FIGHTSCREEN = fight.FightScreen(self)

        # Sekcja inicjalizująca mapę
        self.map_surface = pygame.Surface((1, 1))
        self.map = map.TestMap(self)

        # Sekcja inicjalizująca ekran sklepu
        self.SHOPSCREEN = Shopscreen(self)

        count = 0

        self.PLAYER.set_pos((48, 192))

        self.SETTINGS = menu.Settings(self)

        self.main()

    def main(self):
        
        while self._running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            match self.game_state:
                
                case "TEST":
                    self.map_state()
                    
                case "MENU":
                    self.menu_state()
                    
                case "INVENTORY":
                    self.inventory_state()
                    
                case "MAP":
                    self.map_state()

                case "FIGHT":
                    if self.FIGHTSCREEN.enemy_creature is None:
                        self.FIGHTSCREEN.set_enemy(self.spawn_flametorch(random.randint(1, 5)))
                    self.fight_state()

                case "SETTINGS":
                    self.settings_state()

                case "SHOP":
                    self.shop_state()

                case _:
                    self.map_state()
            
            self.flip_n_tick()
    
    def map_state(self):
        
        # Input
        if not self.map.baked:
            self.map.bake_events()
        
        self.current_time = time()
        keys = pygame.key.get_pressed()

        if not self.map.in_dialogue:
            self.PLAYER.update(keys, self)

        self.map.update(keys, self)
        
        # Draw
        self.map_surface.fill((0, 0, 0))
        self.SCREEN.fill((0, 0, 0))
        self.map.draw_map()
            
    def inventory_state(self):
        
        # Input
        self.current_time = time()
        keys = pygame.key.get_pressed()    
        
        if (keys[pygame.K_i] or keys[pygame.K_ESCAPE]) and self.current_time - self.func_key_used > \
                self.FUNC_KEY_COOLDOWN:
            self.STATE_MANAGER.change_state(3)
            self.func_key_used = self.current_time

        self.INVENTORY.update(keys)
        
        # Draw    
        self.SCREEN.fill((0, 0, 0))

        self.INVENTORY.draw()

    def fight_state(self):

        self.FIGHTSCREEN.content_list.refresh()
        self.current_time = time()
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_f] and self.current_time - self.func_key_used > self.FUNC_KEY_COOLDOWN:
        #     self.game_state = self.STATE_MANAGER.change_state(3)
        #     self.func_key_used = self.current_time
        #     self.FIGHTSCREEN.action_log.clear_log()

        # Input
        self.FIGHTSCREEN.update(keys)

        # Draw
        self.FIGHTSCREEN.draw()

    def menu_state(self):

        self.current_time = time()
        keys = pygame.key.get_pressed()

        self.MENU.update(keys)

        self.MENU.draw()

    def settings_state(self):

        self.current_time = time()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and self.current_time - self.func_key_used > self.FUNC_KEY_COOLDOWN:
            self.STATE_MANAGER.change_state("MENU")
            self.func_key_used = self.current_time

        self.SETTINGS.update(keys)

        self.SETTINGS.draw()

    def shop_state(self):
        self.current_time = time()
        keys = pygame.key.get_pressed()
        self.SHOPSCREEN.set_for_refresh()
        self.SHOPSCREEN.refresh()

        if keys[pygame.K_c] or keys[pygame.K_BACKSPACE]:
            self.STATE_MANAGER.change_state(3)

        self.SHOPSCREEN.update(keys)

        self.SHOPSCREEN.draw()

    def flip_n_tick(self, fps=60):
        pygame.display.flip()
        self.CLOCK.tick(fps)

    # Funkcje do zarządzania contentem

    def spawn_flametorch(self, level=1, name=""):
        creature_ = creature.Flametorch(1, self.ASSETS["CRT_FLAMETORCH"], name)

        creature_.add_hidden_skill(self.SKILLS_DICT.get_skill("FIREBREATH"))
        creature_.add_hidden_skill(self.SKILLS_DICT.get_skill("FIREWHIP"))

        if level > 1:
            for x in range(level - 1):
                creature_.level_up()
        return creature_

    def spawn_leafwing(self, level=1, name=""):
        creature_ = creature.Leafwing(1, self.ASSETS["CRT_LEAFWING"], name)
        creature_.add_hidden_skill(self.SKILLS_DICT.get_skill("WHIRLWIND"))

        if level > 1:
            for x in range(level - 1):
                creature_.level_up()
        return creature_

    def spawn_aquashade(self, level=1, name=""):
        creature_ = creature.Aquashade(1, self.ASSETS["CRT_AQUASHADE"], name)
        creature_.add_hidden_skill(self.SKILLS_DICT.get_skill("WATERBLAST"))

        if level > 1:
            for x in range(level - 1):
                creature_.level_up()

        return creature_

