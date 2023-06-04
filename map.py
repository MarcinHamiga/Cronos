import pygame
import pytmx
from pathlib import Path

class Map(pygame.Surface):
    def __init__(self, scr_w, scr_h):
        self.tmx_map_data = None
        self._scr_w = scr_w
        self._scr_w_center = scr_w // 2
        self._scr_h = scr_h
        self._scr_h_center = scr_h // 2
        self.map_width = None
        self.map_height = None
        
    def load_map(self, mapname,):
        
        if mapname[:-4] != ".tmx":
            mapname += ".tmx"
            
        map_path = Path.cwd()
        map_path /= Path(f"maps/{mapname.lower()}")
        self.tmx_map_data = pytmx.load_pygame(map_path)
        self.layers = []
        self.layers_rects = []
        layer_num = 0
        item_counter = 0
        height_counter = 0
        y_tracker = 0
        
        for layer in self.tmx_map_data:
            self.layers.append([])
            self.layers_rects.append([])
            
            if isinstance(layer, pytmx.TiledTileLayer):
                item_counter = 0
                
                for x, y, gid in layer:
                    print(x, y)
                    tile = self.tmx_map_data.get_tile_image_by_gid(gid)
                    
                    if tile is not None:
                        tile = pygame.transform.scale(tile, (self.tmx_map_data.tilewidth, self.tmx_map_data.tileheight))
                        self.layers[layer_num].append(tile)
                        
                        if self.layers[layer_num][item_counter]:
                            item_counter += 1
                            tile_rect = tile.get_rect()
                            tile_rect.center = (x * self.tmx_map_data.tilewidth, y * self.tmx_map_data.tileheight)
                            self.layers_rects[layer_num].append(tile_rect)

                        
            layer_num += 1
        
                
                
    def update(self):
        pass
    
    def draw_map(self, screen, player):
        layer_num = 1
        player_x, player_y = player.get_pos()
        
        for layer in self.layers:
            
            for tile, tile_rect in zip(layer, self.layers_rects[layer_num - 1]):
                adjusted_pos = tile_rect.move(self._scr_w_center - 16 - player_x, self._scr_h_center - 16 - player_y)
                screen.blit(tile, adjusted_pos)
                
            if layer_num == 1:
                player.draw(screen)
                
            layer_num += 1
                        
                        
    def get_tile_at(self):
        pos_x, pos_y = self._player.get_pos()
                        
    def get_map_size(self):
        print(self.tmx_map_data.width, self.tmx_map_data.height)
        return (self.tmx_map_data.width - 1) * self.tmx_map_data.tilewidth, (self.tmx_map_data.height - 1) * self.tmx_map_data.tileheight