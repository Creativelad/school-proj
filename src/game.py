import pygame
import math
import sys
import time
from enemy import Enemy
from player import Player
from pathlib import Path
from tilemap import Tilemap
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
        self.assets = {
            "sand_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_brick.png").convert(),
            "sand_cracked_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_cracked_brick.png").convert(),
        "sand": pygame.image.load(BASE_DIR/"../assets/images/sand.png").convert(),
            "player_spawn": pygame.transform.scale(pygame.image.load(BASE_DIR / "../assets/player/cat.png").convert_alpha()
,(32,16)),
            "rat":(pygame.image.load(BASE_DIR / "../assets/enemy/rat.png")).convert_alpha(),
            "gun": (pygame.image.load(BASE_DIR / "../assets/enemy/gun.png").convert_alpha()),
            "bullets":(pygame.image.load(BASE_DIR / "../assets/enemy/bullet.png").convert_alpha()),
            "flag":(pygame.image.load(BASE_DIR / "../assets/images/flag.png")).convert_alpha(),
            "blahaj":(pygame.image.load(BASE_DIR / "../assets/images/blahaj.png")).convert()


        }
        self.tilemap= Tilemap(self)
        self.level=0
        self.load_level(self.level)
        self.bg_music = pygame.mixer.Sound(BASE_DIR / "../assets/music/bgm.ogg")
        self.bg_music.play(-1)
        self.jump_sound = pygame.mixer.Sound(BASE_DIR / "../assets/sounds/jump.ogg")
        

    def load_level(self,map_id):
        
        if self.level == 12:
            print("thats it! the games over")
            pygame.quit()
            sys.exit()
        self.tilemap.load(BASE_DIR.parent /"assets" / "levels" / f"{map_id}.json")
        self.scroll = [0.0,0.0]
        self.bullets = []
        self.bg = pygame.image.load(BASE_DIR/"../assets/images/bg.png").convert()
        self.bg = pygame.transform.scale(self.bg,(self.res[0],self.res[1]))
        self.sword_right = pygame.image.load(BASE_DIR / "../assets/images/sword.png").convert_alpha()
        self.sword_left = pygame.transform.flip(self.sword_right, True, False)
        cat_image = pygame.image.load(BASE_DIR / "../assets/player/cat.png").convert_alpha()
        cat_image = pygame.transform.scale(cat_image,(32,20))
        
        spawn = self.tilemap.extract("player_spawn", False)
        if spawn:
            x, y = spawn[0]["pos"]
            self.cat = Player(x*self.tilemap.tile_size, y*self.tilemap.tile_size, cat_image, self, 5, 5)
        else:
            self.cat = Player(0, 0, cat_image, self, 5, 5)

        enemy_spawners=["rat"]
        self.enemies = []
        for enemy in enemy_spawners:
            spawn = self.tilemap.extract(enemy, False)
            if spawn:
                for s in spawn:
                    x, y = s["pos"]
                    self.enemies.append(Enemy(x*self.tilemap.tile_size,y*self.tilemap.tile_size,self.assets[enemy],self,1,1))
        self.last_swing_time = 0.0
        self.real_swing_cooldown = 0.2
        self.swing_cooldown = self.real_swing_cooldown+self.cat.swing_duration/60
        self.fcount = 0
        self.cat.health=self.cat.max_health
        self.cat.shield=self.cat.max_shield
        self.sword_x = 0.0 
        self.sword_y = 0.0
        flag_spawn = self.tilemap.extract("flag", True)
        self.flag_pos = None
        if flag_spawn:
            x, y = flag_spawn[0]["pos"]
            self.flag_pos = (x * self.tilemap.tile_size, y * self.tilemap.tile_size)
        if self.level == 11:
            self.bg_music.stop()
            end_music = pygame.mixer.Sound(BASE_DIR / "../assets/music/end.ogg")
            end_music.play()



    def run(self):

        self.sword_x = 0.0 
        self.sword_y = 0.0
        regen_timer = 0

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
                self.jump_sound.play()

            if keys[pygame.K_a]: 
                movement[0] -= self.cat.speed
                self.cat.direction=True
                #print(self.cat.dash_time)
            if keys[pygame.K_d]: 
                movement[0] += self.cat.speed
                self.cat.direction=False

            if mouse[2] and (not self.cat.dashing) and self.cat.dash_time == 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                mouse_x_unscaled = mouse_x / 2
                mouse_y_unscaled = mouse_y / 2
                
                mouse_world_x = mouse_x_unscaled + self.scroll[0]
                mouse_world_y = mouse_y_unscaled + self.scroll[1]
                
                player_x, player_y = self.cat.rect().center
                
                vec_x = mouse_world_x - player_x
                vec_y = mouse_world_y - player_y
                
                length = (vec_x**2 + vec_y**2)**0.5
                if length != 0:
                    normalized = (vec_x / length, vec_y / length)
                else:
                    normalized = (0, 0)

                self.cat.dash_norm=normalized
                self.cat.dash_vel[0] = normalized[0]*self.cat.dash_speed 
                self.cat.dash_vel[1] = normalized[1]*self.cat.dash_speed//2
                self.cat.dashing = True
                self.cat.dash_time = self.cat.max_dash_cd
               
            if mouse[0] and not self.cat.swinging and time.time() - self.last_swing_time >= self.swing_cooldown:
                 mouse_x, mouse_y = pygame.mouse.get_pos()
                 player_x, player_y = self.cat.rect().center
                 dx = (mouse_x / 2) - (player_x - render_scroll[0])
                 dy = (mouse_y / 2) - (player_y - render_scroll[1])

                 if abs(dx) > abs(dy):
                     self.cat.swing_dir = "right" if dx > 0 else "left"
                 else:
                     self.cat.swing_dir = "down" if dy > 0 else "up"

                 self.cat.swinging = True
                 self.cat.swing_progress = 0
                 self.last_swing_time = time.time()


            if self.cat.swinging:
                 center_x, center_y = self.cat.rect().center
                 center_x -= render_scroll[0]
                 center_y -= render_scroll[1]

                 progress_ratio = self.cat.swing_progress / self.cat.swing_duration
                 arc_angle = 90
                 radius = 32

                 start_angle = {
                     "right": -45,
                     "left": -135,
                     "up": -135,
                     "down": 45
                 }[self.cat.swing_dir]
                 if self.cat.swing_dir == "left":
                     current_angle = start_angle - arc_angle * progress_ratio
                 else:
                     current_angle = start_angle + arc_angle * progress_ratio

                 radians = math.radians(current_angle)

                 self.sword_x = center_x + radius * math.cos(radians)
                 self.sword_y = center_y + radius * math.sin(radians)

                 rotated_sword = pygame.transform.rotate(self.sword_right, -current_angle)
                 rect = rotated_sword.get_rect(center=(self.sword_x, self.sword_y))
                 self.screen.blit(rotated_sword, rect.topleft)            
                 self.cat.swing_progress += 1
                 if self.cat.swing_progress > self.cat.swing_duration:
                    self.cat.swinging = False

            self.cat.move(self.tilemap,movement)

            for event in pygame.event.get():
                 if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                     self.fcount += 1
                     if self.fcount == 7:
                         self.fcount = 0
                         pygame.mixer.Sound(BASE_DIR / "../assets/sounds/meow.ogg").play()

            for enemy in self.enemies.copy():
                enemy.move(self.tilemap,(0,0))
                enemy.render(render_scroll)
                if self.cat.swinging:
                     sword_point = pygame.math.Vector2(self.sword_x, self.sword_y)  
                     enemy_point = pygame.math.Vector2(enemy.pos[0] - self.scroll[0],enemy.pos[1] - self.scroll[1])
                     if sword_point.distance_to(enemy_point) < 16:
                         self.enemies.remove(enemy)


            self.cat.render(offset=render_scroll)
            #print(tilemap.physics_rects_around(cat.pos,(4,2)))
            #pygame.display.update()
            for bullet in self.bullets.copy():
                bullet[0][0] += bullet[1]
                bullet[2]+=1 
                img =self.assets["bullets"] 
                self.screen.blit(img,(bullet[0][0]-img.get_width()/2-self.scroll[0], bullet[0][1]-img.get_height()/2-self.scroll[1]))
                if self.tilemap.solid_check(bullet[0]):
                    self.bullets.remove(bullet)
                elif bullet[2] > 360:
                    self.bullets.remove(bullet)
                elif not self.cat.dashing and self.cat.rect().collidepoint(bullet[0]):
                    self.bullets.remove(bullet)
                    if self.cat.shield>0:
                        self.cat.shield -= 1
                    elif self.cat.health > 0:
                        self.cat.health -= 1
                    if self.cat.health <= 0:
                        self.level= 0
                        self.load_level(self.level)
                        break
                if self.cat.swinging:
                     sword_point = pygame.math.Vector2(self.sword_x, self.sword_y)  
                     bullet_point = pygame.math.Vector2(bullet[0][0] - self.scroll[0], bullet[0][1] - self.scroll[1])
                     if sword_point.distance_to(bullet_point) < 16:
                         self.bullets.remove(bullet)



            if self.flag_pos:
                 flag_rect = pygame.Rect(self.flag_pos[0], self.flag_pos[1], 16, 16)
                 if self.cat.rect().colliderect(flag_rect):
                     self.level = self.level+1
                     self.load_level(self.level)
            regen_timer+=1
            if regen_timer>300:
                regen_timer=0
                if self.cat.health < self.cat.max_health:
                 self.cat.health+=1
            scaled_surface = pygame.transform.scale(self.screen,(self.res[0]*2, self.res[1]*2))
            if self.cat.pos[1]>1000:
                self.load_level(self.level)
            self.real_screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
