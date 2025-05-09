class Player:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image = image
    def move(self,dx,dy,image):
        self.x += dx
        self.y += dy
        self.image = image
    
