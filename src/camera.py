import pygame
import random as random

class Camera:
    def __init__(self, win_dims: pygame.Vector2, grid_size: int):
        self.pos: pygame.Vector2 = pygame.Vector2(0, 0)

        self.window_dimensions = win_dims
        self.window_center = win_dims // 2

        self.grid_size = grid_size
        self.shake_amount = 0 
        self.zoom_level = 1

    def center(self, pos: pygame.Vector2, bounds: pygame.Vector2) -> None:
        self.pos = pos - self.window_center
        self.clamp_pos(bounds)

    def clamp_pos(self, bounds: pygame.Vector2) -> None:
        self.pos.x = max(0, min(self.pos.x, bounds.x - self.window_dimensions.x))
        self.pos.y = max(0, min(self.pos.y, bounds.y - self.window_dimensions.y))

    def world_pos_to_view_pos(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        return world_pos - self.pos + self.get_shake_offset(1/60)
    
    def grid_pos_to_view_pos(self, grid_pos: pygame.Vector2) -> pygame.Vector2:
        return grid_pos * self.grid_size
        
    def shake_camera(self, intensity_x=10, intensity_y=10, duration=0.5):
        self.shake_amount_x = intensity_x
        self.shake_amount_y = intensity_y
        self.shake_duration = duration 

    def get_shake_offset(self, delta_time):

        if self.shake_duration > 0:
            self.shake_duration -= delta_time
            fraction = self.shake_duration / max(self.shake_duration + delta_time, 0.01)
            current_x = self.shake_amount_x * fraction
            current_y = self.shake_amount_y * fraction
            offset_x = random.uniform(-current_x, current_x)
            offset_y = random.uniform(-current_y, current_y)
            return pygame.Vector2(offset_x, offset_y)
        
        # Reset when the shake is over-
        self.shake_amount_x = 0
        self.shake_amount_y = 0
        return pygame.Vector2(0, 0)
        
    # def camera_zoom(self):
    #     keys = pygame.key.get_pressed()

    #     # Zoom In
    #     if keys[pygame.K_q]:
    #         self.zoom_level += 0.02
    #     # Zoom Out
    #     if keys[pygame.K_e]:
    #         self.zoom_level -= 0.02

    #     # Note that this function allows the player to zoom, not as we wish.
    #     self.zoom_level = max(0.5, min(self.zoom_level, 3.0))

    # def get_zoomed_grid(self):
    #     """Calculates the grid size adjusted for zoom."""
    #     return self.grid_size * self.zoom_level
