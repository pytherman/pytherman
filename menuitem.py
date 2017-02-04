"""Class for preparing elements in menu lists"""
import pygame


class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=(255, 255, 255), pos_x = 0, pos_y=0):
        """set up all variables"""
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def set_position(self, x, y):
        """Set position of element"""
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def is_mouse_on_this(self, posx, posy):
        """Return true where mouse is on this element and false otherwise"""
        if self.pos_x <= posx <= self.pos_x + self.width:
            if self.pos_y <= posy <= self.pos_y + self.height:
                return True
        return False

    def color_the_item(self, color):
        """Change the color of element"""
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)
