import pygame

from src.camera import Camera

class Entity:
    def __init__(self, grid_pos: pygame.Vector2, image: pygame.Surface):
        self.grid_pos: pygame.Vector2 = grid_pos
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.surface: pygame.Surface = image
        self.dimensions: pygame.Vector2 = pygame.Vector2(image.get_width(), image.get_height()) 

    def set_image(self, image: pygame.Surface):
        self.surface = image
        self.dimensions = pygame.Vector2(self.surface.get_width(), self.surface.get_height())

    def input(self, keys: pygame.key.ScancodeWrapper):
        pass

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface, camera: Camera):
        surface.blit(self.surface, camera.grid_pos_to_view_pos(self.grid_pos))