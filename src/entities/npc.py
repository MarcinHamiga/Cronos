import pygame

from ..data.dialogue import DialogueLine, DialogueTree, RadiantTree


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

    def __init__(self, assets):
        body_textures = assets["CHAR_BLUE_EYES_PERSON"]
        accessories = [assets["CHAR_DARKBLUE_HOODIE"], assets["CHAR_GREY_JEANS"], assets["CHAR_BROWN_BOBCUT"], assets["CHAR_DARKBLUE_SNEAKERS"]]
        super().__init__(body_textures, accessories)
        greeting_1 = DialogueLine("Hello! My name's Brigitte!", None)
        greeting_2 = DialogueLine("I hope you are having fun in our little town!", None)
        greeting_3 = DialogueLine("Alright then, time to go back to work. It was a pleasure!", None)

        greeting_1.set_next(greeting_2)
        greeting_2.set_next(greeting_3)

        greeting_tree = DialogueTree("GREETING", greeting_1)

        banter_1 = DialogueLine("*Humming*", None)
        banter_2 = DialogueLine("Huh, where did these Creatures go...?", None)
        banter_3 = DialogueLine("I'm so bored...", None)
        banter_4 = DialogueLine("I hope my shift ends soon enough...", None)
        banter_5 = DialogueLine("Oh, hello there. Sorry, I gotta go.", None)

        banter_tree = RadiantTree("BANTER", [banter_1, banter_2, banter_3,
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

    def __init__(self, assets):
        body_textures = assets["CHAR_BLUE_EYES_PERSON"]
        accessories = [assets["CHAR_DARKBLUE_HOODIE"], assets["CHAR_JEANS"]]
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

    def __init__(self, assets):
        body_textures = assets["CHAR_BLUE_EYES_PERSON"]
        accessories = [assets["CHAR_MEDICAL_UNIFORM"], assets["CHAR_BLONDE_PONYTAIL"]]
        super().__init__(body_textures, accessories)

        greeting_4 = DialogueLine("Bye now!", None)
        greeting_3 = DialogueLine("Just come talk to me and we will figure it out!", greeting_4)
        greeting_2 = DialogueLine("I can cure your Creatures anytime you need!", greeting_3)
        greeting_1 = DialogueLine("Hi! My name is Lily.", greeting_2)

        greeting_tree = DialogueTree("GREETING", greeting_1)

        healing_2 = DialogueLine("That'll be all. Your Creatures are happy and healthy.", None)
        healing_1 = DialogueLine("Right, I'm on it! Don't worry!", healing_2)

        healing_tree = RadiantTree("HEALING", [healing_1])

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

    def __init__(self, assets):
        body_textures = assets["CHAR_BROWN_EYES_PERSON"]
        accessories = [assets["CHAR_WHITERED_SNEAKERS"], assets["CHAR_WHITE_TSHIRT"], assets["CHAR_OVERALLS"]]
        super().__init__(body_textures, accessories)

        greeting_4 = DialogueLine("Anyway, I hope you have a great day. Visit anytime you need to buy something!", None)
        greeting_3 = DialogueLine("Did you meet Brigitte? I hope she doesn't come off as a little... harsh.", greeting_4)
        greeting_2 = DialogueLine("I came here with my daughter Brigitte two years back, so we are both new, just like you.", greeting_3)
        greeting_1 = DialogueLine("Oh, hi there! I'm Mark. I run this little store.", greeting_2)

        greeting_tree = DialogueTree("Greeting", greeting_1)

        trade_1 = DialogueLine("I've got everything you need.", None)

        trade_tree = RadiantTree("Trade", [trade_1])

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

    def __init__(self, assets):
        body_textures = assets["CHAR_BROWN_EYES_PERSON"]
        accessories = [assets["CHAR_FISHNETS"], assets["CHAR_DARKBLUE_HOODIE"], assets["CHAR_DARKBLUE_SKIRT"], assets["CHAR_DARKBLUE_SNEAKERS"], assets["CHAR_PINK_BOBCUT"]]
        super().__init__(body_textures, accessories)

        greeting_4 = DialogueLine("Sorry, I need to get going now. But I hope we can talk some more later! Cya!", None)
        greeting_3 = DialogueLine("I hope you are going to have a great time here!", greeting_4)
        greeting_2 = DialogueLine("You are the new guy here, aren't you?", greeting_3)
        greeting_1 = DialogueLine("Oh hi there! I'm Lavender.", greeting_2)

        greeting_tree = DialogueTree("Greeting", greeting_1)

        banter_1 = DialogueLine("Any plans for today? I would kill for some ice cream.", None)
        banter_2 = DialogueLine("It's so hoooot today...", None)
        banter_3 = DialogueLine("Ugh, why did my parents have to move here...", None)
        banter_tree = RadiantTree("Banter", [banter_1, banter_2, banter_3])

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


class LockedDoor(NPC):

    def __init__(self, assets):
        super().__init__(assets["MAP_DOOR"])

        closed_door = DialogueLine("It's locked", None)
        door = RadiantTree("Locked", [closed_door])

        self.dialogue_dict = {
            "CLOSED": door
        }

    def get_dialogue(self):
        return self.dialogue_dict["CLOSED"]

    def is_available(self):
        return self.dialogue_dict["CLOSED"]
