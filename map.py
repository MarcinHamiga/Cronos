import pygame

class Tile:
    def __init__(self, texture: pygame.image, px: int, py: int):
        self.texture = texture
        self.rect = self.texture.get_rect()
        self.rect.center = px, py

    def draw(self, surface):
        surface.blit(self.texture, self.rect)

class Map:
    def __init__(self, height: int, width: int, texture_db: dict):
        self.MAP = []
        self._generate_map(height, width)
        self._fill_map(texture_db)

    def _generate_map(self, height, width):
        for y in range(height):
            self.MAP.append([])
            for x in range(width):
                self.MAP[y].append(0)

    def _fill_map(self, texture_db: dict):
        px, py = 16, 16
        for id, tile_row in enumerate(self.MAP):
            for idx, tile in enumerate(tile_row):
                self.MAP[id][idx] = Tile(texture_db[tile], px, py)
                px += 32
            py += 32
            px = 16

    def draw_map(self, surface: pygame.display):
        for row in self.MAP:
            for tile in row:
                tile.draw(surface)