import pygame
import math
class Entity:
    def __init__(self,x,y,image,game):
        self.pos=[x,y]
        self.image = image
        self.direction=True
        self.hitbox = pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(x, y)
        self.hitbox = self.hitbox.inflate(-2, -14)
        self.hitbox=self.hitbox.move(-3,6)
        self.game=game
    def move(self,dx,dy):
        self.pos[0] += dx
        self.pos[1] += dy
        self.hitbox = self.hitbox.move(dx, dy)
        if self.hitbox.colliderect(self.game.platform):
            i=100
            while self.hitbox.colliderect(self.game.platform) and i>0:
                self.pos[0]+= math.floor(-dx/2)
                self.pos[1]+=math.floor(-dy/2)
                self.hitbox=self.hitbox.move(math.floor(-dx/2),math.floor(-dy/2))
                i-=1
        if dx==0 :
            return
        if (dx<0) != self.direction: 
            self.image=pygame.transform.flip(self.image,True,False)
            self.direction=not self.direction
    
