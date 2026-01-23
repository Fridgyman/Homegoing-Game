import pygame

from src.scenes import scene
from src.player import Player
from src.asset_manager import AssetManager
from src.camera import Camera

import os

class SceneManager:
    def __init__(self):
        self.scenes: dict[str, scene.Scene] = {}
        self.current_scene: str = ""

    def add_scene(self, name: str, scene: scene.Scene) -> None:
        self.scenes[name] = scene

    def load_scene(self, scene_name: str, asset_manager: AssetManager) -> None:
        self.scenes[scene_name].load(asset_manager)
        self.current_scene = scene_name

    def input(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.scenes[self.current_scene].input(keys)

    def update(self, camera: Camera, dt: float) -> None:
        self.scenes[self.current_scene].update(camera, dt)

    def render(self, window_surface: pygame.Surface, camera: Camera) -> None:
        self.scenes[self.current_scene].render(window_surface, camera)