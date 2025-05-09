import pygame
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.cat = pygame.image.load('assets/player/cat.png')

    def run(self):
        self.screen.fill((30, 30, 46))
        while self.running:
            
            self.screen.blit(self.cat,(100,100))
            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(60)


