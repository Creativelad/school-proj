import pygame
import sys
from player import Player
from pathlib import Path
from tilemap import Tilemap
BASE_DIR = Path(__file__).resolve().parent
class Game:
 

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.res = (800, 600)
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_resting_forward = True
        self.platform = pygame.Rect(100,450,675,166)
        self.assets={"dirt":pygame.image.load(BASE_DIR/"../assets/images/5.png").convert_alpha(),
            "grass":pygame.image.load(BASE_DIR/"../assets/images/1.png").convert_alpha()}
        self.scroll = [0.0,0.0]

    def run(self):
        cat_image = pygame.image.load(BASE_DIR / "../assets/player/cat.png")
        cat = Player(100,100,cat_image,self)
        pygame.mixer.music.load(BASE_DIR / "../assets/music/bgm.mp3")
        # v ENABLE THIS BEFORE MAIN RELASE v 
        # pygame.mixer.music.play(-1,0.0)
        tilemap = Tilemap(self)
        while self.running:
            self.screen.fill((30, 30, 46))
            self.scroll[0] += (cat.rect().centerx - self.res[0] / 2 - self.scroll[0]) / 30
            self.scroll[1] += (cat.rect().centery - self.res[1] / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            tilemap.render(offset=render_scroll)
            keys = pygame.key.get_pressed()
            movement = [0, 0]

            if keys[pygame.K_SPACE] and cat.vel[1] == 0: cat.vel[1]=-5
            if keys[pygame.K_a]: movement[0] -= 5
            if keys[pygame.K_d]: movement[0] += 5
            cat.move(tilemap,movement)            
            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            cat.render(offset=render_scroll)
            #print(tilemap.physics_rects_around(cat.pos,(4,2)))
            pygame.display.update()
            self.clock.tick(60)


