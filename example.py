import pygame
# 1. Setup (Manual Initialization)
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
# 2. THE MAIN LOOP (The App-Controlled Approach)
while running:
    # Manual Event Handling (CS Concept: Queue Processing)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Logic & Math (Vector updates)
    # player_pos += velocity * dt
    # Rendering (Manual Buffer Management)
    screen.fill((0, 0, 0))      # Clear the screen
    pygame.draw.circle(screen, "red", (400, 300), 40) 
    pygame.display.flip()       # "Swap Buffers" - Show the new frame
    clock.tick(60)              # Manual Framerate Control (Optimization)
pygame.quit() 