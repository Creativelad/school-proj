import pygame
class Entity:
    def __init__(self,x,y,image,game,health,size=(1,1)):
        self.pos=[x,y]
        self.image = image.convert_alpha()
        self.direction=True
        self.hitbox = pygame.mask.from_surface(self.image).get_bounding_rects()[0].move(self.pos[0], self.pos[1])
        self.game=game
        self.vel=[0.0,0.0]
        self.dash_vel=[0.0,0.0]
        self.dash_norm=(0.0,0.0)
        self.collisions = {"up":False,"down":False,"left":False,"right":False}
        self.size=size
        self.health=health
        self.max_health=health
        self.dashing = False

    def move(self,tilemap,movement=(0,0)):
        self.collisions = {"up":False,"down":False,"left":False,"right":False}

        frame_movement=(self.vel[0]+movement[0]+self.dash_vel[0],self.vel[1]+movement[1]+self.dash_vel[1])

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
            self.dash_vel[1]=0
        if self.collisions["left"] or self.collisions["right"]:
            self.vel[0]=0
            self.dash_vel[0]=0


        if (frame_movement[0]<0) != self.direction and frame_movement[0]!=0 : 
            self.image=pygame.transform.flip(self.image,True,False)
            self.direction=not self.direction

        if self.vel[0]>0:
            self.vel[0]=max(0,self.vel[0]-0.1)
        
        if self.vel[0]<0:
            self.vel[0]=min(0,self.vel[0]+0.1)
        
        if self.dash_vel[0]==0 and self.dash_vel[1]==0:
            self.dashing=False


        if self.dashing:

            for i in (0, 1):
                    change = self.dash_norm[i] * 0.1
                    # If dash_vel and dash_norm have the same sign
                    if (self.dash_vel[i] > 0 and self.dash_norm[i] > 0) or (self.dash_vel[i] < 0 and self.dash_norm[i] < 0):
                        self.dash_vel[i] -= change
                        # Prevent overshooting zero
                        if (self.dash_vel[i] > 0 and self.dash_vel[i] - change < 0) or (self.dash_vel[i] < 0 and self.dash_vel[i] - change > 0):
                            self.dash_vel[i] = 0










    def render (self):
        self.game.screen.blit(self.image,(self.pos[0],self.pos[1]))

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0]*16,16*self.size[1])
