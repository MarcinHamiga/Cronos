import pygame
from time import time

from ..data.items import Item_dict, Shop_dict


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
            self.card_surface.fill((180,180,180))
        else:
            self.card_surface.fill((128, 0, 35))

        item_name, name_rect = font.render(f"{self.item.name}", (255,255,255))
        name_rect.center = name_rect.w // 2 + 48, 12

        item_amount, amount_rect = font.render(f"Amount: {self.item.amount}", (255,255,255))
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


class Inventory:

    def __init__(self, game):
        assets = game.ASSETS
        self.player = game.PLAYER
        self.item_dict = Item_dict(assets)
        self.shop_dict = Shop_dict(assets)
        self.game = game

        self.item_cards = []

        self.current_item = 0
        self.offset = 0

        self.click_cooldown = 0.15
        self.last_click = 0

        for item in self.player.items:
            self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    def check_for_strays(self):
        for idx, item in enumerate(self.player.items):
            if item.amount == 0:
                self.player.items.pop(idx)

    def _check_card_integrity(self):

        self.check_for_strays()

        if len(self.item_cards) != len(self.player.items):
            self.item_cards = []
            for item in self.player.items:
                self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    def draw_items(self):
        try:
            for x in range(6):
                if self.current_item % 6 == x:
                    card_surface = self.item_cards[x + self.offset * 6].draw_card(True)
                else:
                    card_surface = self.item_cards[x + self.offset * 6].draw_card(False)

                card_surface_rect = card_surface.get_rect()
                card_surface_rect.center = self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + x * self.game.SCR_HEIGHT // 6

                self.game.SCREEN.blit(card_surface, card_surface_rect)
        except IndexError:
            pass

    def draw(self):
        self._check_card_integrity()
        self.draw_items()

    def add_item(self, name, amount=1):
        exists, item = self.check_for_item(name)

        if exists:
            item.amount += amount
            amount = 0
            return
        else:
            prefix = "ITEM_"
            new_name = ""
            for char in name:
                if char == " ":
                    new_name += "_"
                else:
                    new_name += char
            item = self.item_dict.item_dict[name.upper()](self.game.ASSETS[prefix + new_name.upper()], amount)
            self.player.items.append(item)
            self.item_cards = []

            for item in self.player.items:
                self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    def check_for_item(self, name):
        if len(self.player.items) != 0:

            for item in self.player.items:
                if item.name == name:
                    return True, item

            return False, None

        else:
            return False, None

    def _handle_item_input(self, keys, cur_time):

        if keys[pygame.K_UP] and cur_time - self.last_click > self.click_cooldown and self.current_item > 0:
            self.current_item -= 1
            self.last_click = cur_time
            if self.current_item % 6 == 5:
                self.offset -= 1

        if keys[pygame.K_DOWN] and cur_time - self.last_click > self.click_cooldown and self.current_item < len(self.player.items) - 1:
            self.current_item += 1
            self.last_click = cur_time
            if self.current_item % 6 == 0:
                self.offset += 1

    def update(self, keys):

        cur_time = time()
        self._handle_item_input(keys, cur_time)
