import pygame
from time import time

import items

class Item_card:
    
    def __init__(self, item):
        self.item = item
        self.card_surface = pygame.Surface((192, 48))
        
    def draw_card(self, font, is_current: bool):
        # Wypełnienie tła kolorem bazując na tym, czy dana karta jest w tym momencie
        # wybrana przez użytkownika 
        if is_current:
            self.card_surface.fill((180,180,180))
        else:
            self.card_surface.fill((120, 120, 120))
            
        # Renderowanie tekstu na podstawie nazwy przedmiotu    
        item_name, name_rect = font.render(f"{self.item.name}", (255,255,255))
        name_rect.center = name_rect.w // 2 + 48, 12
        
        # Renderowanie tekstu na podstawie ilości przedmiotu
        item_amount, amount_rect = font.render(f"Amount: {self.item.amount}", (255,255,255))
        amount_rect.center = amount_rect.w // 2 + 48, 36
        
        # Uzyskanie obrazu ikony przedmiotu oraz wytworzenie na jej podstawie prostokąta oraz
        # wyrysowanie go na powierzchni karty przedmiotu
        if self.item.icon is not None:
            icon_rect = self.item.icon.get_rect()
            icon_rect.center = 24, 24
            self.card_surface.blit(self.item.icon, icon_rect)
        
        # Wyrysowanie obu tekstów na karcie przedmiotu
        self.card_surface.blit(item_name, name_rect)
        self.card_surface.blit(item_amount, amount_rect)
        
        # Zwrócenie kompletnej karty przedmiotu
        return self.card_surface

class Inventory:
    
    def __init__(self, player):
        py = 48
        
        self._player = player
        self.item_cards = []
        self.surface = pygame.Surface((192, py * 5))
       
        self.current_item = 0
        self.click_cooldown = 0.15
        self.last_click = 0
        self.offset = 0
       
        py //= 2
        
        for item in self._player.items:
            self.item_cards.append(Item_card(item, py))
            py += 48
        
    def draw(self, font, screen):
        self.surface.fill((120,120,120))
        
        try:
            for x in range(5):
                if self.current_item % 5 == x:
                    card_surface = self.item_cards[x + self.offset * 5].draw_card(font, True)
                else:
                    card_surface = self.item_cards[x + self.offset * 5].draw_card(font, False)
                
                # Uzyskanie prostokąta na podstawie zwrócnej przez draw_card() karty przedmiotu
                # i ustawienie jego centrum w odpowiednim miejscu na powierzchni ekwipunku 
                card_surface_rect = card_surface.get_rect()
                card_surface_rect.center = 192 // 2, 24 + 48 * x
                
                # Wyrysowanie karty na powierzchni
                self.surface.blit(card_surface, card_surface_rect)
           
                # Wyrysowanie powierzchni na ekranie
                screen.blit(self.surface, self.surface.get_rect())
        except IndexError:
            pass
        
    def add_item(self, name, icon, amount):
        exists, item = self.check_for_item(name)
        print(exists, item)
        if exists:
            item.amount += amount
        else:
            item = items.Item(name, icon, amount)
            self._player.items.append(item)
            self.item_cards = []
            
            for item in self._player.items:
                self.item_cards.append(Item_card(item))
    
    def check_for_item(self, name):
        if len(self._player.items) != 0:
            for item in self._player.items:
                print(item)
                if item.name == name:
                    return True, item
            return False, None
        else:
            return False, None
    
    def update(self, keys):
        time_now = time()
        
        if keys[pygame.K_DOWN] and self.current_item < len(self.item_cards) - 1 and time_now - self.last_click > self.click_cooldown:
            self.current_item += 1
            self.last_click = time_now
            if self.current_item % 5 == 0:
                self.offset += 1
        
        if keys[pygame.K_UP] and self.current_item > 0 and time_now - self.last_click > self.click_cooldown:
            self.current_item -= 1 
            self.last_click = time_now
            if self.current_item % 5 == 4:
                self.offset -= 1
                
        if keys[pygame.K_c]:
            self.add_item(self._player.items[self.current_item].name, None, 1)
            print(self._player.items[self.current_item].name)