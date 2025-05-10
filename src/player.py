import pygame
import math
class Player:
    def __init__(self,x,y,image,game):
        self.x=x
        self.y=y
        self.image = image
        self.direction=True
        #self.hitbox = pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        self.hitbox = pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(x, y)
        self.hitbox = self.hitbox.inflate(-2, -14)
        self.hitbox=self.hitbox.move(-3,6)
        self.game=game
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        self.hitbox = self.hitbox.move(dx, dy)
        #image = pygame.image.load('../assets/player/cat.png')
        #image = pygame.transform.scale(image, (round(image.get_width()/2),round(image.get_height()/2)))

        #if dx>0:
        #self.image =  pygame.transform.flip(image, True, False)
        #if dx<0:
        # self.image = image
        if self.hitbox.colliderect(self.game.platform):
            i=10
            while self.hitbox.colliderect(self.game.platform) and i>0:
                self.x+= math.floor(-dx/2)
                self.y+=math.floor(-dy/2)
                self.hitbox=self.hitbox.move(math.floor(-dx/2),math.floor(-dy/2))
                i-=1
        if dx==0 :
            return
        if (dx<0) != self.direction: 
            self.image=pygame.transform.flip(self.image,True,False)
            self.direction=not self.direction
    
