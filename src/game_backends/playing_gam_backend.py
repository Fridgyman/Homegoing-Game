import pygame
from src.game_backends.backend import Backend

class PlayingBackend(Backend):
    def __init__(self):
        super().__init__()
        self.camera_pos = pygame.Vector2(0, 0)
        self.move_speed = 400  # Pixels per second
        self.grid_size = 80
        self.is_setup = True # So the Menu shows "Continue"

    def init(self, game):
        self.next_backend = None
       
    def input(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from src.game_backends.backend import GameState
                    game.set_backend(GameState.MAIN_MENU)

    def update(self, game):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        
        # Movement logic: Changing camera coordinates
        if keys[pygame.K_w] or keys[pygame.K_UP]:    direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()
            self.camera_pos += direction * self.move_speed * game.delta_time

    def render(self, game):
        screen = game.window_surface
        screen.fill((20, 20, 25)) # Deep theme for Homegoing
        
        width, height = screen.get_size()
        center = pygame.Vector2(width // 2, height // 2)

        offset_x = -(self.camera_pos.x % self.grid_size)
        offset_y = -(self.camera_pos.y % self.grid_size)

        for x in range(int(offset_x), width + self.grid_size, self.grid_size):
            pygame.draw.line(screen, (40, 40, 50), (x, 0), (x, height), 1)
        for y in range(int(offset_y), height + self.grid_size, self.grid_size):
            pygame.draw.line(screen, (40, 40, 50), (0, y), (width, y), 1)

        # In an "Open World", the player stays center while the world moves
        pygame.draw.rect(screen, (200, 50, 50), (center.x - 20, center.y - 20, 40, 40))
