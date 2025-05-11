import pygame
NEIGHBOR_OFSETS=[(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(0,0),(-1,1),(0,1),(1,1)]
PHYSICS_TILES={"grass","dirt"}
class Tilemap:
    def __init__(self,game,tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap={}
        self.offgrid_tiles=[]
        for i in range (4):
            self.tilemap[str(12+i)+";30"]={"type": "grass","pos":(12+i,30)}
            self.tilemap[str(12+i)+";31"]={"type": "dirt","pos":(12+i,31)}
            self.tilemap["31;"+str(12+i)]={"type": "dirt","pos":(31,12+i)}

    
    def tiles_around(self, pos, size=(1, 1)):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        for dx in range(size[0]):  
            for dy in range(size[1]):  
                base_x = tile_loc[0] + dx
                base_y = tile_loc[1] + dy
                for offset in NEIGHBOR_OFSETS:
                    check_x = base_x + offset[0]
                    check_y = base_y + offset[1]
                    check_loc = f"{check_x};{check_y}"
                    if check_loc in self.tilemap:
                        tiles.append(self.tilemap[check_loc])
        return tiles
    def physics_rects_around(self,pos,size=(1,1)):
        rects=[]
        for tile in self.tiles_around(pos,size):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["pos"][0]*self.tile_size,tile["pos"][1]*self.tile_size,self.tile_size,self.tile_size))
        return rects


    def render (self):
        for tile in self.offgrid_tiles:
            self.game.screen.blit(self.game.assets[tile["type"]],tile["pos"])
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            self.game.screen.blit(self.game.assets[tile["type"]],(tile["pos"][0]*self.tile_size,tile["pos"][1]*self.tile_size))
        
        

