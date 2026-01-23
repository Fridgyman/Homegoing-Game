import pygame

class Camera:
    def __init__(self, win_dims: pygame.Vector2, grid_size: int):
        self.pos: pygame.Vector2 = pygame.Vector2(0, 0)

        self.window_dimensions = win_dims
        self.window_center = win_dims // 2

        self.grid_size = grid_size

    def center(self, pos: pygame.Vector2, bounds: pygame.Vector2) -> None:
        self.pos = pos - self.window_center
        self.clamp_pos(bounds)

    def clamp_pos(self, bounds: pygame.Vector2) -> None:
        self.pos.x = max(0, min(self.pos.x, bounds.x - self.window_dimensions.x))
        self.pos.y = max(0, min(self.pos.y, bounds.y - self.window_dimensions.y))

    def world_pos_to_view_pos(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        return world_pos - self.pos
    
    def grid_pos_to_view_pos(self, grid_pos: pygame.Vector2) -> pygame.Vector2:
        return grid_pos * self.grid_size