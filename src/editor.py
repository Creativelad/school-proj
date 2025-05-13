
import sys
import pygame
from pathlib import Path
from tilemap import Tilemap
BASE_DIR = Path(__file__).resolve().parent
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Editor')
        # Create an 800×600 window directly (no intermediate surface)
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.res = (800, 600)
        # Load tile assets (same as original: 'decor', 'grass', etc.)
        self.assets = {
            "dirt":pygame.image.load(BASE_DIR/"../assets/images/5.png").convert_alpha(),
            "grass":pygame.image.load(BASE_DIR/"../assets/images/1.png").convert_alpha(),
            "sand_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_brick.jpg").convert_alpha(),
            "sand_cracked_brick":pygame.image.load(BASE_DIR/"../assets/images/sand_cracked_brick.jpg"),
            "sand": pygame.image.load(BASE_DIR/"../assets/images/sand.png").convert_alpha()

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

    def run(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Keyboard for scrolling (arrow keys or WASD)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.movement[0] = True
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.movement[1] = True
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.movement[2] = True
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.movement[3] = True
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
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
            mpos = pygame.mouse.get_pos()              # raw mouse pos (no scaling)
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
            if self.clicking:
                # Write new tile info into internal tilemap dict:contentReference[oaicite:8]{index=8}
                self.tilemap.tilemap[key] = {
                    'type': self.tile_list[self.tile_group],
                    'pos': (tile_x, tile_y)
                }
            if self.right_clicking and key in self.tilemap.tilemap:
                # Delete tile if it exists:contentReference[oaicite:9]{index=9}
                del self.tilemap.tilemap[key]

            # Update the display at native resolution
            pygame.display.update()
            self.clock.tick(60)

