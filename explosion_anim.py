import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'assets/explosion')

FPS = 60

# define colors

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
flag = True


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_anim):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_anim = explosion_anim
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        global flag
        flag = True

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                global flag
                flag = False
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def run(pos, screen):
    explosion_anim = {}
    explosion_anim['lg'] = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (95, 95))
        explosion_anim['lg'].append(img_lg)

    all_sprites = pygame.sprite.Group()
    expl = Explosion(pos, 'lg', explosion_anim)
    while flag:
        all_sprites.update()
        expl = Explosion(pos, 'lg', explosion_anim)
        all_sprites.add(expl)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()

    expl.kill()
    all_sprites.remove(expl)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
