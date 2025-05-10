from entity import Entity
class Player(Entity):
    def adjustHitbox(self):
        self.hitbox = self.hitbox.inflate(-2, -14)
        self.hitbox=self.hitbox.move(-3,6)

    def __init__(self,x,y,image,game):  
        super().__init__(x,y,image,game)
        self.adjustHitbox()


    def move(self,movement=(0,0)):
        super().move(movement)
        self.adjustHitbox()

    

