import random

import pygame

from src.config import Config


def grid_pos_to_view_pos(grid_pos: pygame.Vector2) -> pygame.Vector2:
    return grid_pos * Config.TILE_SIZE


class Camera:
    POS: pygame.Vector2 = pygame.Vector2(0, 0)
    WINDOW_CENTER: int = 0

    SHAKE_OFFSET: pygame.Vector2 = pygame.Vector2(0, 0)
    SHAKE_AMOUNT: pygame.Vector2 = pygame.Vector2(0, 0)
    SHAKE_DURATION: float = 0

    ZOOM: float = 1

    TRACK = None

    @classmethod
    def init_window_center(cls) -> None:
        cls.WINDOW_CENTER = Config.WINDOW_DIMS // 2

    @classmethod
    def center_at(cls, pos: pygame.Vector2, bounds: pygame.Vector2) -> None:
        cls.POS = pos - cls.WINDOW_CENTER
        cls.clamp_pos(bounds)

    @classmethod
    def clamp_pos(cls, bounds: pygame.Vector2) -> None:
        cls.POS.x = pygame.math.clamp(cls.POS.x, 0, (bounds.x - 1) * Config.TILE_SIZE - Config.WINDOW_DIMS.x)
        cls.POS.y = pygame.math.clamp(cls.POS.y, 0, (bounds.y - 1) * Config.TILE_SIZE - Config.WINDOW_DIMS.y)

    @classmethod
    def update(cls, bounds: pygame.Vector2, dt: float) -> None:
        cls.SHAKE_OFFSET = cls._get_shake_offset(dt)
        if cls.TRACK is not None:
            cls.center_at(cls.TRACK.pos, bounds)

    @classmethod
    def world_pos_to_view_pos(cls, world_pos: pygame.Vector2) -> pygame.Vector2:
        return world_pos - cls.POS + cls.SHAKE_OFFSET

    @classmethod
    def shake_camera(cls, intensity_x=10, intensity_y=10, duration=0.5) -> None:
        cls.SHAKE_AMOUNT.x = intensity_x
        cls.SHAKE_AMOUNT.y = intensity_y
        cls.shake_duration = duration

    @classmethod
    def _get_shake_offset(cls, dt: float) -> pygame.Vector2:
        if cls.SHAKE_DURATION > 0:
            fraction = cls.SHAKE_DURATION / max(cls.SHAKE_DURATION + dt, 0.01)
            current_x = cls.SHAKE_AMOUNT.x * fraction
            current_y = cls.SHAKE_AMOUNT.y * fraction
            offset_x = random.uniform(-current_x, current_x)
            offset_y = random.uniform(-current_y, current_y)
            
            cls.SHAKE_DURATION -= dt
            return pygame.Vector2(offset_x, offset_y)
        
        cls.SHAKE_AMOUNT.x = 0
        cls.SHAKE_AMOUNT.y = 0
        return pygame.Vector2(0, 0)
