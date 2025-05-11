from entity import Entity
class Player(Entity):
    def render (self):
        self.game.screen.blit(self.image,(self.pos[0],self.pos[1]-8))
    

    def __init__(self,x,y,image,game):  
        super().__init__(x,y,image,game)

    def move(self,tilemap,movement=(0,0)):
        super().move(tilemap,movement)

    

