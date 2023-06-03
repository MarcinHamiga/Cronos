import pygame
from pathlib import Path

# Custom made modules
import map 
import person
import statemanager


class Game:
    def __init__(self):
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        screen_info = pygame.display.Info()
        self.SCR_WIDTH = screen_info.current_w
        self.SCR_HEIGHT = screen_info.current_h
        self.SCREEN = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT)) 
        self._running = True
        
        self.SCALE = min(self.SCR_WIDTH // 32, self.SCR_HEIGHT // 32)
        self.SURFACE = pygame.Surface((32*32, 32*32))
        self.SCALED_GAME_SURFACE = pygame.transform.scale(self.SURFACE, (self.SCALE * 32, self.SCALE * 32))
        self.SCALED_DISPLAY = pygame.Surface((self.SCR_WIDTH, self.SCR_HEIGHT))
                
        self.game_state = "MENU"
        self.STATE_MANAGER = statemanager.State_manager(self)
        self.STATE_MANAGER.change_state(0)
        
        self.ASSETS = {}
        self.PATH_TO_ASSETS = Path(Path.cwd()) / Path("assets")
        for asset in self.PATH_TO_ASSETS.iterdir():
            filename = asset.name[:-4]
            print(filename)
            self.ASSETS[filename.upper()] = pygame.image.load(asset).convert_alpha()
            self.ASSETS[filename.upper()] = pygame.transform.scale(self.ASSETS[filename.upper()], (128, 128))
            
        self.PLAYER = person.Player(self.ASSETS["CHAR_BLUE_EYES_PERSON"], 64, 64, [self.ASSETS["CHAR_JEANS"], self.ASSETS["CHAR_STRIPED_SHIRT"]])
        
        self.NUMBERED_ASSETS = {}
        count = 0
        for asset in self.ASSETS.values():
            self.NUMBERED_ASSETS[count] = asset
            count += 1


        
        self.camera_pos = self.PLAYER.get_pos()
        self.MAP = map.Map("testmap.pkl", self.PLAYER, self.NUMBERED_ASSETS)
        self.main()
            
    def main(self):
        while self._running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit

            # Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
            self.PLAYER.update(keys)
                
            # Draw
            self.PLAYER.draw(self.SCREEN)
            self.SCREEN.blit(self.MAP)
            pygame.display.flip()
            self.CLOCK.tick(60)
            