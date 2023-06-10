import pygame
from random import randint

class Person(pygame.sprite.Sprite):
    
    def __init__(self, body_textures: list, px, py, accessories = []):
        
        super().__init__()
        
        self.rotation = 0 # 0 - w dół, 1 - w lewo, 2 - w górę , 3 - w prawo
        
        if not isinstance(body_textures, (list, tuple)):
            body_textures = [body_textures]
        # Tekstury używane w zależności od obecnej orientacji postaci na mapie.
        self._body_textures = []
       
        for texture in body_textures:
            self._body_textures.append(texture)
        
        for accessory in accessories:
            self._body_textures.append(accessory)
        
        self._rectangles = []
        
        for x in self._body_textures:
            rectangle = x.get_rect()
            rectangle.center = px, py
            self._rectangles.append(rectangle)
        
    def draw(self, surface):
        for texture, rect in zip(self._body_textures, self._rectangles):
            surface.blit(texture, rect)
            
    def update(self):
        pass
    
    def get_dialogue_window(self, game):
        surface = pygame.Surface((game.SCR_WIDTH, game.SCR_HEIGHT))
        surface.fill((128, 0, 32))
        surface_rect = surface.get_rect()
        
        return surface, surface_rect
        
        
        
class Player(Person):
    
    def __init__(self, body_texture: list, px, py, accessories = []):
        super().__init__(body_texture, px, py, accessories)
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        self.creatures = []
        self.items = []
        
        self.moving = {
            "top": False,
            "bottom" : False,
            "right" : False,
            "left" : False,
        }
     
    def _start_sprint(self):
        self._movement_speed_multiplier = 2.0
    
    def _stop_sprint(self):
        self._movement_speed_multiplier = 1.0
            
    def _handle_events(self, keys_pressed, layers):
        if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
            self._start_sprint()
            
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        
        if keys_pressed[pygame.K_LEFT]:
            for rect in self._rectangles:
                rect.x -= movement * self.scale
            self.moving["left"] = True
            self.check_collision(layers)
            self.moving["left"] = False

            
        if keys_pressed[pygame.K_RIGHT]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["right"] = True
            self.check_collision(layers)
            self.moving["right"] = False
            
            
        if keys_pressed[pygame.K_UP]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["top"] = True
            self.check_collision(layers)
            self.moving["top"] = False
            
            
        if keys_pressed[pygame.K_DOWN]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["bottom"] = True
            self.check_collision(layers)
            self.moving["bottom"] = False
        
        self.check_boundaries(layers)
        
        self._stop_sprint()
            
    def check_boundaries(self, game):
        
        for tile in game.map.layers[0]:
            x, y = 0, 0
            if tile.x > x:
                x += tile.x
            if tile.y > y:
                y += tile.y

        for rect in self._rectangles:
            if rect.x > (x - 1) * 48 * self.scale:
                rect.x = (x - 1) * 48 * self.scale
            if rect.x < 0:
                rect.x = 0
            if rect.y > (y - 1) * 48 * self.scale:
                rect.y = (y - 1) * 48 * self.scale
            if rect.y < 0:
                rect.y = 0        
            
    def update(self, keys_pressed, layers):
        self._handle_events(keys_pressed, layers)
        
    def get_pos(self):
        return self._rectangles[0].center

    def set_pos(self, coordinates: tuple):
        pos_x, pos_y = coordinates
        for rect in self._rectangles:
            rect.center = pos_x, pos_y

    def reverse_movement(self):
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        if self.moving["left"]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["left"] = False
        if self.moving["right"]:
            for rect in self._rectangles:
                rect.x -= movement * self.scale
            self.moving["right"] = False
        if self.moving["top"]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["top"] = False
        if self.moving["bottom"]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["bottom"] = False

    def check_collision(self, game):
        for layer in game.map.layers:
            for tile in layer:
                if tile.rect.colliderect(self._rectangles[0]) and tile.impassable == True:
                    self.reverse_movement()
                if len(tile.events) != 0:
                    for event in tile.events:
                        event.check_stepped_on(game)
                        event.check_interact(game)
                    
    def read_scale(self, scale):
        self.scale = scale
        
    def get_rectangles(self):
        return self._rectangles
    
    def get_rectangle(self):
        return self._rectangles[0]
        
        
class Brigitte(Person):
    
    def __init__(self, body_textures: list, px, py, accessories=[]):
        super().__init__(body_textures, px, py, accessories)
        self.player_greet = False
        self.DIALOGUE_DICT = {
            "GREETING_1" : "Hejka! Nazywam się Brigitte!",
            "GREETING_2" :  "Mam nadzieję, że dobrze się bawisz w naszym urokliwym miasteczku!",
            "GREETING_3" : "No nic, pora wracać do swoich zajęć. Papatki!",
            "BANTER_1" : "*Nuci*",
            "BANTER_2" : "Eh, gdzie się podziały te stworki...",
            "BANTER_3" : "Ale nudy..."
        }
        
class Thomas(Person):
    def __init__(self, body_textures: list, px, py, accessories=[]):
        super().__init__(body_textures, px, py, accessories)
        
        