import pygame

from src.asset_manager import AssetManager
from src.camera import Camera
from src.config import Config
from src.entity import Entity
from src.map_element import MapElement
from src.sprite import Sprite
from src.sprite import dir_to_str
from src.ui_manager import UIManager


class Player(Entity):
    def __init__(self, grid_pos: pygame.Vector2, sprite: Sprite, move_duration: float):
        super().__init__(grid_pos, sprite, False)

        self.pos: pygame.Vector2 = grid_pos * Config.TILE_SIZE
        self.moving: bool = False
        self.move_time: float = 0.0
        self.move_duration: float = move_duration

    def set_sprite(self, sprite: Sprite, hit_box: pygame.Vector2) -> None:
        self.sprite = sprite
        self.hit_box = hit_box
        self.pos = self.grid_pos * Config.TILE_SIZE

    def input(self, keys: pygame.key.ScancodeWrapper) -> None:
        if self.moving:
            return
        
        dx: int = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy: int = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        if dx != 0:
            dy = 0

        if dx != 0 or dy != 0:
            self.velocity = pygame.Vector2(dx, dy)
            self.facing = self.velocity
            self.moving = True
            self.move_time = 0.0

    def update(self, entities: list[Entity], map_elements: list[MapElement], ui_manager: UIManager, dt: float) -> None:
        self.sprite.set(dir_to_str(self.velocity, self.facing))
        self.sprite.update(dt)

        if not self.moving:
            return

        target_grid_pos: pygame.Vector2 = self.grid_pos + self.velocity
        rect: pygame.Rect = pygame.Rect(target_grid_pos, self.hit_box)
        for entity in entities:
            if entity.get_collision(rect):
                self.moving = False
                self.velocity = pygame.Vector2(0, 0)
                self.move_time = 0
                return

        for map_element in map_elements:
            if map_element.get_collision(rect):
                self.moving = False
                self.velocity = pygame.Vector2(0, 0)
                self.move_time = 0
                return
        
        self.move_time += dt
        t: float = min(self.move_time / self.move_duration, 1.0)

        start_pos: pygame.Vector2 = self.grid_pos * 32
        target_pos: pygame.Vector2 = target_grid_pos * 32

        self.pos = start_pos.lerp(target_pos, t)

        if t >= 1.0:
            self.grid_pos += self.velocity
            self.velocity = pygame.Vector2(0, 0)
            self.moving = False

    def render(self, surface: pygame.Surface, camera: Camera) -> None:
        centered: pygame.Vector2 = self.pos - self.sprite.dimensions / 2
        surface.blit(self.sprite.get() or AssetManager.NULL_IMAGE, camera.world_pos_to_view_pos(centered))