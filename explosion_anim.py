"""Show animation during explosion"""
import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'assets/explosion')

FPS = 60
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
flag = True


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_anim):
        """Set up all variables"""
        pygame.sprite.Sprite.__init__(self)
        self.explosion_anim = explosion_anim
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        global flag
        flag = True

    def update(self):
        """Update image in animation"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                global flag
                flag = False
            else:
                center = self.rect.center
                try:
                    self.image = self.explosion_anim[self.size][self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                except IndexError:
                    flag = False


def run(pos, screen, size):
    """Prepare images and run animation"""
    explosion_anim = {'sm': [], 'lg': []}
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_sm = pygame.transform.scale(img, (95, 95))
        img_lg = pygame.transform.scale(img, (150, 150))
        explosion_anim['sm'].append(img_sm)
        explosion_anim['lg'].append(img_lg)

    all_sprites = pygame.sprite.Group()
    expl = Explosion(pos, size, explosion_anim)
    while flag:
        all_sprites.update()
        expl = Explosion(pos, size, explosion_anim)
        all_sprites.add(expl)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()

    expl.kill()
    all_sprites.remove(expl)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
