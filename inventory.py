import pygame

import items

class Item_card:
    def __init__(self, item, px = 128, py = 24):
        self.item = item
        self.rect = pygame.Rect(0, 0, 512, 48)
        self.rect.center = 128, py
        self.offset = py - 24

        
    def draw_card(self, font, surface):
        surface.fill((100,100,100))
        item_name, name_rect = font.render(f"{self.item.name}", (255,255,255))
        name_rect.center = name_rect.w // 2 + 48, 12 + self.offset
        item_amount, amount_rect = font.render(f"Amount: {self.item.amount}", (255,255,255))
        amount_rect.center = amount_rect.w // 2 + 48, 36 + self.offset
        icon_rect = self.item.icon.get_rect()
        icon_rect.center = 24, 24 + self.offset
        surface.blit(self.item.icon, icon_rect)
        surface.blit(item_name, name_rect)
        surface.blit(item_amount, amount_rect)
        

class Inventory:
    def __init__(self, player, py):
        self._player = player
        self.item_cards = []
        self.surface = pygame.Surface((192, py * 5))
        py = 24
        for item in self._player.items:
            self.item_cards.append(Item_card(item, py))
            py += 48
        
    def draw(self, font, screen, scale):
        try:
            for x in range(5):
                self.item_cards[x].draw_card(font, self.surface)
                self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() * scale, self.surface.get_height() * scale))
                screen.blit(self.surface, self.surface.get_rect())
        except IndexError:
            pass
        
    def add_item(self, name, icon, amount):
        item = items.Item(name, icon, amount)
        self._player.items.append(item)
        self.item_cards.append(Item_card(item, 128, 24))