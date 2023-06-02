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
        
        # 0 - postać jest przodem do gracza, 1 - postać jest tyłem do gracza
        # 2 - postać jest zwrócona lewą stroną do gracza, 3 - postać jest zwrócona prawą stroną do gracza
        self._rectangles = []
        for x in self._body_textures:
            rectangle = x.get_rect()
            rectangle.center = px, py
            self._rectangles.append(rectangle)
        
    def draw(self, surface):
        for texture, rect in zip(self._body_textures, self._rectangles):
            surface.blit(texture, rect)
        
        
        
class Player(Person):
    def __init__(self, body_texture: list, px, py, accessories = []):
        super().__init__(body_texture, px, py, accessories)
        self._movement_speed = 3
        self._movement_speed_multiplier = 1.0
        
    def _start_sprint(self):
        self._movement_speed_multiplier = 1.5
    
    def _stop_sprint(self):
        self._movement_speed_multiplier = 1.0
            
    
    def _handle_events(self, keys_pressed):
        if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
            self._start_sprint()
        movement = int(self._movement_speed * self._movement_speed_multiplier)
        if keys_pressed[pygame.K_LEFT]:
            for rect in self._rectangles:
                rect.move_ip([int(-movement), 0])
        if keys_pressed[pygame.K_RIGHT]:
            for rect in self._rectangles:
                rect.move_ip([movement, 0])
        if keys_pressed[pygame.K_UP]:
            for rect in self._rectangles:
                rect.move_ip([0, -movement])
        if keys_pressed[pygame.K_DOWN]:
            for rect in self._rectangles:
                rect.move_ip([0, movement])
        self._stop_sprint()
            
    def update(self, keys_pressed):
        self._handle_events(keys_pressed)