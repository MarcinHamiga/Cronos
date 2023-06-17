from copy import deepcopy

import pygame
from time import time

import items


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
        # Wypełnienie tła kolorem bazując na tym, czy dana karta jest w tym momencie
        # wybrana przez użytkownika 
        if is_current:
            self.card_surface.fill((180,180,180))
        else:
            self.card_surface.fill((128, 0, 35))
            
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

        print(self.card_surface.get_width(), self.card_surface.get_height())
        
        # Zwrócenie kompletnej karty przedmiotu
        return self.card_surface


# Ten obiekt typu ItemCard skaluje się do rozdzielczości ekranu użytkownika. Zajmuje zawsze 1/2 szerokości ekranu
# i 1/6 jego wysokości
class DynamicItemCard:

    def __init__(self, item, scr_width, scr_height, font):
        surf_w, surf_h = scr_width // 2, scr_height // 6
        self.surface = pygame.Surface((surf_w, surf_h))
        self.surface_rect = self.surface.get_rect()

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

        self.name, self.name_rect = font.render(f"Name: {self.creature.name}", size=32, fgcolor=(0, 0, 0))
        self.name_rect.center = self.surface_rect.w // 2 + self.image_rect.w, self.surface_rect.h // 4

    def draw_card(self, is_current):
        if is_current:
            self.surface.fill((255, 255, 255))
        else:
            self.surface.fill((128, 0, 35))

        amount, amount_rect = self.font.render(f"Lvl: {self.creature.level}, HP:{self.creature.health}/{self.creature.max_health}", size=32, fgcolor=(0, 0, 0))
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

        data, data_rect = font.render(f"Name: {self.creature.name}", size=self.font_size)
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

        self.current_item = 0
        self.offset = 0

        self.current_creature = 0
        self.creature_offset = 0

        self.choosing_item = True

        self.click_cooldown = 0.15
        self.last_click = 0

        for item in self.player.items:
            self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

        for creature in self.player.creatures:
            self.creature_cards.append(DynamicCreatureCard(creature, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

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
        try:
            for x in range(6):
                if self.current_item % 6 == x:
                    card_surface = self.item_cards[x + self.offset * 6].draw_card(True)
                else:
                    card_surface = self.item_cards[x + self.offset * 6].draw_card(False)

                print(card_surface.get_width(), card_surface.get_height())
                card_surface_rect = card_surface.get_rect()
                card_surface_rect.center = self.game.SCR_WIDTH // 4, self.game.SCR_HEIGHT // 12 + x * self.game.SCR_HEIGHT // 6

                self.game.SCREEN.blit(card_surface, card_surface_rect)
        except IndexError:
            pass

    def draw_creatures(self):
        try:
            for x in range(3):
                if self.current_creature % 3 == x:
                    card_surface = self.creature_cards[x + self.creature_offset * 3].draw_card(True)
                else:
                    card_surface = self.creature_cards[x + self.creature_offset * 3].draw_card(False)

                print(card_surface.get_width(), card_surface.get_height())
                card_surface_rect = card_surface.get_rect()
                card_surface_rect.center = self.game.SCR_WIDTH // 4 + self.game.SCR_WIDTH // 2, (self.game.SCR_HEIGHT // 2 + self.game.SCR_HEIGHT // 12) + x * self.game.SCR_HEIGHT // 6

                self.game.SCREEN.blit(card_surface, card_surface_rect)
        except IndexError:
            pass

    def draw(self):
        self._check_card_integrity()
        self.draw_creatures()
        self.draw_items()
        self.draw_status()

    def add_item(self, name, amount=1):
        """Dodaje wybrany przedmiot do ekwipunku"""

        # Rozpakowuje zwracane przez check_for_item() wartości
        exists, item = self.check_for_item(name)

        # Jeżeli sprawdzenie zwróciło prawdę, to zamiast tworzyć nowy obiekt typu item,
        # zwyczajnie zwiększamy ilość istniejącego już przedmiotu o zadaną wartość amount
        if exists:
            item.amount += amount
            amount = 0
            return
        # W przeciwnym wypadku, dodajemy nowy obiekt typu Item do listy z ustawioną wartością
        # zmiennej amount na wskazaną przez nas ilość
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
            # Aby uniknąć problemów, lista kart przedmiotów jest zerowana i zapełniana na nowo, kiedy
            # w ekwipunku pojawia się całkiem nowy przedmiot
            self.item_cards = []

            for item in self.player.items:
                self.item_cards.append(DynamicItemCard(item, self.game.SCR_WIDTH, self.game.SCR_HEIGHT, self.game.FONT))

    def check_for_item(self, name):
        """Sprawdza czy przedmiot już istnieje w ekwipunku"""

        # Jeżeli gracz posiada jakieś przedmioty, to funkcja iteruje po nich
        # i porównuje ich nazwę do tej, której szukamy
        if len(self.player.items) != 0:

            for item in self.player.items:
                # Jeżeli przedmiot zostanie odnaleziony, to zwracana jest wartość
                # True oraz sam przedmiot, aby móc łatwo zmienić wartość jego
                # parametru amount
                if item.name == name:
                    return True, item

            # Jeżeli poszukiwany przedmiot nie zostanie odnaleziony, to funkcja zwraca wartość
            # False i None
            return False, None

        # Jeżeli lista jest pusta, to funkcja zwraca wartości domyślne False i None
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

        if keys[pygame.K_RIGHT]:
            self.choosing_item = False

        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and cur_time - self.last_click > self.click_cooldown:
            current_item_idx = self.current_item + self.offset * self.current_item
            current_creature_idx = self.current_creature + self.creature_offset * self.current_creature
            self.player.items[current_item_idx].use(self.player.creatures[current_creature_idx])
            self.last_click = cur_time
            if self.player.check_inventory():
                self.current_item = 0
                self.offset = 0

    def _handle_creature_input(self, keys, cur_time):

        if keys[pygame.K_UP] and cur_time - self.last_click > self.click_cooldown and self.current_creature > 0:
            self.current_creature -= 1
            self.last_click = cur_time
            if self.current_creature % 3 == 2:
                self.creature_offset -= 1

        if keys[pygame.K_DOWN] and cur_time - self.last_click > self.click_cooldown and self.current_creature < len(
                self.player.creatures) - 1:
            self.current_creature += 1
            self.last_click = cur_time
            if self.current_creature % 3 == 0:
                self.creature_offset += 1

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

