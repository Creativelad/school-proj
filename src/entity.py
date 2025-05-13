import pygame
class Entity:
    def __init__(self,x,y,image,game,size=(1,1)):
        self.pos=[x,y]
        self.image = image.convert_alpha()
        self.direction=True
        self.hitbox = pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(self.pos[0], self.pos[1])
        self.game=game
        self.vel=[0.0,0.0]
        self.collisions = {"up":False,"down":False,"left":False,"right":False}
        self.size=size

    def move(self,tilemap,movement=(0,0)):
        self.collisions = {"up":False,"down":False,"left":False,"right":False}

        frame_movement=(self.vel[0]+movement[0],self.vel[1]+movement[1])

        self.pos[0] += frame_movement[0]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos,self.size):
            if entity_rect.colliderect(rect):
                if frame_movement[0]>0:
                    entity_rect.right=rect.left
                    self.collisions["right"]=True
                if frame_movement[0]<0:
                    entity_rect.left=rect.right
                    self.collisions["left"]=True
                self.pos[0]=entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos,self.size):
            if entity_rect.colliderect(rect):
                if frame_movement[1]>0:
                    entity_rect.bottom=rect.top
                    self.collisions["down"]=True
                if frame_movement[1]<0:
                    entity_rect.top=rect.bottom
                    self.collisions["up"]=True
                self.pos[1]=entity_rect.y

        self.vel[1]=min(5,self.vel[1]+0.1)
        if self.collisions["down"]or self.collisions["up"]:
            self.vel[1]=0

        if frame_movement[0]==0 :
            return

        if (frame_movement[0]<0) != self.direction: 
            self.image=pygame.transform.flip(self.image,True,False)
            self.direction=not self.direction

    def render (self):
        self.game.screen.blit(self.image,(self.pos[0],self.pos[1]))

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0]*16,16*self.size[1])
