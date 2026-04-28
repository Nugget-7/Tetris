import pygame

class FButton():
    # Tarea agregar imagen normal y una imagen on hover
    # si no se usa imagen entonces solo se usa el color

    # Debes hacer una logica que si existe la imagen
    # usa la imagen si no entonces usa el texto
    def __init__(self, x, y, lx, ly, txt, color, colorH, font, img = None, imgH = None):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.color = color
        self.color_on_hover = colorH
        self.font = font
        self.txt = txt
        self.txt_img = font.render(txt, True, color)
        self.img = img
        self.imgH = imgH
        

    def hover(self, mouse):
        if (mouse[0] > self.x and mouse[0] < self.x + self.lx) and (mouse[1] > self.y and mouse[1] < self.y + self.ly):
            if self.img and self.imgH:
                img = self.imgH
            self.txt_img = self.font.render(self.txt, True, self.color_on_hover)
        else:
            self.txt_img = self.font.render(self.txt, True, self.color)
        
    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (self.x < mouse[0] < self.x + self.lx and
                self.y < mouse[1] < self.y + self.ly):
                return True
        return False
    