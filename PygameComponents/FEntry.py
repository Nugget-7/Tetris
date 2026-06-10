import pygame

class Fentry:
    def __init__(self, x, y, lx, ly, place_holder = "", 
                password = False, numeric = False, max_len = None, font = None, 
                bg_color = None, bg_color_active = None, border_color = None, 
                border_color_active = None, txt_color = None,
                place_holder_color = None, cursor_color = None,
                border_lx = 2, padding = 8):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.place_holder = place_holder
        self.password = password
        self.numeric = numeric
        self.max_len = max_len
        self.font = font
        self.rect = None
        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer =  0
        self.cursor_interval = 500
        self.bg_color = bg_color
        self.bg_color_active = bg_color_active
        self.border_color = border_color
        self.border_color_active = border_color_active
        self.txt_color = txt_color
        self.place_holder_color = place_holder_color
        self.cursor_color = cursor_color
        self.border_lx = border_lx
        self.padding = padding

    
    def init(self):
        self.rect = pygame.Rect(self.x, self.y, self.lx, self.ly)
        if self.font == None:
            self.font = pygame.font.SysFont("Arial", 20)
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.cursor_visible = True
            self.cursor_timer = 0
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.active = False
            elif event.key == pygame.K_TAB:
                self.active = False
            else:
                char = event.unicode
                if char and char.isprintable():
                    if self.numeric and not (char.isdigit() or char in ".-"):
                        return
                    if self.max_len is None or len(self.text) < self.max_len:
                        self.text += char
            self.cursor_visible = True
            self.cursor_timer = 0

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_interval:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, surface):
        bg = self.bg_color_active if self.active else self.bg_color
        border = self.border_color_active if self.active else self.border_color
        pygame.draw.rect(surface, bg, self.rect, border_radius=4)
        pygame.draw.rect(surface, border, self.rect, self.border_lx, border_radius=4)

        display_text = "*" * len(self.text) if self.password else self.text

        if display_text:
            text_surf = self.font.render(display_text, True, self.txt_color)
        elif self.place_holder and not self.active:
            text_surf = self.font.render(self.place_holder, True, self.place_holder_color)
        else:
            text_surf = None

        clip = surface.get_clip()
        inner = self.rect.inflate(-self.padding * 2, -self.padding)
        surface.set_clip(inner)

        text_y = self.rect.y + (self.rect.height - self.font.get_height()) // 2
        if text_surf:
            surface.blit(text_surf, (self.rect.x + self.padding, text_y))

        if self.active and self.cursor_visible:
            text_w = self.font.size(display_text)[0] if display_text else 0
            cursor_x = self.rect.x + self.padding + text_w
            pygame.draw.line(
                surface, self.cursor_color,
                (cursor_x, text_y + 2),
                (cursor_x, text_y + self.font.get_height() - 2),
                2,
            )

        surface.set_clip(clip)

    def get_value(self):
        return self.text

    def set_value(self, value):
        self.text = str(value)

    def clear(self):
        self.text = ""