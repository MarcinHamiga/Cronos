import random

class Tile:
    def __init__(self, texture, px: int, py: int):
        self.texture = texture
        self.rect = self.texture.get_rect()
        self.rect.center = px, py
        self._type = None

    def draw(self, surface):
        surface.blit(self.texture, self.rect)

class Layer:
    def __init__(self, layer_name, width, height):
        self._TILEMAP = []
        self._MAP_W = width
        self._MAP_H = height
        self._NAME = layer_name
    
    def generate_layer(self, beginning = 0, end = 2):
        if beginning == end:
            for y in range(self._MAP_H):
                self._TILEMAP.append([])
                for x in range(self._MAP_W):
                    self._TILEMAP[y].append(beginning)
        else:
            for y in range(self._MAP_H):
                self._TILEMAP.append([])
                for x in range(self._MAP_W):
                    self._TILEMAP[y].append(random.randint(beginning, end))

    def fill_layer(self, texture_db):
        px = py = 16
        for id, tile_row in enumerate(self._TILEMAP):
            for idx, tile in enumerate(tile_row):
                self._TILEMAP[id][idx] = Tile(texture_db[tile], px, py)
                px += 32
            py += 32
            px = 16
            
    def draw_layer(self, surface):
        for row in self._TILEMAP:
            for tile in row:
                tile.draw(surface)

    def get_tilemap(self):
        return self._TILEMAP
    
    def append_row(self):
        self._TILEMAP.append([])

    def insert_row(self, idx = 0):
        try:
            self._TILEMAP.insert(idx, [])
        except IndexError:
            self._TILEMAP.insert(0, [])

class Map:
    def __init__(self, height: int, width: int, texture_db: dict):
        ground, mid, top = Layer("GROUND", width, height), Layer("MID", width, height), Layer("TOP", width, height)
        self._LAYERS = [ground, mid, top]
        self._generate_ground_layer()
        self._generate_mid_layer()
        self._fill_map(texture_db)

    def _generate_ground_layer(self, data = None):
        self._LAYERS[0].generate_layer()

    def _generate_mid_layer(self, data = None):
        self._LAYERS[1].generate_layer(3, 3)

    def _fill_map(self, texture_db: dict):
        for layer in self._LAYERS:
            if layer.get_tilemap() != []:
                layer.fill_layer(texture_db)
    def draw_first_layer(self, surface):
        self._LAYERS[0].draw_layer(surface)
        
    def draw_second_layer(self, surface):
        self._LAYERS[1].draw_layer(surface)
        
    def draw_third_layer(self, surface):
        self._LAYERS[2].draw_layer(surface)