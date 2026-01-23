import pygame

from src.entity import Entity
from src.camera import Camera

class Player(Entity):
    def __init__(self, grid_pos: pygame.Vector2, image: pygame.Surface, move_duration: int):
        super().__init__(grid_pos, image)

        self.pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.moving: bool = False
        self.move_dir: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_time: float = 0.0
        self.move_duration: float = move_duration

    def set_image(self, image: pygame.Surface):
        self.surface = image
        self.dimensions = pygame.Vector2(self.surface.get_width(), self.surface.get_height())
        self.pos = self.grid_pos * self.dimensions.x

    def input(self, keys: pygame.key.ScancodeWrapper):
        if self.moving:
            return
        
        dx: int = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy: int = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        if dx != 0:
            dy = 0

        if dx != 0 or dy != 0:
            self.move_dir = pygame.Vector2(dx, dy)
            self.moving = True
            self.move_time = 0.0

    def update(self, dt: float):
        if not self.moving:
            return
        
        self.move_time += dt
        t: float = min(self.move_time / self.move_duration, 1.0)

        start_pos: pygame.Vector2 = self.grid_pos * self.dimensions.x
        target_pos: pygame.Vector2 = (self.grid_pos + self.move_dir) * self.dimensions.x

        self.pos = start_pos.lerp(target_pos, t)

        if t >= 1.0:
            self.grid_pos += self.move_dir
            self.moving = False

    def render(self, surface: pygame.Surface, camera: Camera):
        centered: pygame.Vector2 = self.pos - self.dimensions / 2
        surface.blit(self.surface, camera.world_pos_to_view_pos(centered))