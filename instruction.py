"""Screen with instruction how to play"""
from collections import OrderedDict
import pygame
import sys
from pygame.locals import *

from menuitem import MenuItem
import navigation_helpers as nh


class Instruction:
    pygame.init()

    def __init__(self, screen, bg_color=(0, 0, 0), font=None, font_size=35, font_color=(255, 255, 255)):
        """set up all variables, prepare basic navigation"""
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.items = []
        self.funcs = OrderedDict()

        self.text_color = (255, 255, 255)

        self.funcs["Back"] = self.menu
        self.funcs["Quit"] = sys.exit
        items = self.funcs.keys()
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height) + 120
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None
        self.text_wall = TextWall()
        self.text_wall.parse_text(instruction_text)

    def menu(self):
        """Go back to menu"""
        from mainmenu import Menu
        gm = Menu(self.screen)
        gm.run()

    def run(self):
        """Main loop of screen, wait and react for user selection, show navigation, etc"""
        mainloop = True
        while mainloop:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    nh.set_item_selection(self, event.key)
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        text = self.items[self.cur_item].text
                        mainloop = False
                        self.funcs[text]()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        (x, y) = pygame.mouse.get_pos()
                        if item.is_mouse_on_this(x, y):
                            self.funcs[item.text]()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            nh.set_if_mouse_visible(self.mouse_is_visible)

            self.screen.fill(self.bg_color)
            for item in self.items:
                if self.mouse_is_visible:
                    (x, y) = pygame.mouse.get_pos()
                    nh.set_mouse_selection(item, x, y)
                self.screen.blit(item.label, item.position)

            self.text_wall.draw()
            pygame.display.flip()


class TextLine(object):
    def __init__(self, font=None, size=24, text=""):
        """Set up all variables, colors and fonts"""
        self.font_name = font
        self.font_size = size
        self.color_fg = Color("white")
        self.color_bg = Color("gray20")

        self._aa = True
        self._text = text
        self.font = pygame.font.Font(font, size)
        self.screen = pygame.display.get_surface()

        self.dirty = True
        self.image = None
        self._render()

    def _render(self):
        """Render line of text"""
        self.dirty = False
        self.image = self.font.render(self._text, self.aa, self.color_fg)
        self.rect = self.image.get_rect()

    def draw(self):
        """Call this do draw, always prefers to use cache"""
        if self.dirty or (self.image is None):
            self._render()
        self.screen.blit(self.image, self.rect)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.dirty = True
        self._text = text

    @property
    def aa(self): return self._aa

    @aa.setter
    def aa(self, aa):
        self.dirty = True
        self._aa = aa


class TextWall(object):
    """Manages multiple lines of text"""
    def __init__(self, font=None, size=24):
        self.font = font
        self.font_size = size
        self.offset = Rect(20, 20, 3, 3)

        self.screen = pygame.display.get_surface()
        self.dirty = True
        self.text_lines = []
        self._text_paragraph = "Empty\nText"
        self._render()

    def _render(self):
        """render list of lines"""
        self.dirty = False
        self.text_lines = [TextLine(self.font, self.font_size, line) for line in self._text_paragraph]
        self.text_lines[0].rect.top = self.offset.top

        # offset the height of each line
        prev = Rect(0, 0, 0, 0)
        for t in self.text_lines:
            t.rect.top += prev.bottom
            t.rect.left = self.offset.left
            prev = t.rect

    def parse_text(self, text):
        """parse raw text to something usable"""
        self._text_paragraph = text.split("\n")
        self._render()

    def draw(self):
        """draw with cached surfaces"""
        if self.dirty:
            self._render()
        for text in self.text_lines:
            text.draw()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self.dirty = True
        self._font_size = size

    @property
    def text(self):
        return self._text_paragraph

    @text.setter
    def text(self, text_paragraph):
        self.dirty = True
        self.parse_text(text_paragraph)


if __name__ == '__main__':
    pygame.display.set_caption('Instruction')
    Instruction.run()

instruction_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed aliquet
tellus eros, eu faucibus dui. Phasellus eleifend, massa id ornare sodales, est urna
congue tellus, vitae varius metus nunc non enim. Mauris elementum, arcu vitae tempor euismod, justo turpis malesuada est, sed dictum nunc nulla nec mauris. Cras felis eros, elementum vitae sollicitudin in, elementum et augue. Proin eget nunc at dui congue pretium. Donec ut ipsum ut lacus mollis tristique.

Proin pulvinar metus nec mi semper semper. Pellentesque habitant morbi tristique
senectus et netus et malesuada fames ac turpis egestas. Proin in diam odio. Vestibulum
at neque sed ante sodales eleifend quis id dui. Mauris sollicitudin, metus a semper consectetur,
est lectus varius erat, sit amet ultrices tortor nisi id justo. Aliquam elementum vestibulum dui ut auctor. Mauris commodo sapien vitae augue tempus sagittis. Morbi a nibh lectus, sed porta nibh. Donec et est ac dui sodales aliquet tristique et arcu. Nullam enim felis, posuere vel rutrum eu, euismod a purus. Morbi porta cursus libero, id rutrum elit lacinia vitae.

In condimentum ultrices ipsum, ut convallis odio egestas et. Cras at egestas elit. Morbi
quis neque ligula. Sed tempor, sem at fringilla rhoncus, diam quam mollis nisi, vitae semper
mi massa sit amet tellus. Vivamus congue commodo ornare. Morbi et mi non sem malesuada rutrum. Etiam est purus, interdum ut placerat sit amet, tempus eget eros. Duis eget augue quis diam facilisis blandit. Ut vulputate adipiscing eleifend. """
