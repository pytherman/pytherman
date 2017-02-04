"""First screen of game"""
import sys
from collections import OrderedDict
import pygame
import instruction
import pytherman
import authors
from menuitem import MenuItem
import navigation_helpers as nh


class Menu:
    pygame.init()

    def __init__(self, screen, bg_color=(0, 0, 0), font=None, font_size=35, font_color=(255, 255, 255)):
        """Set up all variables, choose colors and fonts
        and preparing list of items in menu with functions
        which them called"""
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.items = []
        self.funcs = OrderedDict()
        self.funcs["Start Game"] = self.startgame
        self.funcs["Instruction"] = self.instruction
        self.funcs["Authors"] = self.showauthors
        self.funcs["Quit"] = sys.exit
        items = self.funcs.keys()
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def instruction(self):
        """Show screen with intructions to game"""
        instruction.Instruction(self.screen).run()

    def startgame(self):
        """start game"""
        pytherman.main()

    def showauthors(self):
        """Show screen with names of authors"""
        authors.Authors(self.screen).run()

    def run(self):
        """Main loop of menu, watch for changes, selection of item, etc """
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
            pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Game Menu')

    gm = Menu(screen)
    gm.run()
