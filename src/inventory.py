from time import time

import pygame

from src import items


class SelectionWindow:
    def __init__(self, page_size):
        self.page_size = page_size
        self.current_index = 0
        self.offset = 0

    def move_up(self):
        if self.current_index > 0:
            self.current_index -= 1
            if self.current_index % self.page_size == self.page_size - 1:
                self.offset -= 1

    def move_down(self, total_items):
        if self.current_index < total_items - 1:
            self.current_index += 1
            if self.current_index % self.page_size == 0:
                self.offset += 1

    def reset(self):
        self.current_index = 0
        self.offset = 0

    def visible_indexes(self, total_items):
        start = self.offset * self.page_size
        end = min(start + self.page_size, total_items)
        return range(start, end)


# Ten obiekt typu ItemCard jest statycznych rozmiarów. Istnieje z powodu kodu, który potrzebuje tego typu klasy
class ItemCard:

    def __init__(self, item, w=240, h=48):

        if h < 48:
            h = 48
        if w < 180:
            w = 180

        self.item = item
        self.card_width = w
        self.card_height = h
        self.card_surface = pygame.Surface((self.card_width, self.card_height))

    def draw_card(self, font, is_current: bool):
        if is_current:
            self.card_surface.fill((180, 180, 180))
        else:
            self.card_surface.fill((128, 0, 35))

        item_name, name_rect = font.render(f"{self.item.name}", (255, 255, 255))
        name_rect.center = name_rect.w // 2 + 48, 12

        item_amount, amount_rect = font.render(f"Amount: {self.item.amount}", (255, 255, 255))
        amount_rect.center = amount_rect.w // 2 + 48, 36

        if self.item.icon is not None:
            icon_rect = self.item.icon.get_rect()
            icon_rect.center = 24, 24
            self.card_surface.blit(self.item.icon, icon_rect)

        self.card_surface.blit(item_name, name_rect)
        self.card_surface.blit(item_amount, amount_rect)

        return self.card_surface


