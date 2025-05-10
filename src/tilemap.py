class Tilemap:
    def __init__(self,game,tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap={}
        self.offgrid_tiles=[]
        self.tilemap["15;20"]={"type": "dirt","pos":(15,20)}
        self.tilemap["16;21"]={"type": "dirt","pos":(16,21)}
        for i in range (10):
            self.tilemap[str(12+i)+";30"]={"type": "grass","pos":(12+i,30)}
            self.tilemap[str(12+i)+";31"]={"type": "dirt","pos":(12+i,31)}
            self.tilemap[str(12+i)+";32"]={"type": "dirt","pos":(12+i,32)}
            self.tilemap[str(12+i)+";33"]={"type": "dirt","pos":(12+i,33)}
    
    def render (self):
        for tile in self.offgrid_tiles:
            self.game.screen.blit(self.game.assets[tile["type"]],tile["pos"])
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            self.game.screen.blit(self.game.assets[tile["type"]],(tile["pos"][0]*self.tile_size,tile["pos"][1]*self.tile_size))
        
        

