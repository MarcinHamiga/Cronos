import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, body_texture: list, px, py, accessories=None):
        super().__init__()
        if accessories is None:
            accessories = []
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        self.orientation = 0
        self.items = []
        self.money = 0
        self.scale = 1
        
        if not isinstance(body_texture, (list, tuple)):
            body_texture = [body_texture]

        self._body_textures = []

        for texture in body_texture:
            self._body_textures.append(texture)

        for accessory in accessories:
            self._body_textures.append(accessory)

        self._rectangles = []

        for x in self._body_textures:
            rectangle = x.get_rect()
            rectangle.center = px, py
            self._rectangles.append(rectangle)

        self.moving = {
            "top": False,
            "bottom": False,
            "right": False,
            "left": False,
        }

    def _start_sprint(self):
        self._movement_speed_multiplier = 2.0

    def _stop_sprint(self):
        self._movement_speed_multiplier = 1.0

    def _handle_events(self, keys, layers):
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self._start_sprint()

        movement = int(self._movement_speed * self._movement_speed_multiplier)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for rect in self._rectangles:
                rect.x -= movement * self.scale
            self.moving["left"] = True
            self.check_collision(layers)
            self.moving["left"] = False
            self.orientation = 3

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["right"] = True
            self.check_collision(layers)
            self.moving["right"] = False
            self.orientation = 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["top"] = True
            self.check_collision(layers)
            self.moving["top"] = False
            self.orientation = 0

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["bottom"] = True
            self.check_collision(layers)
            self.moving["bottom"] = False
            self.orientation = 2

        self.check_boundaries(layers)

        self._stop_sprint()

    def check_boundaries(self, game):
        for tile in game.map.layers[0]:
            x, y = 0, 0
            if tile.x > x:
                x += tile.x
            if tile.y > y:
                y += tile.y

        for rect in self._rectangles:
            if rect.x > x * 48 * self.scale:
                rect.x = x * 48 * self.scale
            if rect.x < 0:
                rect.x = 0
            if rect.y > y * 48 * self.scale:
                rect.y = y * 48 * self.scale
            if rect.y < 0:
                rect.y = 0

    def update(self, keys, layers):
        self._handle_events(keys, layers)

    def get_pos(self):
        return self._rectangles[0].center

    def get_orient(self):
        return self.orientation

    def set_pos(self, coordinates: tuple):
        pos_x, pos_y = coordinates
        for rect in self._rectangles:
            rect.center = pos_x, pos_y

    def reverse_movement(self):
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        if self.moving["left"]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["left"] = False
        if self.moving["right"]:
            for rect in self._rectangles:
                rect.x -= movement * self.scale
            self.moving["right"] = False
        if self.moving["top"]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["top"] = False
        if self.moving["bottom"]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["bottom"] = False

    def check_collision(self, game):
        for layer in game.map.layers:
            for tile in layer:
                if tile.rect.colliderect(self._rectangles[0]) and tile.impassable:
                    self.reverse_movement()
                if len(tile.events) != 0:
                    for event in tile.events:
                        event.check_stepped_on(game)

    def read_scale(self, scale):
        self.scale = scale

    def get_rectangles(self):
        return self._rectangles

    def get_rectangle(self):
        return self._rectangles[0]

    def check_inventory(self):
        popped = False
        for idx, item in enumerate(self.items):
            if item.amount <= 0:
                self.items.pop(idx)
                popped = True
        return popped

    def draw(self, surface):
        for texture, rect in zip(self._body_textures, self._rectangles):
            surface.blit(texture, rect)
