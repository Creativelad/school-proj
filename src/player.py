from entity import Entity
from pathlib import Path
import pygame
BASE_DIR = Path(__file__).resolve().parent
class Player(Entity):
    def render(self,offset=(0,0)):
        self.game.screen.blit(self.image,(self.pos[0] - offset[0],self.pos[1] - 4 - offset[1]))
        for i in range(self.health):
            self.game.screen.blit(pygame.image.load(BASE_DIR/"../assets/player/heart.png").convert_alpha(),(16 + i*16,32))
        for i in range(self.max_health - self.health):
            self.game.screen.blit(pygame.image.load(BASE_DIR/"../assets/player/empty_heart.png").convert_alpha(),(16 + (i+self.health)*16,32))
    

    def __init__(self,x,y,image,game,max_health,shield):  
        super().__init__(x,y,image,game,max_health,size=(2,1))
        self.shield=shield
        self.health=4

    def move(self,tilemap,movement=(0,0)):
        super().move(tilemap,movement)

    

