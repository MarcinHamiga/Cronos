import random
import pygame
import pygame.freetype
from pathlib import Path
from time import time

from .state_manager import State_manager
from ..entities import Player, Brigitte, Thomas, Healer, Trader, Lavender, LockedDoor
from ..systems import Inventory, Shopscreen
from ..world import Dockersville
from ..ui import Menu, Settings


class Game:

    def __init__(self):

        pygame.init()
        pygame.freetype.init()
        self.CLOCK = pygame.time.Clock()
        screen_info = pygame.display.get_desktop_sizes()
        self.SCR_WIDTH, self.SCR_HEIGHT = screen_info[0][0], screen_info[0][1]
        self.SCREEN = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT))

        self._running = True

        self.game_state = "MENU"
        self.STATE_MANAGER = State_manager(self)

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
                try:
                    self.ASSETS[filename.upper()] = pygame.image.load(asset).convert_alpha()
                except pygame.error:
                    continue

        pygame.display.set_caption("Cronos")
        pygame.display.set_icon(self.ASSETS["ICN_CRONOS"])

        self.BRIGITTE = Brigitte(self.ASSETS)
        self.THOMAS = Thomas(self.ASSETS)
        self.HEALER = Healer(self.ASSETS)
        self.TRADER = Trader(self.ASSETS)
        self.LAVENDER = Lavender(self.ASSETS)
        self.LOCKEDDOOR = LockedDoor(self.ASSETS)

        self.PLAYER = Player(self.ASSETS["CHAR_BLUE_EYES_PERSON"], self.SCR_WIDTH // 2, self.SCR_HEIGHT // 2, [self.ASSETS["CHAR_JEANS"], self.ASSETS["CHAR_STRIPED_SHIRT"], self.ASSETS["CHAR_WHITERED_SNEAKERS"], self.ASSETS["CHAR_RED_FULLCAP"]])

        self.PLAYER.read_scale(self.scale)

        self.INVENTORY = Inventory(self)

        self.INVENTORY.add_item("Candy", 5)
        self.INVENTORY.add_item("Small HP Restore", 5)
        self.INVENTORY.add_item("Small SP Restore", 5)
        self.INVENTORY.add_item("HP restore", 5)
        self.INVENTORY.add_item("SP restore", 5)
        self.INVENTORY.add_item("Catcher", 5)
        self.INVENTORY.add_item("Junk", 10)

        self.map_surface = pygame.Surface((1, 1))
        self.map = Dockersville(self)

        self.SHOPSCREEN = Shopscreen(self)

        self.PLAYER.set_pos((360, 456))

        self.SETTINGS = Settings(self)

        self.main()

    def main(self):

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            match self.game_state:

                case "MENU":
                    self.menu_state()

                case "INVENTORY":
                    self.inventory_state()

                case "MAP":
                    self.map_state()

                case "SETTINGS":
                    self.settings_state()

                case "SHOP":
                    self.shop_state()

                case _:
                    self.map_state()

            self.flip_n_tick()

    def map_state(self):

        if not self.map.baked:
            self.map.bake_events()

        self.current_time = time()
        keys = pygame.key.get_pressed()

        if not self.map.in_dialogue:
            self.PLAYER.update(keys, self)

        self.map.update(keys, self)

        self.map_surface.fill((0, 0, 0))
        self.SCREEN.fill((0, 0, 0))
        self.map.draw_map()

    def inventory_state(self):

        self.current_time = time()
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_i] or keys[pygame.K_ESCAPE]) and self.current_time - self.func_key_used > \
                self.FUNC_KEY_COOLDOWN:
            self.STATE_MANAGER.change_state(3)
            self.func_key_used = self.current_time

        self.INVENTORY.update(keys)

        self.SCREEN.fill((0, 0, 0))

        self.INVENTORY.draw()

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
