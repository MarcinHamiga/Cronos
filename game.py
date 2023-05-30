import pygame
import tkinter as tk
import sys
import os
from random import randint

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
        self.PATH = os.path.join(os.pardir, "assets")
        self.filenames = sorted(os.listdir("C:/Users/marci/Documents/GitHub/Cronos/assets"))
        for filename in self.filenames:
            asset_name = filename[:-4].upper()
            self.ASSETS[asset_name] = pygame.image.load(os.path.join("C:/Users/marci/Documents/GitHub/Cronos/assets", filename)).convert_alpha()
        
        counter = 0    
        for key in self.ASSETS.keys():
            self.ASSET_CODES[counter] = self.ASSETS[key]
            print(f"{key} - {counter}")
            counter += 1
            
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
                
            # Draw
            self.MAP.draw_map(self.SCREEN)
            pygame.display.flip()
            