from entity import Entity
import random
import pygame

class Enemy(Entity):
    def __init__(self, x, y, image, game, max_health, damage,dash_speed=0):
        super().__init__(x, y, image, game, max_health, damage,dash_speed)
        self.health = max_health
        self.damage = damage
        self.size = (1, 1)  # Size of the enemy entity
        self.walking=0


    def move(self, tilemap, movement=(0, 0)):

        if self.walking:
            if tilemap.solid_check((self.rect().centerx+(-7 if self.direction else 7), self.pos[1]+23)):
                if (self.collisions["right"] or self.collisions["left"]):
                    self.direction = not self.direction
                movement=(movement[0] - 0.5 if self.direction else 0.5,movement[1])
            else:
                self.direction = not self.direction
            self.walking= max(0, self.walking - 1)
            if not self.walking:
                dis=(self.game.cat.pos[0] - self.pos[0], self.game.cat.pos[1] - self.pos[1])
                if abs(dis[1]) <16:
                    if (self.direction and dis[0]< 0):
                        self.game.bullets.append([[self.rect().centerx-7,self.rect().centery],-1.5,0])
                    if (not self.direction and dis[0] > 0):
                        self.game.bullets.append([[self.rect().centerx+7,self.rect().centery],1.5,0])
        elif random.random() < 0.01:
            self.walking = random.randint(30,400)  
            self.direction = random.choice([True, False])
        super().move(tilemap, movement)

    def render(self,offset=(0,0)):
        super().render(offset)
        if self.direction:
            self.game.screen.blit(pygame.transform.flip(self.game.assets["gun"], True, False), (self.rect().centerx-4-self.game.assets["gun"].get_width() - offset[0],self.rect().centery - offset[1]))
        else:
            self.game.screen.blit(self.game.assets["gun"], (self.rect().centerx+10-self.game.assets["gun"].get_width() - offset[0],self.rect().centery - offset[1]))
