from entity import Entity
from pathlib import Path
import pygame
BASE_DIR = Path(__file__).resolve().parent
class Player(Entity):
    def render(self,offset=(0,0)):
        real_offset=(offset[0],offset[1]+4)
        super().render(real_offset)
        #self.game.screen.blit(self.image,(self.pos[0] - offset[0],self.pos[1] - 4 - offset[1]))
        for i in range(self.health):
            self.game.screen.blit(pygame.image.load(BASE_DIR/"../assets/player/heart.png").convert_alpha(),(16 + i*16,32))
        for i in range(self.max_health - self.health):
            self.game.screen.blit(pygame.image.load(BASE_DIR/"../assets/player/empty_heart.png").convert_alpha(),(16 + (i+self.health)*16,32))
        for i in range(self.shield):
            self.game.screen.blit(pygame.image.load(BASE_DIR/"../assets/player/shield.png").convert_alpha(),(16 + i*16,16))
    

    def __init__(self,x,y,image,game,max_health,max_shield):  
        super().__init__(x,y,image,game,max_health,3,20,size=(2,1))
        self.shield=max_shield
        self.max_shield=max_shield
        self.health=max_health
        self.swinging = False
        self.swing_progress = 0
        self.swing_side = "right"
        self.swinging = False
        self.swing_progress = 0
        self.swing_dir = "right"
        self.swing_duration =20

    def move(self,tilemap,movement=(0,0)):
        super().move(tilemap,movement)

    

