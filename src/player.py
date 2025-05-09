import pygame
class Player:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image = image
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        image = pygame.image.load('../assets/player/cat.png')
        image = pygame.transform.scale(image, (round(image.get_width()/2),round(image.get_height()/2)))

        if dx>0:
            self.image =  pygame.transform.flip(image, True, False)
        if dx<0:
             self.image = image
    
