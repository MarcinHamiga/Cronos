import pygame
from time import time

from src.inventory import DynamicItemCard, SelectionWindow


class Shopscreen:

    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 2
        self.buyable_items = [x for x in self.game.INVENTORY.shop_dict.shop_dict.values() if x.buyable is True]
        self.buying = False
        self.inventory_selection = SelectionWindow(page_size=5)
        self.shop_selection = SelectionWindow(page_size=6)
        self.item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.game.PLAYER.items]
        self.shop_item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT, print_price=True) for item in self.buyable_items]
        self.last_click = time()
        self.cooldown = 0.15

        self.money_icon = self.game.ASSETS["ITEM_MONEY"]
        self.money_icon = pygame.transform.scale(self.money_icon, (self.game.SCR_HEIGHT // 12, self.game.SCR_HEIGHT // 12))
        self.money_icon_rect = self.money_icon.get_rect()
        self.money_icon_rect.center = self.game.SCR_HEIGHT // 12, self.game.SCR_HEIGHT // 12

        self.refreshed = False

    @property
    def current_item_inv(self):
        return self.inventory_selection.current_index

    @property
    def offset(self):
        return self.inventory_selection.offset

    @property
    def current_item_shop(self):
        return self.shop_selection.current_index

    @property
    def offset_shop(self):
        return self.shop_selection.offset

    def draw_inv(self):
        visible_indexes = list(self.inventory_selection.visible_indexes(len(self.item_cards)))
        for draw_index, item_index in enumerate(visible_indexes):
            card_surface = self.item_cards[item_index].draw_card(item_index == self.current_item_inv)
            card_surface_rect = card_surface.get_rect()
            card_surface_rect.center = self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + draw_index * self.game.SCR_HEIGHT // 6
            self.game.SCREEN.blit(card_surface, card_surface_rect)

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
        visible_indexes = list(self.shop_selection.visible_indexes(len(self.shop_item_cards)))
        for draw_index, item_index in enumerate(visible_indexes):
            card_surface = self.shop_item_cards[item_index].draw_card(item_index == self.current_item_shop)
            card_surface_rect = card_surface.get_rect()
            card_surface_rect.center = 3 * self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + draw_index * self.game.SCR_HEIGHT // 6
            self.game.SCREEN.blit(card_surface, card_surface_rect)

    def draw(self):
        self.game.SCREEN.fill((0, 0, 0))
        self.draw_inv()
        self.draw_shop()

    def update(self, keys):
        cur_time = time()

        match self.buying:

            case True:
                if keys[pygame.K_UP] and cur_time - self.last_click > self.cooldown:
                    self.shop_selection.move_up()
                    self.last_click = cur_time

                if keys[pygame.K_DOWN] and cur_time - self.last_click > self.cooldown:
                    self.shop_selection.move_down(len(self.buyable_items))
                    self.last_click = cur_time

                if keys[pygame.K_LEFT] and cur_time - self.last_click > self.cooldown:
                    self.buying = False
                    self.last_click = cur_time

                if keys[pygame.K_RETURN] and cur_time - self.last_click > self.cooldown:
                    self.buy()
                    self.last_click = cur_time

            case False:
                if keys[pygame.K_UP] and cur_time - self.last_click > self.cooldown:
                    self.inventory_selection.move_up()
                    self.last_click = cur_time

                if keys[pygame.K_DOWN] and cur_time - self.last_click > self.cooldown:
                    self.inventory_selection.move_down(len(self.game.PLAYER.items))
                    self.last_click = cur_time

                if keys[pygame.K_RIGHT] and cur_time - self.last_click > self.cooldown:
                    self.buying = True
                    self.last_click = cur_time

                if keys[pygame.K_RETURN] and cur_time - self.last_click > self.cooldown:
                    self.sell()
                    self.last_click = cur_time

    def buy(self):
        if not self.buyable_items:
            return

        item = self.buyable_items[self.current_item_shop]
        if self.game.PLAYER.money >= item.price:
            self.set_for_refresh()
            self.game.PLAYER.money -= item.price
            for player_item in self.game.PLAYER.items:
                if player_item.__class__.__name__ == item.__class__.__name__:
                    player_item.amount += 1
                    self.refresh()
                    return
            self.game.INVENTORY.add_item(item.name)
            self.refresh()

    def sell(self):
        if not self.game.PLAYER.items:
            return

        item = self.game.PLAYER.items[self.current_item_inv]
        item.amount -= 1
        if item.amount == 0 and self.current_item_inv != 0:
            self.inventory_selection.current_index -= 1
            if self.inventory_selection.current_index % self.inventory_selection.page_size == self.inventory_selection.page_size - 1:
                self.inventory_selection.offset -= 1

        self.set_for_refresh()
        self.refresh()
        self.game.INVENTORY.check_for_strays()

        if item.__class__.__name__ == "Junk":
            self.game.PLAYER.money += item.price
        else:
            self.game.PLAYER.money += item.price // 2

        self.game.INVENTORY.check_for_strays()

    def refresh(self):
        if not self.refreshed:
            self.item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.game.PLAYER.items]
            self.refreshed = True

    def set_for_refresh(self):
        self.refreshed = False
