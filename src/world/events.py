import pygame


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
        game.PLAYER.set_pos(self.map_coords)
        if self.dest_map is not None:
            game.map = self.dest_map

    def check_stepped_on(self, game):
        if self.rect.colliderect(game.PLAYER.get_rectangle()):
            self.teleport(game)

    def check_interact(self, game, tile):
        if game.map.check_if_looking_at(tile):
            self.teleport(game)


class Dialogue(Event):

    def __init__(self, coords, img=None, npc=None):
        super().__init__(coords, img=img)
        self.NPC = npc
        if npc.__class__.__name__.lower() == "lockeddoor":
            self.NPC_NAME = ""
        else:
            self.NPC_NAME = self.NPC.__class__.__name__
        self.current_tree = None
        self.radiant_selected = False

    def check_interact(self, game, tile):
        if game.map.check_if_looking_at(tile):
            if self.NPC.is_available() is not None:
                self.dialogue(game)

    def dialogue(self, game):

        if self.current_tree is None:
            self.current_tree = self.NPC.get_dialogue()

        if self.current_tree.__class__.__name__ == "RadiantTree" and not self.radiant_selected:
            self.current_tree.choose_random()
            self.radiant_selected = True

        game.map.in_dialogue = True

        if self.current_tree.get_current_line() is not None:
            game.SCREEN.fill((0, 0, 0))
            game.map.current_dialogue = self
            name_tag, name_tag_rect = self.create_name_tag(game)

            content_tag, content_tag_rect = self.create_content_tag(game)
            content_tag.fill((128, 0, 32))

            npc_name, npc_name_rect = game.FONT.render(self.NPC_NAME, size=36, fgcolor=(255,255,255))
            npc_name_rect.center = name_tag_rect.w // 2, name_tag_rect.h // 2
            name_tag.blit(npc_name, npc_name_rect)

            content = self.current_tree.get_content()
            content, content_rect = game.FONT.render(content, size=24, fgcolor=(255,255,255))
            content_rect.center = content_tag_rect.w // 2, content_tag_rect.h // 2
            content_tag.blit(content, content_rect)

            game.map.dialogue_card.fill((0, 0, 0))
            game.map.dialogue_card.blit(npc_name, npc_name_rect)
            game.map.dialogue_card.blit(content_tag, content_tag_rect)
            self.current_tree.go_to_next()

        else:
            game.map.current_dialogue = None
            game.map.in_dialogue = False
            self.current_tree = None
            self.radiant_selected = False

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


class Shop(Dialogue):
    def __init__(self, coords: tuple, img=None, npc=None):
        super().__init__(coords, img, npc)

    def dialogue(self, game):
        super().dialogue(game)
        if not game.map.in_dialogue:
            game.STATE_MANAGER.change_state(6)
            game.SHOPSCREEN.set_for_refresh()


class Cure(Dialogue):
    def __init__(self, coords: tuple, img=None, npc=None):
        super().__init__(coords, img, npc)

    def dialogue(self, game):
        super().dialogue(game)
