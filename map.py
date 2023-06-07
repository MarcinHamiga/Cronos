import pygame
import pytmx
from pathlib import Path

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

class Map:
    def __init__(self, scale):
        self.tmx_map_data = None
        self.map_width = None
        self.map_height = None
        self.scale = scale
        
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
        
    def _handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_1] and self.scale < 4:
            self.scale += 1
        if keys_pressed[pygame.K_2] and self.scale > 1:
            self.scale -= 1
                
    def update(self, keys_pressed):
        self._handle_input(keys_pressed)
    
    def draw_map(self, surface, screen, player):
        layer_num = 1
        surface = pygame.Surface((self.tmx_map_data.width * self.tmx_map_data.tilewidth, self.tmx_map_data.height * self.tmx_map_data.tileheight))
        for layer in self.layers:
            
            for tile in layer:
                surface.blit(tile.image, tile.rect)
                
            if layer_num == 1:
                player.draw(surface)
                
            layer_num += 1
            
        surface = pygame.transform.scale(surface, (surface.get_width() * self.scale, surface.get_height() * self.scale))
        pos_x, pos_y = player.get_pos()
        scr_sizes = pygame.display.get_desktop_sizes()
        map_offset_x = (scr_sizes[0][0] // 2) - (pos_x * self.scale)
        map_offset_y = (scr_sizes[0][1] // 2) - (pos_y * self.scale)
        screen.blit(surface, (map_offset_x, map_offset_y))
                        
    def get_layers(self):
        return self.layers
