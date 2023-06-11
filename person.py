import pygame

import dialogue


class Person(pygame.sprite.Sprite):
    
    def __init__(self, body_textures: list, px=24, py=24, accessories=[]):
        
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

class Player(Person):
    
    def __init__(self, body_texture: list, px, py, accessories=[]):
        super().__init__(body_texture, px, py, accessories)
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        self.creatures = []
        self.items = []
        self.orientation = 0 # 0 - góra, 1 - prawo, 2 - dół, 3 - lewo
        
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
            self.orientation = 3

        if keys_pressed[pygame.K_RIGHT]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["right"] = True
            self.check_collision(layers)
            self.moving["right"] = False
            self.orientation = 1

        if keys_pressed[pygame.K_UP]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["top"] = True
            self.check_collision(layers)
            self.moving["top"] = False
            self.orientation = 0

        if keys_pressed[pygame.K_DOWN]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["bottom"] = True
            self.check_collision(layers)
            self.moving["bottom"] = False
            self.orientation = 2
        
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
            if rect.x > x * 48 * game.scale:
                rect.x = x * 48 * game.scale
            if rect.x < 0:
                rect.x = 0
            if rect.y > y * 48 * game.scale:
                rect.y = y * 48 * game.scale
            if rect.y < 0:
                rect.y = 0        
            
    def update(self, keys_pressed, layers):
        self._handle_events(keys_pressed, layers)
        
    def get_pos(self):
        return self._rectangles[0].center

    def get_orient(self):
        return self.orientation

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
                    
    def read_scale(self, scale):
        self.scale = scale
        
    def get_rectangles(self):
        return self._rectangles
    
    def get_rectangle(self):
        return self._rectangles[0]
        


class NPC:
    def __init__(self, body_textures: list, accessories=[]):
        if not isinstance(body_textures, list):
            body_textures = [body_textures]
        self.body_textures = body_textures
        self.rectangles = []
        for texture in self.body_textures:
            rect = texture.get_rect()
            rect.center = 24, 24
            self.rectangles.append(rect)
        self.accessories = accessories
        for accessory in self.accessories:
            rect = accessory.get_rect()
            rect.center = 24, 24
            self.rectangles.append(rect)


class Brigitte(NPC):
    
    def __init__(self, body_textures: list, accessories=[]):
        super().__init__(body_textures, accessories)
        greeting_1 = dialogue.DialogueLine("Hello! My name's Brigitte!", None)
        greeting_2 = dialogue.DialogueLine("I hope you are having fun in our little town!", None)
        greeting_3 = dialogue.DialogueLine("Alright then, time to go back to work. It was a pleasure!", None)

        greeting_1.set_next(greeting_2)
        greeting_2.set_next(greeting_3)

        greeting_tree = dialogue.DialogueTree("GREETING", greeting_1)

        banter_1 = dialogue.DialogueLine("*Humming*", None)
        banter_2 = dialogue.DialogueLine("Huh, where did these Creatures go...?", None)
        banter_3 = dialogue.DialogueLine("I'm so bored...", None)
        banter_4 = dialogue.DialogueLine("I hope my shift ends soon enough...", None)
        banter_5 = dialogue.DialogueLine("Oh, hello there. Sorry, I gotta go.", None)

        banter_tree = dialogue.RadiantTree("BANTER", [banter_1, banter_2, banter_3,
                                                      banter_4, banter_5])

        self.player_greet = False

        self.DIALOGUE_DICT = {
            "GREETING": greeting_tree,
            "BANTER": banter_tree
        }

    def get_dialogue(self):
        if not self.player_greet:
            self.player_greet = True
            return self.DIALOGUE_DICT["GREETING"]
        return self.DIALOGUE_DICT["BANTER"]

    def is_available(self):
        if not self.player_greet:
            return self.DIALOGUE_DICT["GREETING"]
        else:
            return self.DIALOGUE_DICT["BANTER"]


class Thomas(NPC):
    
    def __init__(self, body_textures: list, accessories=[]):

        super().__init__(body_textures, accessories)

        self.player_greet = False
        self.DIALOGUE_DICT = {
            "GREETING_1": "Cześć.",
            "GREETING_2": "Mam nadzieję, że podoba Ci się tutaj.",
            "GREETING_3": "Przepraszam, muszę wracać do pracy. Trzymaj się!",
            "BANTER_1": "Praca, praca.",
            "BANTER_2": "Hejka. Niestety, ale nie mam czasu...",
            "BANTER_3": "Jak leci?"
        }

    def get_dialogue(self, key):
        if not self.player_greet:
            return self.DIALOGUE_DICT[key]
    