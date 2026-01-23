import pygame

from src.entity import Entity

class NPC(Entity):
    def __init__(self, grid_pos: pygame.Vector2, image: pygame.Surface):
        super().__init__(grid_pos, image)

        

        pass

    def input(keys: pygame.key.ScancodeWrapper):
        pass

    def update(self, dt: float):
        pass
