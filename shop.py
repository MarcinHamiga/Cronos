import pygame
from inventory import DynamicItemCard
from copy import deepcopy
from time import time


class Shopscreen:

    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 2
        self.buyable_items = [x for x in self.game.INVENTORY.shop_dict.shop_dict.values() if x.buyable is True]
        self.buying = False
        self.current_item_inv = 0
        self.offset = 0
        self.current_item_shop = 0
        self.offset_shop = 0
        self.item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.game.PLAYER.items]
        self.shop_item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.buyable_items]
        self.last_click = time()
        self.cooldown = 0.15

        self.money_icon = self.game.ASSETS["ITEM_MONEY"]
        self.money_icon = pygame.transform.scale(self.money_icon, (self.game.SCR_HEIGHT // 12, self.game.SCR_HEIGHT // 12))
        self.money_icon_rect = self.money_icon.get_rect()
        self.money_icon_rect.center = self.game.SCR_HEIGHT // 12, self.game.SCR_HEIGHT // 12

        self.refreshed = False

    def draw_inv(self):
        if self.current_item_inv < 0:
            self.current_item_inv = 0
        try:
            for x in range(5):
                if self.current_item_inv % 5 == x:
                    card_surface = self.item_cards[x + self.offset * 5].draw_card(True)
                else:
                    card_surface = self.item_cards[x + self.offset * 5].draw_card(False)

                print(card_surface.get_width(), card_surface.get_height())
                card_surface_rect = card_surface.get_rect()
                card_surface_rect.center = self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + x * self.game.SCR_HEIGHT // 6

                self.game.SCREEN.blit(card_surface, card_surface_rect)

        except IndexError:
            pass

        money_surf = pygame.Surface((self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 6))
        money_surf.fill((128, 0, 35))
        money_rect = money_surf.get_rect()
        money_rect.center = self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + 5 * self.game.SCR_HEIGHT // 6
        money_surf.blit(self.money_icon, self.money_icon_rect)
        money_amount, money_amount_rect = self.game.FONT.render(f"Amount: {self.game.PLAYER.money}", size=self.game.SCR_HEIGHT // 24)
        money_amount_rect.center = money_rect.w // 2, money_rect.h // 2
        money_surf.blit(money_amount, money_amount_rect)
        self.game.SCREEN.blit(money_surf, money_rect)

    def draw_shop(self):
        try:
            for x in range(6):
                if self.current_item_shop % 6 == x:
                    card_surface = self.shop_item_cards[x + self.offset_shop * 6].draw_card(True)
                else:
                    card_surface = self.shop_item_cards[x + self.offset_shop * 6].draw_card(False)

                print(card_surface.get_width(), card_surface.get_height())
                card_surface_rect = card_surface.get_rect()
                card_surface_rect.center = 3 * self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + x * self.game.SCR_HEIGHT // 6

                self.game.SCREEN.blit(card_surface, card_surface_rect)
        except IndexError:
            pass

    def draw(self):
        self.game.SCREEN.fill((0, 0, 0))
        self.draw_inv()
        self.draw_shop()

    def update(self, keys):
        cur_time = time()

        match self.buying:

            case True:
                if keys[pygame.K_UP] and cur_time - self.last_click > self.cooldown and self.current_item_shop > 0:
                    self.current_item_shop -= 1
                    self.last_click = cur_time
                    if self.current_item_shop % 6 == 5:
                        self.offset_shop -= 1

                if keys[pygame.K_DOWN] and cur_time - self.last_click > self.cooldown and self.current_item_shop < len(self.buyable_items) - 1:
                    self.current_item_shop += 1
                    self.last_click = cur_time
                    if self.current_item_shop % 6 == 0:
                        self.offset_shop += 1

                if keys[pygame.K_LEFT] and cur_time - self.last_click > self.cooldown:
                    self.buying = False

                if keys[pygame.K_RETURN] and cur_time - self.last_click > 0.15:
                    self.buy()
                    self.last_click = cur_time

            case False:
                if keys[pygame.K_UP] and cur_time - self.last_click > self.cooldown and self.current_item_inv > 0:
                    self.current_item_inv -= 1
                    self.last_click = cur_time
                    if self.current_item_inv % 5 == 4:
                        self.offset -= 1

                if keys[pygame.K_DOWN] and cur_time - self.last_click > self.cooldown and self.current_item_inv < len(self.game.PLAYER.items) - 1:
                    self.current_item_inv += 1
                    self.last_click = cur_time
                    if self.current_item_inv % 5 == 0:
                        self.offset += 1

                if keys[pygame.K_RIGHT] and cur_time - self.last_click > self.cooldown:
                    self.buying = True

                if keys[pygame.K_RETURN] and cur_time - self.last_click > 0.15:
                    self.sell()
                    self.last_click = cur_time

    def buy(self):

        if self.game.PLAYER.money >= self.buyable_items[self.current_item_shop].price:
            self.set_for_refresh()
            item = self.buyable_items[self.current_item_shop]
            self.game.PLAYER.money -= item.price
            for player_item in self.game.PLAYER.items:
                if player_item.__class__.__name__ == item.__class__.__name__:
                    player_item.amount += 1
                    return
            self.game.INVENTORY.add_item(item.name.upper())
            self.refresh()
            print(self.game.PLAYER.items)

    def sell(self):

        try:
            item = self.game.PLAYER.items[self.current_item_inv]
            item.amount -= 1
            if item.amount == 0 and self.current_item_inv != 0:
                self.current_item_inv -= 1
            if item.__class__.__name__ == "Junk":
                self.game.PLAYER.money += self.game.PLAYER.items[self.current_item_inv].price
            else:
                self.game.PLAYER.money += self.game.PLAYER.items[self.current_item_inv].price // 2
            self.game.INVENTORY.check_for_strays()

        except IndexError:
            self.current_item_inv -= 1
            if self.current_item_inv % 5 == 4:
                self.offset -= 1
            self.set_for_refresh()
            self.refresh()
            self.game.INVENTORY.check_for_strays()

    def refresh(self):
        if not self.refreshed:
            self.item_cards = []
            self.item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.game.PLAYER.items]
            self.refreshed = True

    def set_for_refresh(self):
        self.refreshed = False