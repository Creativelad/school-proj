import pygame
import sys
from player import Player
from pathlib import Path
from tilemap import Tilemap
import random
BASE_DIR = Path(__file__).resolve().parent
class Game:
 

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.font = pygame.font.Font(BASE_DIR / "../assets/fonts/font1.ttf", 16)
        self.res = (1280//2, 720//2)
        self.screen = pygame.Surface(self.res)
        self.real_screen = pygame.display.set_mode((self.res[0]*2, self.res[1]*2))
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_resting_forward = True
        self.platform = pygame.Rect(100,450,675,166)
        self.assets = {
            "sand_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_brick.png").convert(),
            "sand_cracked_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_cracked_brick.png").convert(),
            "sand": pygame.image.load(BASE_DIR/"../assets/images/sand.png").convert(),
            "player_spawn": pygame.transform.scale(pygame.image.load(BASE_DIR / "../assets/player/cat.png").convert_alpha()
,(32,16)),
            "rat":(pygame.image.load(BASE_DIR / "../assets/enemy/rat.png")).convert_alpha()


        } 
        self.tilemap = Tilemap(self)
        try:
           self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0.0,0.0]
        self.bg = pygame.image.load(BASE_DIR/"../assets/images/bg.png").convert()
        self.bg = pygame.transform.scale(self.bg,(self.res[0],self.res[1]))
        cat_image = pygame.image.load(BASE_DIR / "../assets/player/cat.png").convert_alpha()
        cat_image= pygame.transform.scale(cat_image,(32,20))
        
        spawn = self.tilemap.extract("player_spawn", False)
        if spawn:
            x, y = spawn[0]["pos"]
            self.cat = Player(x*self.tilemap.tile_size, y*self.tilemap.tile_size, cat_image, self, 5, 5)
        else:
            self.cat = Player(0, 0, cat_image, self, 5, 5)



    def run(self):

        pygame.mixer.music.load(BASE_DIR / "../assets/music/bgm.ogg")
        # v ENABLE THIS BEFORE MAIN RELASE v 
        pygame.mixer.music.play(-1,0.0)
        

        while self.running:
            #self.screen.fill((30, 30, 46))
            self.screen.blit(self.bg, (0, 0))
            self.scroll[0] += (self.cat.rect().centerx - self.res[0] / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.cat.rect().centery - self.res[1] / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(offset=render_scroll)
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            movement = [0, 0]
            if keys[pygame.K_SPACE] and self.cat.vel[1] == 0:
                self.cat.vel[1]=-3
                pygame.mixer.music.load(BASE_DIR / "../assets/sounds/jump.ogg")
                pygame.mixer.music.play(0,0.0)
            if keys[pygame.K_a]: 
                movement[0] -= 3
            if keys[pygame.K_d]: 
                movement[0] += 3
             
            if mouse[0] and not self.cat.dashing:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                mouse_x_unscaled = mouse_x / 2
                mouse_y_unscaled = mouse_y / 2
                
                # Undo camera scroll (scroll holds world coordinates offset)
                mouse_world_x = mouse_x_unscaled + self.scroll[0]
                mouse_world_y = mouse_y_unscaled + self.scroll[1]
                
                # Player position in world coords (center of rect)
                player_x, player_y = self.cat.rect().center
                
                # Vector from player to mouse in world coords
                vec_x = mouse_world_x - player_x
                vec_y = mouse_world_y - player_y
                
                length = (vec_x**2 + vec_y**2)**0.5
                if length != 0:
                    normalized = (vec_x / length, vec_y / length)
                else:
                    normalized = (0, 0)

                self.cat.vel[0] = normalized[0] * 15
                self.cat.vel[1] = normalized[1] * 1 - 3
                self.cat.dashing = True
                
            self.cat.move(self.tilemap,movement) 

            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            self.cat.render(offset=render_scroll)
            #print(tilemap.physics_rects_around(cat.pos,(4,2)))
            #pygame.display.update()
            scaled_surface = pygame.transform.scale(self.screen,(self.res[0]*2, self.res[1]*2))
            self.real_screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)



