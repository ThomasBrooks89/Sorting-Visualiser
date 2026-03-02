import pygame
import sys

WIDTH = 2000
HEIGHT = 1200
FPS = 60
BG_COLOR = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("+x goes right, +y goes down")
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 15)

def draw_plus(surface, colour, size, x, y, width):
    offset = size // 2
    pygame.draw.line(surface, colour, (x - offset, y), (x + offset, y), width)
    pygame.draw.line(surface, colour, (x, y - offset), (x, y + offset), width)

    text_surface = font.render(f"{x}, {y}", True, colour)
    surface.blit(text_surface, (x+8, y+10))
    


def draw(surface):
    surface.fill(BG_COLOR)
    x, y = 0, 0

    while x <= WIDTH:
        while y <= HEIGHT:
            draw_plus(surface, "white", 20, x, y, 2)
            y += 100
        y = 0
        x += 100

    pygame.display.flip()


while running:
    dt = clock.tick(FPS) / 1000  # seconds since last frame

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard example
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw(screen)


pygame.quit()
sys.exit()