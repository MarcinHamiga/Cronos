import pygame
import tkinter as tk
import sys
import os
from random import randint
import person

# Custom made modules
import map 


class Game:
    def __init__(self):
        root = tk.Tk()
        self._WIDTH, self._HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
        self.SCREEN = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.ASSETS = {}
        self.ASSET_CODES = {}
        self.MAP_ASSETS_PATH = os.path.join(os.path.dirname(os.pardir), "map_assets")
        self.map_assets_filenames = sorted(os.listdir(self.MAP_ASSETS_PATH))
        for filename in self.map_assets_filenames:
            asset_name = filename[:-4].upper()
            self.ASSETS[asset_name] = pygame.image.load(os.path.join(self.MAP_ASSETS_PATH, filename)).convert_alpha()
        
        counter = 0    
        for key in self.ASSETS.keys():
            self.ASSET_CODES[counter] = self.ASSETS[key]
            print(f"{key} - {counter}")
            counter += 1
            
        self.CHARACTER_ASSETS_PATH = os.path.join(os.path.dirname(os.pardir), "character_assets")    
        self.CHARACTER_ASSETS = {}
        self.character_assets_filenames = sorted(os.listdir(self.CHARACTER_ASSETS_PATH))
        for filename in self.character_assets_filenames:
            asset_name = filename[:-4].upper()
            self.CHARACTER_ASSETS[asset_name] = pygame.image.load(os.path.join(self.CHARACTER_ASSETS_PATH, filename)).convert_alpha()
        self.PLAYER = person.Player(self.CHARACTER_ASSETS["BLUE_EYES_PERSON"], 32, 32, [self.CHARACTER_ASSETS["JEANS"], self.CHARACTER_ASSETS["STRIPED_SHIRT"]]) 
        self.MAP = map.Map(34, 64, self.ASSET_CODES)
    
    def main(self):
        pygame.init()
        self._running = True

        while self._running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
        
            # Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                sys.exit(0)
            self.PLAYER.update(keys)
                
            # Draw
            self.MAP.draw_first_layer(self.SCREEN)
            self.MAP.draw_second_layer(self.SCREEN)
            self.PLAYER.draw(self.SCREEN)
            pygame.display.flip()
            