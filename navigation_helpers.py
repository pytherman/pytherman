"""Helper functions for navigate via game"""
import pygame


def set_if_mouse_visible(is_visible):
    """Hide mouse where user uses keyboard to navigation and show mouse otherwise"""
    if is_visible:
        pygame.mouse.set_visible(True)
    else:
        pygame.mouse.set_visible(False)


def set_item_selection(self, key):
    """Set yellow color of item when user select it by keyboard, and white otherwise"""
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


def set_mouse_selection(item, posx, posy):
    """Set yellow color of item when user select it by mouse, and white otherwise"""
    if item.is_mouse_on_this(posx, posy):
        item.color_the_item((255, 255, 0))
        item.set_italic(True)
    else:
        item.color_the_item((255, 255, 255))
        item.set_italic(False)
