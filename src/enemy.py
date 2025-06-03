from entity import Entity
import random

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
        elif random.random() < 0.01:
            self.walking = random.randint(30,120)  # Randomly start walking for 1 to 60 frames
        super().move(tilemap, movement)
