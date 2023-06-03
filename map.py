import pygame
import pytmx

class Tile(pygame.sprite.Sprite):
    def __init__(self, texture, px, py):
        super().__init__()
        self.texture = texture
        self.rect = self.texture.get_rect()
        self.rect.center = px, py
        
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        
    def _start_sprint(self):
        self._movement_speed_multiplier = 1.5
    
    def _stop_sprint(self):
        self._movement_speed_multiplier = 1.0
    
    def _handle_events(self, keys_pressed):
        if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
            self._start_sprint()
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        if keys_pressed[pygame.K_LEFT]:
            for rect in self._rectangles:
                rect.move_ip([int(-movement), 0])
        if keys_pressed[pygame.K_RIGHT]:
            for rect in self._rectangles:
                rect.move_ip([movement, 0])
        if keys_pressed[pygame.K_UP]:
            for rect in self._rectangles:
                rect.move_ip([0, -movement])
        if keys_pressed[pygame.K_DOWN]:
            for rect in self._rectangles:
                rect.move_ip([0, movement])
        
    def update(self, keys_pressed):
        self._handle_events(keys_pressed)
        
    def draw(self, surface):
        surface.blit(self.texture, self.rect)
        
class Layer:
    def __init__(self, width, height, tilemap, assets):
        self._width = width
        self._height = height
        self._TILES = []
        self.create_tiles(tilemap, assets)
        
    def create_tiles(self, tilemap, assets):
        px = py = 16
        for tile_row in tilemap:
            for tile in tile_row:
                self._TILES.append(Tile(assets[tile], px, py))
                px += 32
            px = 16
            py += 32

    def draw_tiles(self, surface):
        for tile_row in self._TILES:
            for tile in tile_row:
                tile.draw(surface)
                
class Map(pygame.surface.Surface):
    def __init__(self, mapname, player, assets):
        with open(mapname, "rb") as file:
            self.loaded_data = pickle.load(file)
            self.tilemaps = [self.loaded_data["layer1"]["data"], self.loaded_data["layer2"]["data"], self.loaded_data["layer3"]["data"]]
            self.map_width, self.map_height = self.loaded_data["layer1"]["width"], self.loaded_data["layer1"]["height"]
        super().__init__((self.map_width, self.map_height))
        self.layers = []
        self.player = player
        self.gen_layers(assets)
        
    def load_map(self, mapname):
        self.map_width, self.map_height, self.tilemaps = pickle.load(mapname)
        
    def gen_layers(self, assets):
        for tilemap in self.tilemaps:
            self.layers.append(Layer(self.map_width, self.map_height, tilemap, assets))
            
            
    def draw_first_layer(self):
        self.layers[0].draw_tiles(self)
        
    def draw_second_layer(self):
        self.layers[1].draw_tiles(self)
        
    def draw_third_layer(self):
        self.layers[2].draw_tiles(self)