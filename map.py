import pygame
import pytmx
from pathlib import Path
from time import time

import creature


class Event:
    
    def __init__(self, coords: tuple, img=None):
        if img is not None:
            self.image = img
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = pygame.Rect(0, 0, 48, 48)

        x, y = coords
        self.rect.center = x, y
        
    # Wszystkie poniższe funkcje powinny, ale nie muszą zostać przeciążone 
    def check_stepped_on(self, game):
        pass
    
    def check_interact(self, game, tile):
        pass

    def draw(self, tile):
        if self.image is not None:
            image_rect = self.image.get_rect()
            image_rect.center = 24, 24
            tile.image.blit(self.image, image_rect)


class Teleport(Event):
    
    def __init__(self, coords, place_on_map: tuple, map=None, img=None):
        super().__init__(coords, img=img)
        self.dest_map = map
        self.map_coords = place_on_map

    def teleport(self, game):
        """Teleportuje gracza na wybrane koordynaty na wybranej mapie"""
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
        self.NPC_NAME = self.NPC.__class__.__name__
        self.current_tree = None
        self.radiant_selected = False

    def check_interact(self, game, tile):
        if game.map.check_if_looking_at(tile):
            if self.NPC.is_available() is not None:
                self.dialogue(game)
            else:
                pass
        else:
            pass

    def dialogue(self, game):

        if self.current_tree is None:
            self.current_tree = self.NPC.get_dialogue()

        if self.current_tree.__class__.__name__ == "RadiantTree" and not self.radiant_selected:
            self.current_tree.choose_random()
            self.radiant_selected = True

        game.map.in_dialogue = True

        if self.current_tree.get_current_line() is not None:
            game.map.current_dialogue = self
            name_tag, name_tag_rect = self.create_name_tag(game)

            content_tag, content_tag_rect = self.create_content_tag(game)
            content_tag.fill((128, 0, 32))

            npc_name, npc_name_rect = game.FONT.render(self.NPC_NAME, size=36, fgcolor=(255,255,255))
            npc_name_rect.center = name_tag_rect.w // 2, name_tag_rect.h // 2
            name_tag.blit(npc_name, npc_name_rect)

            content = self.current_tree.get_content()
            content, content_rect = game.FONT.render(content, size=24, fgcolor=(255,255,255))
            content_tag.blit(content, content_rect)

            game.map.dialogue_card.blit(npc_name, npc_name_rect)
            game.map.dialogue_card.blit(content_tag, content_tag_rect)
            self.current_tree.go_to_next()

        else:
            game.map.current_dialogue = None
            game.map.in_dialogue = False
            self.current_tree = None
            self.radiant_selected = False

        print(game.map.in_dialogue)

    def create_name_tag(self, game):
        name_tag = pygame.Surface((game.map.dialogue_card_rect.w // 6, game.map.dialogue_card_rect.h // 3))
        name_tag_rect = name_tag.get_rect()
        name_tag_rect.center = name_tag_rect.w // 2, game.map.dialogue_card_rect.h // 6
        return name_tag, name_tag_rect

    def create_content_tag(self, game):
        content_tag = pygame.Surface((game.map.dialogue_card_rect.w, 2 * game.map.dialogue_card_rect.h // 3))
        content_tag_rect = content_tag.get_rect()
        content_tag_rect.center = content_tag_rect.w // 2, 2 * game.map.dialogue_card_rect.h // 3
        return content_tag, content_tag_rect


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

        if keys_pressed[pygame.K_e] and not self.in_dialogue and cur_time - self.last_press > 0.5:
            for layer in self.layers:
                for tile in layer:
                    if len(tile.events) != 0:
                        for event in tile.events:
                            print(tile.x, tile.y, tile.events)
                            event.check_interact(game, tile)
                            self.last_press = cur_time

        elif keys_pressed[pygame.K_SPACE] and self.in_dialogue and cur_time - self.last_press > 0.5:
            self.current_dialogue.current_tree.flip_go_to_next()
            self.last_press = cur_time



    def update(self, keys_pressed, game):
        if self.in_dialogue:
            self.current_dialogue.dialogue(self.game)
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
                for event in tile.events:
                    if event.image is not None:
                        self.game.map_surface.blit(event.image, tile.rect)
                
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

    def add_teleport(self, tile: Tile, place_on_map: tuple, mapname: str):
        cx, cy = self.get_tile_center(tile)
        event = Teleport((cx, cy), place_on_map, mapname)
        self.add_event(tile, event)

    def add_dialogue(self, tile, img=None, npc=None):
        cx, cy = self.get_tile_center(tile)
        event = Dialogue((cx, cy), img=img, npc=npc)
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
class TestMap(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("testmap")
        print(self.layers)

    def bake_events(self):
        tile = self.get_tile(0, 0, 19)
        self.add_teleport(tile, (0, 72), TestMap2(self.game))
        tile = self.get_tile(0, 2, 2)
        self.add_dialogue(tile, img=self.game.BRIGITTE.body_textures[0], npc=self.game.BRIGITTE)
        self.baked = 1


class TestMap2(Map):

    def __init__(self, game):
        super().__init__(game)
        self.load_map("testmap2")
    
    def bake_events(self):
        tile = self.get_tile(0, 0, 0)
        self.add_teleport(tile, (24, 888), TestMap(self.game))
        self.baked = 1
