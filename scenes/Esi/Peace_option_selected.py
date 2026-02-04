import pygame
import torch
import torch.nn as nn
import random
import math

class FateEvaluator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def evaluate(self, stats):
        with torch.no_grad():
            val = self.net(torch.tensor(stats, dtype=torch.float32))
            return val.item()

class Raider:
    def __init__(self, x, y, type="fante"):
        self.pos = [float(x), float(y)]
        self.type = type
        self.speed = random.uniform(1.5, 3.0)
        self.health = 2

class EsiWarGame:
    def __init__(self, heritage=1.0, will=1.0, has_stone=True):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Georgia", 22)
        
        self.heritage = heritage
        self.will = will
        self.has_stone = has_stone
        self.fate_engine = FateEvaluator()
        
        self.pos = [400, 300]
        self.health = 100
        self.captured_meter = 0 
        
        self.raiders = []
        self.projectiles = []
        self.decisions_made = []
        self.game_active = True
        self.current_event = None 
        
        self.wave_timer = 0
        self.difficulty = 1.0

    def trigger_decision(self, title, choice1, choice2, impact1, impact2):
        """Pauses game for a Homegoing-themed decision."""
        self.current_event = {
            "title": title,
            "c1": choice1, "c2": choice2,
            "i1": impact1, "i2": impact2
        }

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        speed = 4.0 + (self.will * 0.5)
        
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.pos[1] -= speed  # pyright: ignore[reportCallIssue, reportArgumentType]
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.pos[1] += speed # type: ignore
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.pos[0] -= speed # pyright: ignore[reportCallIssue, reportArgumentType]
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.pos[0] += speed # pyright: ignore[reportCallIssue, reportArgumentType]

        self.pos[0] = max(0, min(800, self.pos[0])) # type: ignore
        self.pos[1] = max(0, min(600, self.pos[1])) # type: ignore

    def spawn_wave(self):
        if len(self.raiders) < 5 + (self.difficulty * 2):
            side = random.choice(["L", "R", "T", "B"])
            if side == "L": spawn = [-50, random.randint(0, 600)]
            else: spawn = [850, random.randint(0, 600)]
            self.raiders.append(Raider(spawn[0], spawn[1]))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "ABORTED"
                
                if self.current_event:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.will += self.current_event["i1"][0]
                            self.heritage += self.current_event["i1"][1]
                            self.current_event = None
                        if event.key == pygame.K_2:
                            self.will += self.current_event["i2"][0] # type: ignore
                            self.heritage += self.current_event["i2"][1] # type: ignore
                            self.current_event = None
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        angle = math.atan2(my - self.pos[1], mx - self.pos[0])
                        self.projectiles.append({"p": list(self.pos), "a": angle})

            if not self.current_event:
                self.handle_movement()
                self.spawn_wave()
                self.wave_timer += 1
                
                self.difficulty += 0.001
                
                if self.wave_timer == 300:
                    self.trigger_decision("THE BIG MAN FALLS", 
                                        "1. Grab his spear (Attack Up)", "2. Comfort him (Will Up)", 
                                        [0.5, 0], [0, 0.5])
                if self.wave_timer == 800:
                    self.trigger_decision("MAAME IS BEING DRAGGED", 
                                        "1. Rush to her (Risk Capture)", "2. Stay in shadows (Heritage Up)", 
                                        [0.2, -0.5], [-0.2, 1.0])

                for r in self.raiders[:]:
                    dx, dy = self.pos[0] - r.pos[0], self.pos[1] - r.pos[1]
                    dist = math.hypot(dx, dy)
                    r.pos[0] += (dx/dist) * r.speed
                    r.pos[1] += (dy/dist) * r.speed
                    
                    if dist < 25:
                        capture_prob = self.fate_engine.evaluate([self.heritage, self.will, self.difficulty, 0.5])
                        self.captured_meter += (0.5 * capture_prob)
                        if not self.has_stone: self.captured_meter += 0.2

                for p in self.projectiles[:]:
                    p["p"][0] += math.cos(p["a"]) * 7
                    p["p"][1] += math.sin(p["a"]) * 7
                    # Collision
                    for r in self.raiders[:]:
                        if math.hypot(p["p"][0]-r.pos[0], p["p"][1]-r.pos[1]) < 20:
                            self.raiders.remove(r)
                            if p in self.projectiles: self.projectiles.remove(p)

                if self.captured_meter >= 100:
                    return self.end_screen(True) # Sold
                if self.wave_timer > 1500:
                    return self.end_screen(False) # Escaped

            self.draw()
            self.clock.tick(60)

    def draw(self):
        self.screen.fill((80, 20, 0)) 
        
        color = (200, 160, 100)
        pygame.draw.circle(self.screen, color, (int(self.pos[0]), int(self.pos[1])), 15)
        if self.has_stone:
            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.pos[0]), int(self.pos[1])), 5)

        for r in self.raiders:
            pygame.draw.rect(self.screen, (230, 230, 230), (r.pos[0]-10, r.pos[1]-10, 20, 20))

        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, 200, 20))
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 20, self.captured_meter * 2, 20))
        self.render_text("CAPTURE PROGRESS", 20, 45, (200, 200, 200))

        if self.current_event:
            s = pygame.Surface((800, 600), pygame.SRCALPHA)
            s.fill((0, 0, 0, 200))
            self.screen.blit(s, (0,0))
            self.render_text(self.current_event["title"], 300, 200, (255, 255, 255))
            self.render_text(self.current_event["c1"], 250, 280, (255, 215, 0))
            self.render_text(self.current_event["c2"], 250, 320, (255, 215, 0))

        pygame.display.flip()

    def render_text(self, text, x, y, color):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def end_screen(self, sold):
        return sold

if __name__ == "__main__":
    war = EsiWarGame(heritage=1.2, will=0.8, has_stone=True)
    is_esi_sold = war.run()
    print(f"Final outcome: {'SOLD' if is_esi_sold else 'ESCAPED'}")