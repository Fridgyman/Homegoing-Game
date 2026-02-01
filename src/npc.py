import pygame

from src.dialogue import Dialogue
from src.entity import Entity
from src.interactable import Interactable
from src.player import Player
from src.sprite import Sprite, dir_to_str
from src.ui_manager import UIManager


class NPC(Entity, Interactable):
    def __init__(self, grid_pos: pygame.Vector2, sprite: Sprite, collision: bool, dialogue: Dialogue):
        Entity.__init__(self, grid_pos=grid_pos, sprite=sprite, collision=collision)
        Interactable.__init__(self)
        self.dialogue: Dialogue = dialogue

    def can_interact(self, player: Player) -> bool:
        return pygame.Rect(self.grid_pos, self.hit_box).collidepoint(player.grid_pos + player.facing)
    
    def interact(self, player: Player) -> Dialogue | None:
        if self.block:
            return None
        self.look_at(player.grid_pos)
        self.dialogue.start()
        self.block = True
        return self.dialogue

    def input(self, keys: pygame.key.ScancodeWrapper) -> None:
        pass

    def update(self, ui_manager: UIManager, dt: float) -> None:
        self.sprite.set(dir_to_str(self.velocity, self.facing))
        self.sprite.update(dt)
        if self.block and not self.dialogue.playing:
            self.look_at(self.grid_pos + pygame.Vector2(0, 1))
            self.elapsed_time += dt
            if self.elapsed_time > 1:
                self.elapsed_time = 0
                self.block = False