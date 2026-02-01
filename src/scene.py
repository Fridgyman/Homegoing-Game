import pygame

from src.camera import Camera
from src.config import Config
from src.dialogue import Dialogue
from src.entity import Entity
from src.interactable import Interactable
from src.map_element import MapElement
from src.player import Player
from src.scene_in_out import SceneEntrance, SceneExit, SceneTransition
from src.ui_manager import UIManager

BACKGROUND_MUSIC_FADE_MS = 1000

class Scene:
    def __init__(self, void_color: tuple[int, int, int, int], bounds: pygame.Vector2,
                 background_music: pygame.mixer.Sound,
                 map_elements: list[MapElement],
                 player: Player,
                 entrances: dict[str, SceneEntrance],
                 exits: list[SceneExit]
                 ):
        self.void_color: tuple[int, int, int, int] = void_color
        self.background_music: pygame.mixer.Sound = background_music
        self.bounds: pygame.Vector2 = bounds

        self.map_elements: list[MapElement] = map_elements

        self.player: Player = player
        self.entities: list[Entity] = []
        self.dialogue: Dialogue | None = None

        self.entrances: dict[str, SceneEntrance] = entrances
        self.entering_through: SceneEntrance | None = None
        self.exits: list[SceneExit] = exits
        self.exiting_through: SceneExit | None = None

        self.loaded: bool = False
        self.void_surface = pygame.Surface(Config.WINDOW_DIMS).convert()
        self.void_surface.fill(self.void_color[:3])
        self.void_surface.set_alpha(self.void_color[3])

    def load(self, entrance: str, player_face_dir: pygame.Vector2) -> None:
        if self.loaded: return
        self.loaded = True
        self.background_music.play(loops=-1, fade_ms=BACKGROUND_MUSIC_FADE_MS)

        if self.entrances[entrance].transition != SceneTransition.VOID_WALK:
            self.player.grid_pos = self.entrances[entrance].spawn.copy()
            self.player.pos = self.player.grid_pos * Config.TILE_SIZE
            self.player.facing = player_face_dir.copy()
        self.entering_through = self.entrances[entrance]

    def unload(self) -> None:
        if not self.loaded: return
        self.loaded = False
        self.background_music.fadeout(BACKGROUND_MUSIC_FADE_MS)

    def input(self, ui_manager: UIManager, keys: pygame.key.ScancodeWrapper) -> None:
        if self.dialogue is not None:
            self.dialogue.input(keys)
            ui_manager.input(keys)
            return

        self.player.input(keys)

        if not (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]): return
        for entity in self.entities:
            entity.input(keys)
            if isinstance(entity, Interactable) and entity.can_interact(self.player):
                self.dialogue = entity.interact(self.player)

        for scene_exit in self.exits:
            if not scene_exit.available():
                continue
            if scene_exit.can_interact(self.player):
                self.exiting_through = scene_exit
                break

    def update(self, camera: Camera, ui_manager: UIManager, dt: float, manager) -> None:
        camera.center_at(self.player.pos, self.bounds)

        if self.entering_through is not None:
            self.entering_through.update(manager, dt)
            if self.entering_through.complete:
                self.entering_through.complete = False
                self.entering_through = None

        elif self.exiting_through is not None:
            self.exiting_through.update(manager, dt)
            if self.exiting_through.complete:
                manager.load_scene(self.exiting_through.next_scene,
                                   self.exiting_through.next_entrance,
                                   self.player.facing)
                self.exiting_through.complete = False
                self.exiting_through = None
            return

        self.player.update(self.entities, self.map_elements, ui_manager, dt)
        self.player.grid_pos.x = pygame.math.clamp(self.player.grid_pos.x, 0, self.bounds.x)
        self.player.grid_pos.y = pygame.math.clamp(self.player.grid_pos.y, 0, self.bounds.y)
        self.player.pos.x = pygame.math.clamp(self.player.pos.x, 0,
                                              self.bounds.x * Config.TILE_SIZE - self.player.sprite.dimensions.x)
        self.player.pos.y = pygame.math.clamp(self.player.pos.y, 0,
                                              self.bounds.y * Config.TILE_SIZE - self.player.sprite.dimensions.y)

        for scene_exit in self.exits:
            if not scene_exit.available():
                continue
            if scene_exit.entered(self.player.grid_pos):
                self.exiting_through = scene_exit
                break

        if self.dialogue is not None:
            self.dialogue.update(ui_manager, dt)
            if self.dialogue.fade == 0:
                self.dialogue.reset()
                self.dialogue = None

        ui_manager.update()

        for entity in self.entities:
            entity.update(ui_manager, dt)

    def render(self, window_surface: pygame.Surface, camera: Camera, ui_manager: UIManager) -> None:
        window_surface.fill((0, 0, 0))
        window_surface.blit(self.void_surface, (0, 0))
        for entity in self.entities: entity.render(window_surface, camera)
        for map_element in self.map_elements: map_element.render(window_surface, camera)
        self.player.render(window_surface, camera)

        if self.dialogue is not None:
            dims: pygame.Rect = pygame.Rect(
                Config.DIALOGUE_BOX_POS.x, Config.DIALOGUE_BOX_POS.y,
                Config.DIALOGUE_BOX_DIMS.x, Config.DIALOGUE_BOX_DIMS.y
            )

            self.dialogue.render(window_surface, dims, ui_manager)