import pygame

import os

class AssetManager:
    def __init__(self, audio_assets_path: str, font_assets_path: str, image_assets_path: str):
        self.audio_assets: dict[str, pygame.mixer.Sound] = {}
        self.font_assets: dict[str, pygame.font.Font] = {}
        self.image_assets: dict[str, pygame.Surface] = {}

        audio_file_names: list[str] = [fp for fp in os.listdir(audio_assets_path) if os.path.isfile(os.path.join(audio_assets_path, fp))]
        font_file_names: list[str] = [fp for fp in os.listdir(font_assets_path) if os.path.isfile(os.path.join(font_assets_path, fp))]
        image_file_names: list[str] = [fp for fp in os.listdir(image_assets_path) if os.path.isfile(os.path.join(image_assets_path, fp))]

        for name in audio_file_names:
            self.add_audio(name=name, audio_path=os.path.join(audio_assets_path, name))

        for name in font_file_names:
            for size in range(6, 24, 4):
                self.add_font(name=name, font_path=os.path.join(font_assets_path, name), font_size=size)

        for name in image_file_names:
            self.add_image(name=name, image_path=os.path.join(image_assets_path, name))

    def add_audio(self, name: str, audio_path: str) -> None:
        self.audio_assets[name] = pygame.mixer.Sound(file=audio_path)

    def add_font(self, name: str, font_path: str, font_size: int) -> None:
        self.font_assets[name + str(font_size)] = pygame.font.Font(file=font_path, size=font_size)

    def add_image(self, name: str, image_path: str) -> None:
        self.image_assets[name] = pygame.image.load(image_path)

    def get_audio(self, name: str) -> pygame.mixer.Sound:
        return self.audio_assets[name]

    def get_font(self, name: str) -> pygame.font.Font:
        return self.font_assets[name]

    def get_image(self, name: str) -> pygame.Surface:
        return self.image_assets[name]