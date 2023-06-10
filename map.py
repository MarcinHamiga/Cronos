import pygame
import pytmx
from pathlib import Path
from time import time

import person
import creature

class Event:
    
    def __init__(self, cx, cy, w = 48, h = 48, img = None):
        if img is not None:
            self.image = img
        else:
            self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        
    # Wszystkie poniższe funkcje powinny, ale nie muszą zostać przeciążone 
    def check_stepped_on(self, game):
        pass
    
    def check_interact(self, game):
        pass


class Teleport(Event):
    
    def __init__(self, cx, cy, place_on_map: tuple, map = None, img = None):
        super().__init__(cx, cy, img=img)
        self.dest_map = map
        self.map_coords = place_on_map

    def teleport(self, game):
        game.PLAYER.set_pos(self.map_coords)
        print(f"Teleported player to {self.map_coords}")
        if self.dest_map is not None:
            game.map = self.dest_map

    def check_stepped_on(self, game):
        # x, y = self.original_center
        # self.
        if self.rect.colliderect(game.PLAYER.get_rectangle()):
            self.teleport(game)
            
class Dialogue(Event):
    
    def __init__(self, dictionary):
        self.DIALOGUE_DICT = dictionary

class Fight(Event):
    pass

        
class Tile:
    def __init__(self, image, rect, impassable, size, x, y):
        self.image = image
        self.rect = rect
        self.size = size
        self.x = x + 1
        self.y = y + 1
        self.rect.center = x * self.size[0] + 24, y * self.size[1] + 24
        self.impassable = impassable
        self.width_pos = (self.rect.x - (self.size[0] // 2), self.rect.x + (self.size[0] // 2))
        self.height_pos = (self.rect.y - (self.size[1] // 2), self.rect.y + (self.size[1] // 2))
        self.events = []
        
    def add_event(self, event):
        self.events.append(event)


class Map:
    def __init__(self):
        self.tmx_map_data = None
        self.map_width = None
        self.map_height = None
        self.last_press = time()
        self.cooldown = 0.25
        self.baked = 0
        self.scale = 1
        
    def load_map(self, mapname):
        
        if mapname[:-4] != ".tmx":
            mapname += ".tmx"
            
        map_path = Path.cwd()
        map_path /= Path(f"maps/{mapname.lower()}")
        self.tmx_map_data = pytmx.load_pygame(map_path)
        self.layers = []
        layer_num = 0
        
        for layer in self.tmx_map_data:
            self.layers.append([])
            
            if isinstance(layer, pytmx.TiledTileLayer):
                
                for x, y, gid in layer:
                    image = self.tmx_map_data.get_tile_image_by_gid(gid)
                    if image is not None:
                        impassable = self.tmx_map_data.get_tile_properties_by_gid(gid)["impassable"]
                        rect = image.get_rect()
                        tile = Tile(image, rect, impassable, (self.tmx_map_data.tilewidth, self.tmx_map_data.tileheight), x ,y)
                        self.layers[layer_num].append(tile)
                        
            layer_num += 1
        
    def _handle_input(self, keys_pressed, game):
        cur_time = time()
        if keys_pressed[pygame.K_1] and game.scale < 4 and cur_time - self.last_press > self.cooldown:
            game.scale += 1
            self.last_press = cur_time
        if keys_pressed[pygame.K_2] and game.scale > 1 and cur_time - self.last_press > self.cooldown:
            game.scale -= 1
            self.last_press = cur_time
                
    def update(self, keys_pressed, game):
        self._handle_input(keys_pressed, game)
    
    def draw_map(self, game):
        # Ustawienie warsty na pierwszą warstwę
        layer_num = 1
        self.scale = game.scale
        # Przygotowanie warstwy
        game.map_surface = pygame.Surface((self.tmx_map_data.width * self.tmx_map_data.tilewidth, self.tmx_map_data.height * self.tmx_map_data.tileheight))
        
        # Pętla wyrysowująca kolejne kafelki na powierzchni
        for layer in self.layers:
            
            for tile in layer:
                game.map_surface.blit(tile.image, tile.rect)
                
            if layer_num == 1:
                game.PLAYER.draw(game.map_surface)
                
            layer_num += 1
        
        # Dostosowanie powierzchni do odpowiedniej skali
        game.map_surface = pygame.transform.scale(game.map_surface, (game.map_surface.get_width() * game.scale, game.map_surface.get_height() * game.scale))
        pos_x, pos_y = game.PLAYER.get_pos()
        
        # Obliczenie wymaganego offsetu tak, aby ekran był zawsze wycentrowany 
        scr_sizes = pygame.display.get_desktop_sizes()
        map_offset_x = (scr_sizes[0][0] // 2) - (pos_x * self.scale)
        map_offset_y = (scr_sizes[0][1] // 2) - (pos_y * self.scale)
        
        # Wyrysowanie powierzchni na ekranie
        game.SCREEN.blit(game.map_surface, (map_offset_x, map_offset_y))
                        
    def get_layers(self):
        return self.layers

class Test_map(Map):
    
    def __init__(self):
        super().__init__()
        self.load_map("testmap")

        
    def bake_events(self):
        cx, cy = self.layers[0][0 + 30 * 19].rect.center
        self.layers[0][0 + 30 * 19].add_event(Teleport(cx, cy, (24, 72), Test_map_2()))
        self.baked = 1
        
class Test_map_2(Map):
    
    def __init__(self):
        super().__init__()
        self.load_map("testmap2")
    
    def bake_events(self):
        cx, cy = self.layers[0][0].rect.center
        self.layers[0][0].add_event(Teleport(cx, cy, (24, 888), Test_map()))
        self.baked = 1