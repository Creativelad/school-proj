import pygame
import sys
from player import Player
from pathlib import Path
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_resting_forward = True

    def run(self):
        BASE_DIR = Path(__file__).resolve().parent
        cat_image = pygame.image.load(BASE_DIR / "../assets/player/cat.png")
        cat_image = pygame.transform.scale(cat_image, (round(cat_image.get_width()/2),round(cat_image.get_height()/2)))
        cat = Player(100,100,cat_image)
        pygame.mixer.music.load(BASE_DIR / "../assets/music/bgm.mp3")
        pygame.mixer.music.play(-1,0.0)
        while self.running:
            self.screen.fill((30, 30, 46))
            self.screen.blit(cat.image,(cat.x,cat.y))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                cat.move(0,-5)
            if keys[pygame.K_s]:
                cat.move(0,5)
            if keys[pygame.K_d]:
                cat.move(5,0)
            if keys[pygame.K_a]:
                cat.move(-5,0)
            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(60)


