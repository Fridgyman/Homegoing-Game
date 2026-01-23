import pygame
from src.scene_manager import SceneManager
from src.asset_manager import AssetManager
from src.camera import Camera

from src.scenes import test_scene

import sys

class Game:
    def __init__(self, FPS: int, audio_assets_path: str = "", font_assets_path: str = "", image_assets_path: str = ""):
        self.scene_manager: SceneManager = SceneManager()
        self.asset_manager: AssetManager = AssetManager(audio_assets_path, font_assets_path, image_assets_path)

        self.window_surface: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.window_dimensions: pygame.Vector2 = pygame.Vector2(self.window_surface.get_width(), self.window_surface.get_height())
        pygame.display.set_caption("Homegoing")
        
        self.camera: Camera = Camera(self.window_dimensions, 32)
        
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.delta_time: float = 0

        self.init_scenes()

    def run(self):
        while True:
            self.delta_time = self.clock.tick() / 1000.0

            self.input()
            self.update()
            self.render()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        self.scene_manager.input(keys)

    def update(self):
        self.scene_manager.update(self.camera, self.delta_time)

    def render(self):
        self.scene_manager.render(self.window_surface, self.camera)
        pygame.display.flip()

    def init_scenes(self):
        self.scene_manager.add_scene("test", test_scene.TestScene())
        self.scene_manager.load_scene("test", self.asset_manager)