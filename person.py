import pygame
        
class Person(pygame.sprite.Sprite):
    def __init__(self, body_textures: list, px, py, accessories = []):
        super().__init__()
        if not isinstance(body_textures, (list, tuple)):
            body_textures = [body_textures]
        # Tekstury używane w zależności od obecnej orientacji postaci na mapie.
        self._body_textures = []
        for texture in body_textures:
            self._body_textures.append(texture)
        for accessory in accessories:
            self._body_textures.append(accessory)
        
        self._rectangles = []
        for x in self._body_textures:
            rectangle = x.get_rect()
            rectangle.center = px, py
            self._rectangles.append(rectangle)
        
    def draw(self, surface):
        for texture, rect in zip(self._body_textures, self._rectangles):
            surface.blit(texture, rect)
            
    def update(self):
        pass
        
        
        
class Player(Person):
    def __init__(self, body_texture: list, px, py, accessories = []):
        super().__init__(body_texture, px, py, accessories)
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        self.creatures = []
        
        self.moving = {
            "top": False,
            "bottom" : False,
            "right" : False,
            "left" : False,
        }

        
    def _start_sprint(self):
        self._movement_speed_multiplier = 1.5
    
    def _stop_sprint(self):
        self._movement_speed_multiplier = 1.0
            
    
    def _handle_events(self, keys_pressed, layers):
        if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
            self._start_sprint()
            
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        
        if keys_pressed[pygame.K_LEFT]:
            for rect in self._rectangles:
                rect.x -= movement * self.scale
            self.moving["left"] = True
            self.check_collision(layers)

            
        if keys_pressed[pygame.K_RIGHT]:
            for rect in self._rectangles:
                rect.x += movement * self.scale
            self.moving["right"] = True
            self.check_collision(layers)
            
            
        if keys_pressed[pygame.K_UP]:
            for rect in self._rectangles:
                rect.y -= movement * self.scale
            self.moving["top"] = True
            self.check_collision(layers)
            
            
        if keys_pressed[pygame.K_DOWN]:
            for rect in self._rectangles:
                rect.y += movement * self.scale
            self.moving["bottom"] = True
            self.check_collision(layers)
            
                        
        self.moving["left"] = False
        self.moving["right"] = False
        self.moving["top"] = False
        self.moving["bottom"] = False
        
        self.check_boundaries(layers)
        
        self._stop_sprint()
            
    def check_boundaries(self, layers):
        for tile in layers[0]:
            x, y = 0, 0
            if tile.x > x:
                x += tile.x
            if tile.y > y:
                y += tile.y

        for rect in self._rectangles:
            if rect.x > (x - 1) * 48 * self.scale:
                rect.x = (x - 1) * 48 * self.scale
            if rect.x < 0:
                rect.x = 0
            if rect.y > (y - 1) * 48 * self.scale:
                rect.y = (y - 1) * 48 * self.scale
            if rect.y < 0:
                rect.y = 0        
            
    def update(self, keys_pressed, layers):
        self._handle_events(keys_pressed, layers)
        
    def get_pos(self):
        return self._rectangles[0].center

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

    def check_collision(self, layers):
        for layer in layers:
            for tile in layer:
                if tile.rect.colliderect(self._rectangles[0]) and tile.impassable == True:
                    self.reverse_movement()
                    
    def read_scale(self, scale):
        self.scale = scale