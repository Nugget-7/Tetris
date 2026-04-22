import pygame

class Button():
    def __init__(self, x, y, lx, ly, txt, color, font):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.color = color
        self.font = font
        self.txt = txt
        self.txt_img = font.render(txt, True, color)

    def hover(self, mouse):
        if (mouse[0] > self.x and mouse[0] < self.x + self.lx) and (mouse[1] > self.y and mouse[1] < self.y + self.ly):
            self.txt_img = self.font.render(self.txt, True, self.color)
            return True
        else:
            self.txt_img = self.font.render(self.txt, True, self.color)
            return False
        
    def click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False