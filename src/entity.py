import pygame
import math
class Entity:
    def __init__(self,x,y,image,game):
        self.pos=[x,y]
        self.image = image.convert_alpha()
        self.direction=True
        self.hitbox = pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(self.pos[0], self.pos[1])
        self.game=game
        self.vel=[0.0,0.0]
    def move(self,movement=(0,0)):
        frame_movement=(self.vel[0]+movement[0],self.vel[1]+movement[1])
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        #self.vel[1]=min(5,self.vel[1]+0.1)
        self.hitbox = pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(self.pos[0], self.pos[1])
        if self.hitbox.colliderect(self.game.platform):
            i=100
            while self.hitbox.colliderect(self.game.platform) and i>0:
                self.pos[0]+= math.floor(-frame_movement[0]/2)
                self.pos[1]+=math.floor(-frame_movement[1]/2)
                self.hitbox=pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(self.pos[0], self.pos[1])
                i-=1
        if frame_movement[0]==0 :
            return
        if (frame_movement[0]<0) != self.direction: 
            self.image=pygame.transform.flip(self.image,True,False)
            self.direction=not self.direction

    def render (self):
        self.game.screen.blit(self.image,(self.pos[0],self.pos[1]))
    
    def adjustHitbox(self):
        pass
    
