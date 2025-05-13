import pygame
import json
NEIGHBOR_OFSETS=[(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(0,0),(-1,1),(0,1),(1,1)]
PHYSICS_TILES={"grass","dirt","sand_brick","sand_cracked_brick"}
class Tilemap:
    def __init__(self,game,tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap={}
        self.offgrid_tiles=[]
        self.texts=[]
           
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


    def render(self, offset=(0,0)):
         for tile in self.offgrid_tiles:
            self.game.screen.blit(self.game.assets[tile["type"]],(tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

         for x in range(offset[0]//self.tile_size,(offset[0]+self.game.res[0])//self.tile_size+1):
            for y in range(offset[1]//self.tile_size,(offset[1]+self.game.res[1])//self.tile_size+1):
                loc = str(x)+";"+str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    self.game.screen.blit(self.game.assets[tile["type"]],(tile["pos"][0]*self.tile_size - offset[0],tile["pos"][1]*self.tile_size - offset[1]))

           
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles,'texts': self.texts}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        self.texts = map_data['texts']
        

