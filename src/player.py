import pygame
class Player:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image = image
        self.direction=True
        self.hitbox = pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
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
        if dx==0 :
            return
        if (dx<0) != self.direction: 
            self.image=pygame.transform.flip(self.image,True,False)
            self.direction=not self.direction
    
