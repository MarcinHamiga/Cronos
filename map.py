import pygame
import pytmx
from pathlib import Path

class Map:
    def __init__(self, player, init_map: str):
        map_path = Path.cwd()
        map_path /= Path(f"maps/{init_map}")
        self._tmx_map_data = pytmx.load_pygame(map_path)
        self._player = player
        self._player.set_pos((self._tmx_map_data.tilewidth * self._tmx_map_data.width, self._tmx_map_data.tilewidth * self._tmx_map_data.height))
        
        self._spawn_point = 
        
    def draw_map(self, screen):
        layer_num = 1
        for layer in self._tmx_map_data:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self._tmx_map_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile_rect = pygame.Rect(x * self._tmx_map_data.tilewidth, y * self._tmx_map_data.tileheight, self._tmx_map_data.tilewidth, self._tmx_map_data.tileheight)
                        adjusted_pos = tile_rect.move(self._player.get_pos())
                        screen.blit(tile, adjusted_pos)
                if layer_num == 1:
                    self._player.draw(screen)
                layer_num += 1
                        
                        