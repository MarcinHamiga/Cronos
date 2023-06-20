import pygame

import dialogue


class Person(pygame.sprite.Sprite):

    def __init__(self, body_textures: list, px=24, py=24, accessories=None):
        super().__init__()
        if accessories is None:
            accessories = []
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
    
    def __init__(self, body_texture: list, px, py, accessories=None):
        super().__init__(body_texture, px, py, accessories)
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        self.creatures = []
        self.designated_creature = None
        self.items = []
        self.orientation = 0 # 0 - góra, 1 - prawo, 2 - dół, 3 - lewo
        self.money = 0
        
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
            
    def _handle_events(self, keys, layers):
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self._start_sprint()
            
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for rect in self._rectangles:
                rect.x -= movement * self.scale
            self.moving["left"] = True
            self.check_collision(layers)
            self.moving["left"] = False
            self.orientation = 3

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["right"] = True
            self.check_collision(layers)
            self.moving["right"] = False
            self.orientation = 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["top"] = True
            self.check_collision(layers)
            self.moving["top"] = False
            self.orientation = 0

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["bottom"] = True
            self.check_collision(layers)
            self.moving["bottom"] = False
            self.orientation = 2
        
        self.check_boundaries(layers)
        
        self._stop_sprint()
            
    def check_boundaries(self, game):

        if game.map.__class__.__name__ == "House":
            print(game.map.layers)
            print(game.map.layers[0])
        for tile in game.map.layers[0]:
            x, y = 0, 0
            if tile.x > x:
                x += tile.x
            if tile.y > y:
                y += tile.y

        for rect in self._rectangles:
            if rect.x > x * 48 * self.scale:
                rect.x = x * 48 * self.scale
            if rect.x < 0:
                rect.x = 0
            if rect.y > y * 48 * self.scale:
                rect.y = y * 48 * self.scale
            if rect.y < 0:
                rect.y = 0        
            
    def update(self, keys, layers):
        self._handle_events(keys, layers)
        
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

    def add_creature(self, creature):
        self.creatures.append(creature)

    def set_designated_creature(self, num):
        if num <= len(self.creatures):
            self.designated_creature = num
        else:
            self.designated_creature = self.creatures[0]

    def check_inventory(self):
        popped = False
        for idx, item in enumerate(self.items):
            if item.amount <= 0:
                self.items.pop(idx)
                popped = True
        return popped


class NPC(pygame.sprite.Sprite):

    def __init__(self, body_textures: list, accessories=None):
        super().__init__()
        if accessories is None:
            accessories = []
        if not isinstance(body_textures, list):
            body_textures = [body_textures]
        self.body_textures = []
        self.rectangles = []
        for texture in body_textures:
            self.body_textures.append(texture)
            rect = texture.get_rect()
            rect.center = 24, 24
            self.rectangles.append(rect)
        for accessory in accessories:
            rect = accessory.get_rect()
            rect.center = 24, 24
            self.rectangles.append(rect)
            self.body_textures.append(accessory)

    def get_image(self):
        npc_surface = pygame.Surface((48, 48))
        npc_surface = npc_surface.convert_alpha(npc_surface)
        npc_surface.fill((0, 0, 0, 0))
        for texture in self.body_textures:
            npc_surface.blit(texture, self.rectangles[0])

        return npc_surface


class Brigitte(NPC):
    
    def __init__(self, game):
        body_textures = game.ASSETS["CHAR_BLUE_EYES_PERSON"]
        accessories = [game.ASSETS["CHAR_DARKBLUE_HOODIE"], game.ASSETS["CHAR_GREY_JEANS"], game.ASSETS["CHAR_BROWN_BOBCUT"], game.ASSETS["CHAR_DARKBLUE_SNEAKERS"]]
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
    
    def __init__(self, game):
        body_textures = game.ASSETS["CHAR_BLUE_EYES_PERSON"]
        accessories = [game.ASSETS["CHAR_DARKBLUE_HOODIE"], game.ASSETS["CHAR_JEANS"]]
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


