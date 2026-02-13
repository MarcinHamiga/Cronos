import pygame
import pytmx
from pathlib import Path
from time import time

from .events import Event, Teleport, Dialogue, Shop, Cure


class Tile:
    def __init__(self, image, rect, impassable, danger_zone, size, x, y, layer):
        self.image = image
        self.rect = rect
        self.size = size
        self.x = x
        self.y = y
        self.layer = layer
        self.rect.center = x * self.size[0] + 24, y * self.size[1] + 24
        self.impassable = impassable
        self.danger_zone = danger_zone
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
        self.in_dialogue = False
        self.current_dialogue = None
        self.dialogue_card = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT // 4))
        self.dialogue_card_rect = self.dialogue_card.get_rect()
        self.dialogue_card_rect.center = self.game.SCR_WIDTH // 2,  7 * (self.game.SCR_HEIGHT // 8)

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
                        data = self.tmx_map_data.get_tile_properties_by_gid(gid)
                        impassable = data["impassable"]
                        danger_zone = data["danger_zone"]
                        rect = image.get_rect()
                        tile = Tile(image, rect, impassable, danger_zone, (self.tmx_map_data.tilewidth,
                                                              self.tmx_map_data.tileheight), x, y, layer_num)
                        self.layers[layer_num].append(tile)

            layer_num += 1

    def _handle_input(self, keys_pressed, game):

        cur_time = time()
        if keys_pressed[pygame.K_e] and not self.in_dialogue and cur_time - self.last_press > 0.5:
            for layer in self.layers:
                for tile in layer:
                    if len(tile.events) != 0:
                        for event in tile.events:
                            event.check_interact(game, tile)
                            self.last_press = cur_time

        elif (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_e] or keys_pressed[pygame.K_RETURN]) and self.in_dialogue and cur_time - self.last_press > self.cooldown:
            self.current_dialogue.current_tree.flip_go_to_next()
            self.last_press = cur_time

        if keys_pressed[pygame.K_ESCAPE] and cur_time - self.last_press > self.cooldown and cur_time - self.game.func_key_used > self.cooldown:
            self.game.STATE_MANAGER.change_state(1)
            self.last_press = cur_time
            self.game.func_key_used = cur_time

        if keys_pressed[pygame.K_i] and cur_time - self.last_press > self.cooldown and cur_time - self.game.func_key_used > self.cooldown:
            self.game.STATE_MANAGER.change_state(2)
            self.last_press = cur_time
            self.game.func_key_used = cur_time

    def update(self, keys_pressed, game):
        if self.in_dialogue:
            self.current_dialogue.dialogue(self.game)
        self._handle_input(keys_pressed, game)

    def draw_map(self):
        layer_num = 1
        self.game.map_surface = pygame.Surface((self.tmx_map_data.width * self.tmx_map_data.tilewidth,
                                                self.tmx_map_data.height * self.tmx_map_data.tileheight))

        for layer in self.layers:

            for tile in layer:
                self.game.map_surface.blit(tile.image, tile.rect)
                for event in tile.events:
                    if event.image is not None:
                        self.game.map_surface.blit(event.image, tile.rect)

            if layer_num == 1:
                self.game.PLAYER.draw(self.game.map_surface)

            layer_num += 1

        self.game.map_surface = pygame.transform.scale(self.game.map_surface,
                                                       (self.game.map_surface.get_width() * self.game.scale,
                                                        self.game.map_surface.get_height() * self.game.scale))

        pos_x, pos_y = self.game.PLAYER.get_pos()

        map_offset_x = (self.game.SCR_WIDTH // 2) - (pos_x * self.game.scale)
        map_offset_y = (self.game.SCR_HEIGHT // 2) - (pos_y * self.game.scale)

        self.game.SCREEN.blit(self.game.map_surface, (map_offset_x, map_offset_y))

        if self.in_dialogue:
            self.game.SCREEN.blit(self.dialogue_card, self.dialogue_card_rect)

    def clear_dialogue_card(self):
        self.dialogue_card = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT // 4))
        self.dialogue_card_rect = self.dialogue_card.get_rect()
        self.dialogue_card_rect.center = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 8

    def get_layers(self):
        return self.layers

    def get_tile(self, layer, x, y):
        return self.layers[layer][x + self.tmx_map_data.width * y]

    def get_tile_center(self, tile):
        return tuple(tile.rect.center)

    def add_event(self, tile: Tile, event: Event):
        tile.add_event(event)

    def add_teleport(self, tile: Tile, place_on_map: tuple, mapname, img=None):
        cx, cy = self.get_tile_center(tile)
        px, py = place_on_map
        px = 24 + px * 48
        py = 24 + py * 48
        event = Teleport((cx, cy), (px, py), mapname, img=img)
        self.add_event(tile, event)

    def add_dialogue(self, tile, img=None, npc=None):
        cx, cy = self.get_tile_center(tile)
        event = Dialogue((cx, cy), img=img, npc=npc)
        self.add_event(tile, event)
        tile.impassable = True

    def add_shop(self, tile, img=None, npc=None):
        cx, cy = self.get_tile_center(tile)
        event = Shop((cx, cy), img=img, npc=npc)
        self.add_event(tile, event)
        tile.impassable = True

    def add_cure(self, tile, img=None, npc=None):
        cx, cy = self.get_tile_center(tile)
        event = Cure((cx, cy), img=img, npc=npc)
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
        try:
            if top.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 2:
                return True
        except AttributeError:
            pass

        try:
            if bottom.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 0:
                return True
        except AttributeError:
            pass

        try:
            if left.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 1:
                return True
        except AttributeError:
            pass

        try:
            if right.rect.collidepoint(self.game.PLAYER.get_pos()) and self.game.PLAYER.get_orient() == 3:
                return True
        except AttributeError:
            pass

        return False


class TestMap(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("testmap")

    def bake_events(self):
        tile = self.get_tile(0, 0, 19)
        self.add_teleport(tile, (0, 1), TestMap2(self.game))
        self.baked = 1


class TestMap2(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("testmap2")

    def bake_events(self):
        tile = self.get_tile(0, 0, 0)
        self.add_teleport(tile, (0, 18), TestMap(self.game))
        tile = self.get_tile(0, 0, 7)
        self.add_teleport(tile, (28, 1), Dockersville(self.game))
        self.baked = 1


class Dockersville(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("dockersville")

    def bake_events(self):
        tile = self.get_tile(0, 29, 1)
        self.add_teleport(tile, (1, 7), TestMap2(self.game))
        tile = self.get_tile(0, 18, 5)
        self.add_teleport(tile, (8, 13), House(self.game), self.game.ASSETS["MAP_DOOR"])
        tile = self.get_tile(0, 25, 7)
        self.add_dialogue(tile, self.game.LAVENDER.get_image(), self.game.LAVENDER)
        tile = self.get_tile(0, 7, 7)
        self.add_dialogue(tile, self.game.LOCKEDDOOR.get_image(), self.game.LOCKEDDOOR)
        tile = self.get_tile(0, 21, 14)
        self.add_teleport(tile, (7, 13), CreatureCenter(self.game), self.game.ASSETS["MAP_DOOR"])
        self.baked = 1


class House(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map(mapname="house")

    def bake_events(self):
        tile = self.get_tile(0, 8, 15)
        self.add_teleport(tile, (18, 6), Dockersville(self.game))

        tile = self.get_tile(0, 7, 3)
        self.add_dialogue(tile, img=self.game.BRIGITTE.get_image(), npc=self.game.BRIGITTE)
        tile = self.get_tile(0, 13, 12)
        self.add_shop(tile, self.game.TRADER.get_image(), self.game.TRADER)
        self.baked = 1


class CreatureCenter(Map):
    def __init__(self, game):
        super().__init__(game)
        self.load_map("creature_center")

    def bake_events(self):
        tile = self.get_tile(0, 7, 14)
        self.add_teleport(tile, (21, 15), Dockersville(self.game))
        tile = self.get_tile(0, 7, 5)
        self.add_cure(tile, img=None, npc=self.game.HEALER)
        tile = self.get_tile(0, 7, 4)
        self.add_cure(tile, img=self.game.HEALER.get_image(), npc=self.game.HEALER)
        self.baked = 1
