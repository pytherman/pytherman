import sys
from collections import OrderedDict

import pygame

import pytherman
from menuitem import MenuItem


class Menu:
    pygame.init()

    def __init__(self, screen, items, funcs, bg_color=(0, 0, 0), font=None, font_size=35, font_color=(255, 255, 255)):

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.items = []
        self.funcs = funcs
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def set_if_mouse_visible(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_item_selection(self, key):
        length = len(self.items)
        for item in self.items:
            item.set_italic(False)
            item.color_the_item((255, 255, 255))
        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_UP:
                if self.cur_item > 0:
                    self.cur_item -= 1
                else:
                    self.cur_item = length - 1
            elif key == pygame.K_DOWN:
                if self.cur_item < length - 1:
                    self.cur_item += 1
                else:
                    self.cur_item = 0
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].color_the_item((255, 255, 0))

    def set_mouse_selection(self, item, posx, posy):
        if item.is_mouse_on_this(posx, posy):
            item.color_the_item((255, 255, 0))
            item.set_italic(True)
        else:
            item.color_the_item((255, 255, 255))
            item.set_italic(False)

    def run(self):
        mainloop = True
        while mainloop:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_item_selection(event.key)
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

            self.set_if_mouse_visible()

            self.screen.fill(self.bg_color)
            for item in self.items:
                if self.mouse_is_visible:
                    (x, y) = pygame.mouse.get_pos()
                    self.set_mouse_selection(item, x, y)
                self.screen.blit(item.label, item.position)
            pygame.display.flip()


if __name__ == "__main__":
    def hello():
        print('Hello')

    def startgame():
        pytherman.main()

    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Game Menu')
    funcs = OrderedDict()
    funcs["Start Game"] = startgame
    funcs["How to play"] = hello
    funcs["Instruction"] = hello
    funcs["Authors"] = hello
    funcs["Quit"] = sys.exit

    gm = Menu(screen, funcs.keys(), funcs)
    gm.run()
