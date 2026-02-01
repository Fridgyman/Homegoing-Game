import pygame

from src.asset_manager import AssetManager
from src.camera import Camera
from src.config import Config
from src.sprite import Sprite
from src.sprite import dir_to_str
from src.ui_manager import UIManager


class Entity:
    def __init__(self, grid_pos: pygame.Vector2, sprite: Sprite, collision: bool):
        self.grid_pos: pygame.Vector2 = grid_pos
        self.facing: pygame.Vector2 = pygame.Vector2(0, 1)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)

        self.sprite: Sprite = sprite
        self.hit_box: pygame.Vector2 = self.sprite.dimensions / Config.TILE_SIZE

        self.collision: bool = collision

    def set_sprite(self, sprite: Sprite, hit_box: pygame.Vector2) -> None:
        self.sprite = sprite
        self.hit_box = hit_box

    def get_collision(self, rect: pygame.Rect) -> bool:
        return self.collision and rect.colliderect(pygame.Rect(self.grid_pos, self.hit_box))

    def look_at(self, grid_pos: pygame.Vector2) -> None:
        diff: pygame.Vector2 = self.grid_pos - grid_pos
        if diff.x == 0 and diff.y == 0:
            return

        if abs(diff[1]) > abs(diff[0]):
            self.facing = pygame.Vector2(0, -diff[1] / abs(diff[1]))
        else:
            self.facing = pygame.Vector2(-diff[0] / abs(diff[0]), 0)

    def input(self, keys: pygame.key.ScancodeWrapper) -> None:
        pass

    def update(self, ui_manager: UIManager, dt: float) -> None:
        self.sprite.set(dir_to_str(self.velocity, self.facing))
        self.sprite.update(dt)

    def render(self, surface: pygame.Surface, camera: Camera) -> None:
        centered: pygame.Vector2 = self.grid_pos * Config.TILE_SIZE - self.sprite.dimensions / 2
        centered.x -= self.sprite.dimensions.y - Config.TILE_SIZE
        surface.blit(self.sprite.get() or AssetManager.NULL_IMAGE, camera.world_pos_to_view_pos(centered))