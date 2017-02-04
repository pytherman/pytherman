"""Screen with names of authors"""
from collections import OrderedDict

import pygame
import sys
from mainmenu import MenuItem
import navigation_helpers as nh

FPS = 60
PPM = 20
RESOLUTION = 720, 480
TIME_STEP = 1.0 / FPS


class Authors:
    pygame.init()

    def __init__(self, screen, bg_color=(0, 0, 0), font=None, font_size=35, font_color=(255, 255, 255)):
        """Setup variables and basic navigation"""
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
        self.label_image = self.font.render("Authors:", True, self.text_color)
        self.name1_image = self.font.render("Dominika Zajac", True, self.text_color)
        self.name2_image = self.font.render("Adam Piekarczyk", True, self.text_color)

        self.funcs["Back"] = self.menu
        self.funcs["Quit"] = sys.exit
        items = self.funcs.keys()
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height) + 80
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def menu(self):
        """Go back to main menu"""
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

            self.screen.blit(self.label_image, (250, 90))
            self.screen.blit(self.name1_image, (200, 150))
            self.screen.blit(self.name2_image, (200, 200))
            pygame.display.flip()


if __name__ == '__main__':
    pygame.display.set_caption('Game Menu')
    Authors.run()
