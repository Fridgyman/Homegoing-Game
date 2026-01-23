import pygame

class Monologue:
    def __init__(self,
                 speaker: str, lines: list[str], char_speeds: list[float],
                 font: pygame.font.Font,
                 next_monologue: Monologue = None,
                 options: list[tuple(str, Monologue)] = {},
                 speaker_image: pygame.Surface | None = None):
        self.speaker: str = speaker
        self.lines: list[str] = lines
        self.speaker_image: pygame.Surface | None = speaker_image
        self.font = font

        self.awaiting_choice: bool = False
        self.options: list[tuple(str, Monologue)] = options
        self.spoken: str = ""
        if (next_monologue is not None):
            self.options.append(("NEXT_MONOLOGUE_RESERVED", next_monologue))

        self.line_index: list[int] = 0
        self.char_index: list[int] = 0

        self.char_duration: float = 0
        self.char_speeds: list[float] = char_speeds

    def choose(self, choice: int):
        if (not awaiting_choice): return None
        return self.options[choice][1]

    def skip(self) -> Monologue | None:
        if (self.awaiting_choice): return
        
        if (self.char_index[0] == self.char_index[1]): # end of current line
            if (self.line_index[0] == self.line_index[1]): # current line is final line of monologue
                return self.options[-1][1]

            self.line_index[0]++
            return None
        self.char_index[0] = self.char_index[1]
        return None
       
    def update(self, dt: float):
        self.char_duration += dt;

        if (self.char_duration >= self.char_speeds[line_index]):
            self.char_duration = 0
            self.char_index++

    def render(self, diag_surface: pygame.Surface):
        pass

class Dialogue:
    def __init__(self):
        self.current_monologue: Monologue = None
 
        self.started: bool = False
        self.fade: int = 0
        self.fading: int = 0
        self.choice_index: int = 0
        self.choice_move_block: bool = False
 
    def start(self):
        self.started = True
        self.fading = 255

    def input(self, keys: pygame.key.ScancodeWrapper):
        if (keys[pygame.K_RETURN]):
            if (self.current_monologue.awaiting_choice):
                self.current_monologue = self.current_monologue.choose(self.choice_index)
                return
            new_monologue: Monologue | None = self.current_monologue.skip()
            if (new_monologue is not None):
                self.current_monologue = new_monologue

        moving: bool = False
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            moving = True
            if (not self.choice_move_block):
                self.choice_index++
                self.choice_move_block = True
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            moving = True
            if (not self.choice_move_block):
                self.choice_index--
                self.choice_move_block = True

        if (not moving):
            self.choice_move_block = False

    def update(self, dt: float):
        self.fade = self.fade + self.fading
        self.current_monologue.update(dt)

    def render(self, ui_surface: pygame.Surface):
        pass
