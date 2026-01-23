import pygame

from src.player import Player
from src.asset_manager import AssetManager
from src.camera import Camera
from src.entity import Entity
from src.player import Player

class Scene:
    def __init__(self):
        self.bounds: pygame.Vector2 = pygame.Vector2(0, 0)
        self.entities: list[Entity] = []

        self.player: Player = None

    def load(self, asset_manager: AssetManager):
        pass

    def input(self, keys: pygame.key.ScancodeWrapper):
        pass

    def update(self, camera: Camera, dt: float):
        pass

    def render(self, window_surface: pygame.Surface, camera: Camera):
        pass