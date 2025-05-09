import pygame
import sys
from player import Player
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        cat_image = pygame.image.load('../assets/player/cat.png')
        cat_image = pygame.transform.scale(cat_image, (round(cat_image.get_width()/2),round(cat_image.get_height()/2)))
        cat = Player(100,100,cat_image)
        while self.running:
            self.screen.fill((30, 30, 46))
            self.screen.blit(cat.image,(cat.x,cat.y))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                cat.y-=5
            if keys[pygame.K_s]:
                cat.y+=5
            if keys[pygame.K_d]:
                cat.x+=5
            if keys[pygame.K_a]:
                cat.x-=5
            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(60)


