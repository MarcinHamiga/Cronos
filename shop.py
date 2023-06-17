import pygame
from inventory import DynamicItemCard
class Shopscreen:

    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((self.game.SCR_WIDTH, self.game.SCR_HEIGHT))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = self.game.SCR_WIDTH // 2, self.game.SCR_HEIGHT // 2
        self.buyable_items = [x for x in self.game.INVENTORY.item_dict.item_dict.values() if x.buyable is True]
        self.buying = False
        self.current_item_inv = 0
        self.offset = 0
        self.current_item_shop = 0
        self.offset_shop = 0
        self.item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.game.PLAYER.items]
        self.shop_item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.buyable_items]

        self.money_icon = self.game.ASSETS["ITEM_JUNK"]
        self.money_icon = pygame.transform.scale(self.money_icon, (self.game.SCR_HEIGHT // 6, self.game.SCR_HEIGHT // 6))
        self.money_icon_rect = self.money_icon.get_rect()
        self.money_icon_rect.center = self.game.SCR_HEIGHT // 12, self.game.SCR_HEIGHT // 12

    def draw_inv(self):

        if len(self.game.PLAYER.items) != len(self.item_cards):
            self.item_cards = [DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT) for item in self.game.PLAYER.items]

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
        pass

    def draw(self):
        self.draw_inv()
        self.draw_shop()

    def update(self, keys):

        if keys[pygame.K_UP]:

        if keys[pygame.K_DOWN]:

        if keys[pygame.K_RIGHT]:

        if keys[pygame.K_LEFT]: