import pygame
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.cat = pygame.image.load('assets/player/cat.png')
        self.cat= pygame.transform.scale(self.cat, (round(self.cat.get_width()/2),round(self.cat.get_height()/2)))
        self.x = 100
        self.y=100

    def run(self):
        while self.running:
            self.screen.fill((30, 30, 46))
            self.screen.blit(self.cat,(self.x,self.y))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y-=5
            if keys[pygame.K_s]:
                self.y+=5
            if keys[pygame.K_d]:
                self.x+=5
            if keys[pygame.K_a]:
                self.x-=5
            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(60)