class Healer(NPC):

    def __init__(self, game):
        body_textures = game.ASSETS["CHAR_BLUE_EYES_PERSON"]
        accessories = [game.ASSETS["CHAR_MEDICAL_UNIFORM"], game.ASSETS["CHAR_BLONDE_PONYTAIL"]]
        super().__init__(body_textures, accessories)

        greeting_4 = dialogue.DialogueLine("Bye now!", None)
        greeting_3 = dialogue.DialogueLine("Just come talk to me and we will figure it out!", greeting_4)
        greeting_2 = dialogue.DialogueLine("I can cure your Creatures anytime you need!", greeting_3)
        greeting_1 = dialogue.DialogueLine("Hi! My name is Lily.", greeting_2)

        greeting_tree = dialogue.DialogueTree("GREETING", greeting_1)

        healing_2 = dialogue.DialogueLine("That'll be all. Your Creatures are happy and healthy.", None)
        healing_1 = dialogue.DialogueLine("Right, I'm on it! Don't worry!", healing_2)

        healing_tree = dialogue.RadiantTree("HEALING", [healing_1])

        self.player_greet = False
        self.DIALOGUE_DICT = {
            "GREETING": greeting_tree,
            "HEALING": healing_tree
        }

    def get_dialogue(self):
        if not self.player_greet:
            self.player_greet = True
            return self.DIALOGUE_DICT["GREETING"]
        return self.DIALOGUE_DICT["HEALING"]

    def is_available(self):
        if not self.player_greet:
            return self.DIALOGUE_DICT["GREETING"]
        else:
            return self.DIALOGUE_DICT["HEALING"]


class Trader(NPC):

    def __init__(self, game):
        body_textures = game.ASSETS["CHAR_BROWN_EYES_PERSON"]
        accessories = [game.ASSETS["CHAR_WHITERED_SNEAKERS"], game.ASSETS["CHAR_WHITE_TSHIRT"], game.ASSETS["CHAR_OVERALLS"]]
        super().__init__(body_textures, accessories)

        greeting_4 = dialogue.DialogueLine("Anyway, I hope you have a great day. Visit anytime you need to buy something!", None)
        greeting_3 = dialogue.DialogueLine("Did you meet Brigitte? I hope she doesn't come off as a little... harsh.", greeting_4)
        greeting_2 = dialogue.DialogueLine("I came here with my daughter Brigitte two years back, so we are both new, just like you.", greeting_3)
        greeting_1 = dialogue.DialogueLine("Oh, hi there! I'm Mark. I run this little store.", greeting_2)

        greeting_tree = dialogue.DialogueTree("Greeting", greeting_1)

        trade_1 = dialogue.DialogueLine("I've got everything you need.", None)

        trade_tree = dialogue.RadiantTree("Trade", [trade_1])

        self.player_greet = False
        self.DIALOGUE_DICT = {
            "GREETING": greeting_tree,
            "TRADE": trade_tree
        }

    def get_dialogue(self):
        if not self.player_greet:
            self.player_greet = True
            return self.DIALOGUE_DICT["GREETING"]
        return self.DIALOGUE_DICT["TRADE"]

    def is_available(self):
        if not self.player_greet:
            return self.DIALOGUE_DICT["GREETING"]
        else:
            return self.DIALOGUE_DICT["TRADE"]


class Lavender(NPC):

    def __init__(self, game):
        body_textures = game.ASSETS["CHAR_BROWN_EYES_PERSON"]
        accessories = [game.ASSETS["CHAR_FISHNETS"], game.ASSETS["CHAR_DARKBLUE_HOODIE"], game.ASSETS["CHAR_DARKBLUE_SKIRT"], game.ASSETS["CHAR_DARKBLUE_SNEAKERS"]]
        super().__init__(body_textures, accessories)

        greeting_4 = dialogue.DialogueLine("Sorry, I need to get going now. But I hope we can talk some more later! Cya!", None)
        greeting_3 = dialogue.DialogueLine("I hope you are going to have a great time here!", greeting_4)
        greeting_2 = dialogue.DialogueLine("You are the new guy here, aren't you?", greeting_3)
        greeting_1 = dialogue.DialogueLine("Oh hi there! I'm Lavender.", greeting_2)

        greeting_tree = dialogue.DialogueTree("Greeting", greeting_1)

        banter_1 = dialogue.DialogueLine("Any plans for today? I would kill for some ice cream.", None)
        banter_2 = dialogue.DialogueLine("It's so hoooot today...", None)
        banter_3 = dialogue.DialogueLine("Ugh, why did my parents have to move here...", None)
        banter_tree = dialogue.RadiantTree("Banter", [banter_1, banter_2, banter_3])

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