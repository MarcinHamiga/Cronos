import pygame
from pathlib import Path
from math import ceil

# Custom made modules
import map 
import person
import statemanager


class Game:
    def __init__(self):
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        screen_info = pygame.display.get_desktop_sizes()
        self.SCR_WIDTH, self.SCR_HEIGHT = screen_info[1][0], screen_info[1][1]
        self.SCREEN = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT)) 
        self._running = True
                
        self.game_state = "MENU"
        self.STATE_MANAGER = statemanager.State_manager(self)
        self.STATE_MANAGER.change_state(0)
        self.CURRENT_MAP = "testmap"
        
        self.ASSETS = {}
        self.PATH_TO_ASSETS = Path(Path.cwd()) / Path("assets")
        for asset in self.PATH_TO_ASSETS.iterdir():
            if asset.is_file():
                filename = asset.name[:-4]
                print(filename)
                self.ASSETS[filename.upper()] = pygame.image.load(asset).convert_alpha()
            
        self.PLAYER = person.Player(self.ASSETS["CHAR_BLUE_EYES_PERSON"], self.SCR_WIDTH // 2, self.SCR_HEIGHT // 2, [self.ASSETS["CHAR_JEANS"], self.ASSETS["CHAR_STRIPED_SHIRT"]])
        
        self.NUMBERED_ASSETS = {}
        count = 0
        for asset in self.ASSETS.values():
            self.NUMBERED_ASSETS[count] = asset
            count += 1

        self.MAP = map.Map(self.SCR_WIDTH, self.SCR_HEIGHT)
        self.MAP.load_map(self.CURRENT_MAP)
        self.PLAYER.set_pos((32, 0))
        self.main()

            
    def main(self):
        while self._running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit

            match (self.game_state):
                
                case "TEST":
                    self.map_state()
                    
                case "MENU":
                    self.menu_state()
                    
                case "INVENTORY":
                    self.inventory_state()
                    
                case "MAP":
                    self.map_state()
                    
                case _:
                    self.map_state()
    
    def map_state(self):
            # Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
            map_width, map_height = self.MAP.get_map_size()
            self.PLAYER.update(keys, map_width, map_height)
                
            # Draw
            self.SCREEN.fill((0,0,0))
            self.MAP.draw_map(self.SCREEN, self.PLAYER)
            pygame.display.flip()
            self.CLOCK.tick(60)
            
    def inventory_state(self):
        pass
    
    def menu_state(self):
        pass