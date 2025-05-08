import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Pygame Test')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill((30, 30, 46))  
    pygame.display.flip()  

pygame.quit()
