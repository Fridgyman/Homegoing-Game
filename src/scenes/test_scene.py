import pygame

from src.scenes.scene import Scene
from src.player import Player
from src.asset_manager import AssetManager
from src.camera import Camera
from src.entity import Entity

class TestScene(Scene):
    def __init__(self):
        super().__init__()
        self.bounds = pygame.Vector2(3000, 3000)

    def load(self, asset_manager: AssetManager):
        self.player = Player(pygame.Vector2(0, 0), asset_manager.get_image("null.png"), 0.15)
        self.player.grid_pos = (self.bounds // self.player.dimensions.x) // 2
        self.player.pos = self.player.grid_pos * self.player.dimensions.x

    def input(self, keys: pygame.key.ScancodeWrapper):
        self.player.input(keys)
        for entity in self.entities: entity.input(keys)

    def update(self, camera: Camera, dt: float):
        camera.center(self.player.pos, self.bounds)

        self.player.update(dt)
        self.player.pos.x = max(0, min(self.player.pos.x, self.bounds.x - self.player.dimensions.x))
        self.player.pos.y = max(0, min(self.player.pos.y, self.bounds.y - self.player.dimensions.y))

        for entity in self.entities: entity.update(dt)

    def render(self, window_surface: pygame.Surface, camera: Camera):
        window_surface.fill((70, 120, 70))

        for x in range(16, int(self.bounds.x) + 32, 32):
            pygame.draw.line(
                window_surface, (90, 140, 90), 
                camera.world_pos_to_view_pos(pygame.Vector2(x, 0)),
                camera.world_pos_to_view_pos(pygame.Vector2(x, self.bounds.y))
            )
        for y in range(16, int(self.bounds.y) + 32, 32):
            pygame.draw.line(
                window_surface, (90, 140, 90), 
                camera.world_pos_to_view_pos(pygame.Vector2(0, y)),
                camera.world_pos_to_view_pos(pygame.Vector2(self.bounds.x, y))
            )

        for entity in self.entities: entity.render(window_surface, camera)
        self.player.render(window_surface, camera)