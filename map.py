import pygame
import pytmx
from pathlib import Path
from time import time

import creature


class Event:
    
    def __init__(self, coords: tuple, w=48, h=48, img=None):
        if img is not None:
            self.image = img
        else:
            self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        x, y = coords
        self.rect.center = x, y
        
    # Wszystkie poniższe funkcje powinny, ale nie muszą zostać przeciążone 
    def check_stepped_on(self, game):
        pass
    
    def check_interact(self, game, tile):
        pass


class Teleport(Event):
    
    def __init__(self, coords, place_on_map: tuple, map = None, img = None):
        super().__init__(coords, img=img)
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

    def __init__(self, coords, img=None, npc=None):
        super().__init__(coords, img=img)
        self.NPC = npc

    def check_interact(self, game, tile):
        if game.map.check_if_looking_at(tile):
            print("Looking at and interacting")
            # self.start_dialogue(game)
        else:
            pass

    # def start_dialogue(self, game):



class Fight(Event):
    pass

        
class Tile:
    def __init__(self, image, rect, impassable, size, x, y, layer):
        self.image = image
        self.rect = rect
        self.size = size
        self.x = x
        self.y = y
        self.layer = layer
        self.rect.center = x * self.size[0] + 24, y * self.size[1] + 24
        self.impassable = impassable
        self.width_pos = ((self.rect.x + 1) - (self.size[0] // 2), self.rect.x + (self.size[0] // 2))
        self.height_pos = ((self.rect.y + 1) - (self.size[1] // 2), self.rect.y + (self.size[1] // 2))
        self.events = []
        
    def add_event(self, event):
        self.events.append(event)

    def get_center(self):
        return self.rect.center


class Map:
    def __init__(self, game):

        self.game = game
        self.tmx_map_data = None
        self.layers = []
        self.map_width = None
        self.map_height = None
        self.last_press = time()
        self.cooldown = 0.25
        self.baked = 0
        self.scale = 1
        self.dialogue_card = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT // 4))
        self.dialogue_card_rect = self.dialogue_card.get_rect()
        self.dialogue_card_rect.center = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 8

    def load_map(self, mapname):
        
        if mapname[:-4] != ".tmx":
            mapname += ".tmx"
            
        map_path = Path.cwd()
        map_path /= Path(f"maps/{mapname.lower()}")
        self.tmx_map_data = pytmx.load_pygame(map_path)
        layer_num = 0
        
        for layer in self.tmx_map_data:
            self.layers.append([])
            
            if isinstance(layer, pytmx.TiledTileLayer):
                
                for x, y, gid in layer:
                    image = self.tmx_map_data.get_tile_image_by_gid(gid)
                    if image is not None:
                        impassable = self.tmx_map_data.get_tile_properties_by_gid(gid)["impassable"]
                        rect = image.get_rect()
                        tile = Tile(image, rect, impassable, (self.tmx_map_data.tilewidth,
                                                              self.tmx_map_data.tileheight), x, y, layer_num)
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
        if keys_pressed[pygame.K_e]:
            for layer in self.layers:
                for tile in layer:
                    if len(tile.events) != 0:
                        for event in tile.events:
                            print(tile.x, tile.y, tile.events)
                            event.check_interact(game, tile)

    def update(self, keys_pressed, game):
        self._handle_input(keys_pressed, game)
    
    def draw_map(self):
        # Ustawienie warsty na pierwszą warstwę
        layer_num = 1
        # Przygotowanie warstwy
        self.game.map_surface = pygame.Surface((self.tmx_map_data.width * self.tmx_map_data.tilewidth,
                                                self.tmx_map_data.height * self.tmx_map_data.tileheight))
        
        # Pętla wyrysowująca kolejne kafelki na powierzchni
        for layer in self.layers:
            
            for tile in layer:
                self.game.map_surface.blit(tile.image, tile.rect)
                
            if layer_num == 1:
                self.game.PLAYER.draw(self.game.map_surface)
                
            layer_num += 1
        
        # Dostosowanie powierzchni do odpowiedniej skali
        self.game.map_surface = pygame.transform.scale(self.game.map_surface,
                                                       (self.game.map_surface.get_width() * self.game.scale,
                                                        self.game.map_surface.get_height() * self.game.scale))

        pos_x, pos_y = self.game.PLAYER.get_pos()
        
        # Obliczenie wymaganego offsetu tak, aby ekran był zawsze wycentrowany 
        map_offset_x = (self.game.SCR_WIDTH // 2) - (pos_x * self.game.scale)
        map_offset_y = (self.game.SCR_HEIGHT // 2) - (pos_y * self.game.scale)
        
        # Wyrysowanie powierzchni na ekranie
        self.game.SCREEN.blit(self.game.map_surface, (map_offset_x, map_offset_y))
                        
    def get_layers(self):
        return self.layers

    def get_tile(self, layer, x, y):
        return self.layers[layer][x + self.tmx_map_data.width * y]

    def get_tile_center(self, tile):
        return tuple(tile.rect.center)

    def add_event(self, tile: Tile, event: Event):
        tile.add_event(event)

    def add_teleport(self, tile: Tile, place_on_map: tuple, mapname: str):
        cx, cy = self.get_tile_center(tile)
        event = Teleport((cx, cy), place_on_map, mapname)
        self.add_event(tile, event)

    def add_dialogue(self, tile, npc=None):
        cx, cy = self.get_tile_center(tile)
        event = Dialogue((cx, cy))
        self.add_event(tile, event)
        tile.impassable = True
    def get_neighbours(self, tile):
        try:
            top = self.get_tile(tile.layer, tile.x, tile.y - 1)
        except IndexError:
            top = None

        try:
            bottom = self.get_tile(tile.layer, tile.x, tile.y + 1)
        except IndexError:
            bottom = None

        try:
            left = self.get_tile(tile.layer, tile.x - 1, tile.y)
        except IndexError:
            left = None

        try:
            right = self.get_tile(tile.layer, tile.x + 1, tile.y)
        except IndexError:
            right = None

        return top, bottom, left, right

    def check_if_looking_at(self, tile):
        top, bottom, left, right = self.get_neighbours(tile)
        if top.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 2:
            return True
        if bottom.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 0:
            return True
        if left.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 1:
            return True
        if right.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 3:
            return True
        return False
class Test_map(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("testmap")
        print(self.layers)

    def bake_events(self):
        tile = self.get_tile(0, 0, 19)
        self.add_teleport(tile, (0, 72), Test_map_2(self.game))
        tile = self.get_tile(0, 2, 2)
        self.add_dialogue(tile)
        self.baked = 1


class Test_map_2(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("testmap2")
    
    def bake_events(self):
        tile = self.get_tile(0, 0, 0)
        self.add_teleport(tile, (24, 888), Test_map(self.game))
        self.baked = 1
