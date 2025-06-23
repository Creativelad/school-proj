
import sys
import pygame
from pathlib import Path
from tilemap import Tilemap
BASE_DIR = Path(__file__).resolve().parent
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Editor')
        self.font = pygame.font.Font(BASE_DIR / "../assets/fonts/font1.ttf", 16)
        # Create an 800×600 window directly (no intermediate surface)
        self.clock = pygame.time.Clock()
        self.res = (1280//2, 720//2)
        self.screen = pygame.Surface(self.res)
        self.real_screen = pygame.display.set_mode((self.res[0]*2, self.res[1]*2))
        # Load tile assets (same as original: 'decor', 'grass', etc.)
        self.assets = {
            "sand_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_brick.png").convert_alpha(),

            "sand_cracked_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_cracked_brick.png"),
            "sand": pygame.image.load(BASE_DIR/"../assets/images/sand.png").convert_alpha(),
            "player_spawn": pygame.transform.scale(pygame.image.load(BASE_DIR / "../assets/player/cat.png").convert_alpha()
,(32,16)),
            "rat":(pygame.image.load(BASE_DIR / "../assets/enemy/rat.png")).convert_alpha(),
            "flag":(pygame.image.load(BASE_DIR / "../assets/images/flag.png")).convert_alpha()


        }      
        self.tilemap = Tilemap(self, tile_size=16)
        
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        # Scrolling and input state
        self.scroll = [0, 0]
        self.movement = [False, False, False, False]  # left, right, up, down
        self.shift = False
        
        # Current tile selection
        self.tile_list = list(self.assets)
        self.tile_group = 0
        
        # Mouse state
        self.clicking = False
        self.right_clicking = False
        self.placing_text = False    
        self.is_typing     = False    
        self.typing_text   = ""       
        self.typing_pos    = (0,0)

        self.is_player_spawner= False
        self.is_player_spawner=bool(self.tilemap.extract("player_spawn", True))




    def run(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Keyboard for scrolling (arrow keys or WASD)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o and not (self.placing_text or self.is_typing):
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_t:
                        self.placing_text = True
                        print("Text mode: click to choose location")
                    if event.key in (pygame.K_LEFT, pygame.K_a) and not (self.placing_text or self.is_typing):
                        self.movement[0] = True
                    if event.key in (pygame.K_RIGHT, pygame.K_d) and not (self.placing_text or self.is_typing):
                        self.movement[1] = True
                    if event.key in (pygame.K_UP, pygame.K_w) and not (self.placing_text or self.is_typing):
                        self.movement[2] = True
                    if event.key in (pygame.K_DOWN, pygame.K_s) and not (self.placing_text or self.is_typing):
                        self.movement[3] = True
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and not (self.placing_text or self.is_typing):
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.movement[0] = False
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.movement[1] = False
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.movement[2] = False
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.movement[3] = False
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        self.shift = False
                # Mouse button down: set clicking state or change tile selection
                # Mouse Scroll (Up/Down) switches tile type (group)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll Up
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)  # Switch to previous tile group
                    elif event.button == 5:  # Scroll Down
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)  # Switch to next tile group
                if self.placing_text and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                     real_x, real_y = event.pos
                     mx, my = real_x // 2, real_y // 2          # map into 640×360 canvas
                     # now convert to grid coords
                     gx = (mx + self.scroll[0]) // self.tilemap.tile_size
                     gy = (my + self.scroll[1]) // self.tilemap.tile_size
                     self.typing_pos    = (int(gx), int(gy))
                     self.typing_text   = ""
                     self.is_typing     = True
                     self.placing_text  = False
                     print("Typing text: press ENTER to finish")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        self.clicking = True
                    if event.button == 3:  # right click
                        self.right_clicking = True
                    # Mouse wheel / scroll to change tile group/variant
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if self.is_typing and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # commit to tilemap
                        self.tilemap.texts.append({
                            'pos':  self.typing_pos,
                            'text': self.typing_text
                        })
                        self.is_typing = False
                        print(f"Committed text: {self.typing_text!r}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.typing_text = self.typing_text[:-1]
                    else:
                        self.typing_text += event.unicode

            # Update scroll offset
            # (Right minus left, down minus up) – matching reference scroll logic:contentReference[oaicite:5]{index=5}
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 4
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 4

            # Clear the screen
            self.screen.fill((30, 30, 46))
            # Render existing tiles (using the scroll offset)
            render_offset = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(offset=render_offset)

            # Draw ghost (preview) tile under mouse
            empos = pygame.mouse.get_pos()              # raw mouse pos (no scaling)
            mpos = (empos[0] // 2, empos[1] // 2)

            # Compute tile coordinates by adding scroll and dividing by tile_size:contentReference[oaicite:6]{index=6}
            tile_x = int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size)
            tile_y = int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size)
            current_img = self.assets[self.tile_list[self.tile_group]].copy()
            current_img.set_alpha(100)  # semi-transparent
            # Blit ghost tile at (tile_pos*tile_size - scroll):contentReference[oaicite:7]{index=7}
            self.screen.blit(current_img, (
                tile_x * self.tilemap.tile_size - self.scroll[0],
                tile_y * self.tilemap.tile_size - self.scroll[1]
            ))

            # Place or remove tile in the tilemap dictionary
            key = f"{tile_x};{tile_y}"
            if self.clicking and not (self.placing_text or self.is_typing):
                
                # Write new tile info into internal tilemap dict:contentReference[oaicite:8]{index=8}
                if not(self.tile_list[self.tile_group] == "player_spawn") :
                    self.tilemap.tilemap[key] = {
                        'type': self.tile_list[self.tile_group],
                        'pos': (tile_x, tile_y)
                    }
                elif self.tile_list[self.tile_group] == "player_spawn" and not self.is_player_spawner:
                    self.tilemap.tilemap[key] = {
                        'type': self.tile_list[self.tile_group],
                        'pos': (tile_x, tile_y)
                    }
                    self.is_player_spawner = True
            if self.right_clicking :
                if key in self.tilemap.tilemap:
                # Delete tile if it exists:contentReference[oaicite:9]{index=9}
                    del self.tilemap.tilemap[key]
                
                self.tilemap.texts[:] = [
                    obj for obj in self.tilemap.texts
                     if obj['pos'] != (tile_x, tile_y)
                ]
                

            if self.is_typing:
                px, py = self.typing_pos
                preview_surf = self.font.render(self.typing_text + "|", True, (200,200,255))
                self.screen.blit(
                    preview_surf,
                    (px * self.tilemap.tile_size - self.scroll[0],
                     py * self.tilemap.tile_size - self.scroll[1])
                )
            # Update the display at native resolution
            scaled_surface = pygame.transform.scale(self.screen,(self.res[0]*2, self.res[1]*2))
            self.real_screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.is_player_spawner=bool(self.tilemap.extract("player_spawn", True))
            self.clock.tick(60)