class DynamicItemCard:

    def __init__(self, item, scr_width, scr_height, font, print_price=False):
        surf_w, surf_h = scr_width // 2, scr_height // 6
        self.surface = pygame.Surface((surf_w, surf_h))
        self.surface_rect = self.surface.get_rect()
        self.print_price = print_price

        self.item = item
        self.font = font
        self.font_size = scr_height // 24

        self.icon = self.item.icon
        self.icon = pygame.transform.scale(self.icon, ((scr_height // 6), (scr_height // 6)))
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.center = self.icon_rect.w // 2, self.icon_rect.h // 2

        self.name, self.name_rect = self.font.render(f"{self.item.name}", size=self.font_size, fgcolor=(0, 0, 0))
        self.name_rect.center = (self.surface_rect.w + self.icon_rect.w) // 2, self.surface_rect.h // 4

    def draw_card(self, is_current: bool):
        if is_current:
            self.surface.fill((255, 255, 255))
        else:
            self.surface.fill((128, 0, 35))

        if self.print_price:
            amount, amount_rect = self.font.render(f"Price: {self.item.price}", size=self.font_size, fgcolor=(0, 0, 0))
            amount_rect.center = (self.surface_rect.w + self.icon_rect.w) // 2, self.surface_rect.h // 4 + self.surface_rect.h // 2
        else:
            amount, amount_rect = self.font.render(f"Amount: {self.item.amount}", size=self.font_size, fgcolor=(0, 0, 0))
            amount_rect.center = (self.surface_rect.w + self.icon_rect.w) // 2, self.surface_rect.h // 4 + self.surface_rect.h // 2

        self.surface.blit(self.icon, self.icon_rect)
        self.surface.blit(self.name, self.name_rect)
        self.surface.blit(amount, amount_rect)

        return self.surface


class DynamicCreatureCard:

    def __init__(self, creature, scr_width, scr_height, font):
        surf_w, surf_h = scr_width // 2, scr_height // 6
        self.surface = pygame.Surface((surf_w, surf_h))
        self.surface_rect = self.surface.get_rect()

        self.creature = creature
        self.font = font
        self.font_size = 32

        self.image = self.creature.image
        self.image = pygame.transform.scale(self.image, ((scr_height // 6), (scr_height // 6)))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.image_rect.w // 2, self.image_rect.h // 2

        self.name, self.name_rect = font.render(f"Name: {str(self.creature)}", size=32, fgcolor=(0, 0, 0))
        self.name_rect.center = self.surface_rect.w // 2 + self.image_rect.w, self.surface_rect.h // 4

    def draw_card(self, is_current):
        if is_current:
            self.surface.fill((255, 255, 255))
        else:
            self.surface.fill((128, 0, 35))

        amount, amount_rect = self.font.render(
            f"Lvl: {self.creature.level}, HP:{self.creature.health}/{self.creature.max_health}",
            size=32,
            fgcolor=(0, 0, 0),
        )
        amount_rect.center = self.surface_rect.w // 2 + self.image_rect.w, self.surface_rect.h // 4 + self.surface_rect.h // 2

        self.surface.blit(self.image, self.image_rect)
        self.surface.blit(self.name, self.name_rect)
        self.surface.blit(amount, amount_rect)

        return self.surface


class CreatureStatusCard:

    def __init__(self, scr_width, scr_height):
        surf_w, surf_h = scr_width // 2, scr_height // 2
        self.surface = pygame.Surface((surf_w, surf_h))
        self.surface_rect = self.surface.get_rect()

        self.creature = None
        self.image = None
        self.image_rect = None

        self.font_size = scr_height // 48
        self.free_width = None

    def set_creature(self, creature, scr_height):
        self.creature = creature
        self.image = self.creature.image
        self.image = pygame.transform.scale(self.image, ((scr_height // 6), (scr_height // 6)))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.image_rect.w // 2, self.image_rect.h // 2
        self.free_width = self.surface_rect.w - self.image_rect.w

    def get_creature(self):
        return self.creature

    def draw_card(self, font):
        self.surface.fill((128, 0, 35))
        self.surface.blit(self.image, self.image_rect)

        data, data_rect = font.render(f"Name: {str(self.creature)}", size=self.font_size)
        data_rect.center = self.free_width // 4 + self.image_rect.w, self.surface_rect.h // 6
        self.surface.blit(data, data_rect)

        data, data_rect = font.render(f"LV: {self.creature.level}", size=self.font_size)
        data_rect.center = self.free_width // 4 + self.image_rect.w + self.free_width // 2, self.surface_rect.h // 6
        self.surface.blit(data, data_rect)

        data, data_rect = font.render(f"HP: {self.creature.health}/{self.creature.max_health}", size=self.font_size)
        data_rect.center = self.free_width // 4 + self.image_rect.w, self.surface_rect.h // 6 + self.surface_rect.h // 3
        self.surface.blit(data, data_rect)

        data, data_rect = font.render(f"XP: {self.creature.xp}/{self.creature.required_xp}", size=self.font_size)
        data_rect.center = self.free_width // 4 + self.image_rect.w + self.free_width // 2, self.surface_rect.h // 6 + self.surface_rect.h // 3
        self.surface.blit(data, data_rect)

        data, data_rect = font.render(f"SP: {self.creature.special_points}/{self.creature.max_special_points}", size=self.font_size)
        data_rect.center = self.free_width // 4 + self.image_rect.w, self.surface_rect.h // 6 + self.surface_rect.h // 3 * 2
        self.surface.blit(data, data_rect)

        return self.surface


class Inventory:

    def __init__(self, game):
        assets = game.ASSETS
        self.player = game.PLAYER
        self.item_dict = items.Item_dict(assets)
        self.shop_dict = items.Shop_dict(assets)
        self.game = game

        self.item_cards = []
        self.creature_cards = []
        self.creature_status = CreatureStatusCard(self.game.SCR_WIDTH, self.game.SCR_HEIGHT)

        self.item_selection = SelectionWindow(page_size=6)
        self.creature_selection = SelectionWindow(page_size=3)
        self.choosing_item = True

        self.click_cooldown = 0.15
        self.last_click = 0

        for item in self.player.items:
            self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

        for creature in self.player.creatures:
            self.creature_cards.append(DynamicCreatureCard(creature, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    @property
    def current_item(self):
        return self.item_selection.current_index

    @property
    def offset(self):
        return self.item_selection.offset

    @property
    def current_creature(self):
        return self.creature_selection.current_index

    @property
    def creature_offset(self):
        return self.creature_selection.offset

    def check_for_strays(self):
        self.player.items = [item for item in self.player.items if item.amount > 0]

    def _check_card_integrity(self):

        self.check_for_strays()

        if len(self.item_cards) != len(self.player.items):
            self.item_cards = []
            for item in self.player.items:
                self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

        if len(self.creature_cards) != len(self.player.creatures):
            self.creature_cards = []
            for creature in self.player.creatures:
                self.creature_cards.append(DynamicCreatureCard(creature, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    def draw_status(self):
        self.creature_status.set_creature(self.player.creatures[self.current_creature], self.game.SCR_HEIGHT)
        surface = self.creature_status.draw_card(self.game.FONT)
        surface_rect = surface.get_rect()
        surface_rect.center = self.game.SCR_WIDTH // 2 + self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 4
        self.game.SCREEN.blit(surface, surface_rect)

    def draw_items(self):
        visible_indexes = list(self.item_selection.visible_indexes(len(self.item_cards)))
        for draw_index, item_index in enumerate(visible_indexes):
            card_surface = self.item_cards[item_index].draw_card(item_index == self.current_item)
            card_surface_rect = card_surface.get_rect()
            card_surface_rect.center = self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + draw_index * self.game.SCR_HEIGHT // 6
            self.game.SCREEN.blit(card_surface, card_surface_rect)

    def draw_creatures(self):
        visible_indexes = list(self.creature_selection.visible_indexes(len(self.creature_cards)))
        for draw_index, creature_index in enumerate(visible_indexes):
            card_surface = self.creature_cards[creature_index].draw_card(creature_index == self.current_creature)
            card_surface_rect = card_surface.get_rect()
            card_surface_rect.center = self.game.SCR_WIDTH // 4 + self.game.SCR_WIDTH // 2, (
                self.game.SCR_HEIGHT // 2 + self.game.SCR_HEIGHT // 12
            ) + draw_index * self.game.SCR_HEIGHT // 6
            self.game.SCREEN.blit(card_surface, card_surface_rect)

    def draw(self):
        self._check_card_integrity()
        self.draw_creatures()
        self.draw_items()
        self.draw_status()

    def add_item(self, name, amount=1):
        exists, item = self.check_for_item(name)

        if exists:
            item.amount += amount
            return

        asset_key = f"ITEM_{name.replace(' ', '_').upper()}"
        item_factory = self.item_dict.item_dict[name.upper()]
        item = item_factory(self.game.ASSETS[asset_key], amount)
        self.player.items.append(item)
        self.item_cards = []

        for item in self.player.items:
            self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    def check_for_item(self, name):
        if len(self.player.items) != 0:
            for item in self.player.items:
                if item.name.upper() == name.upper():
                    return True, item
            return False, None
        else:
            return False, None

    def _handle_item_input(self, keys, cur_time):

        if keys[pygame.K_UP] and cur_time - self.last_click > self.click_cooldown:
            self.item_selection.move_up()
            self.last_click = cur_time

        if keys[pygame.K_DOWN] and cur_time - self.last_click > self.click_cooldown:
            self.item_selection.move_down(len(self.player.items))
            self.last_click = cur_time

        if keys[pygame.K_RIGHT]:
            self.choosing_item = False

        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and cur_time - self.last_click > self.click_cooldown and self.player.items:
            current_item_idx = self.current_item
            self.player.items[current_item_idx].use(self.player.creatures[self.current_creature])
            self.last_click = cur_time
            if self.player.check_inventory():
                self.item_selection.reset()

    def _handle_creature_input(self, keys, cur_time):

        if keys[pygame.K_UP] and cur_time - self.last_click > self.click_cooldown:
            self.creature_selection.move_up()
            self.last_click = cur_time

        if keys[pygame.K_DOWN] and cur_time - self.last_click > self.click_cooldown:
            self.creature_selection.move_down(len(self.player.creatures))
            self.last_click = cur_time

        if keys[pygame.K_LEFT]:
            self.choosing_item = True
            self.last_click = cur_time

        if keys[pygame.K_d]:
            self.player.set_designated_creature(self.current_creature)

    def update(self, keys):

        cur_time = time()

        if self.choosing_item:
            self._handle_item_input(keys, cur_time)
        else:
            self._handle_creature_input(keys, cur_time)
