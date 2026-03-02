import pygame
import sys

pygame.init()
font = pygame.font.Font(None, 32)

class Button():
    width = 180
    height = 80
    
    def __init__(self, surface, x, y, label, font):
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.label = font.render(label, True, "white")
        self.font = font
        self.mouseover = False
        self.clicked = False
        self.active = False
    
    def draw(self):
        # first see if user has their mouse cursor over the button
        mouse_pos = pygame.mouse.get_pos()
        self.mouseover = self.rect.collidepoint(mouse_pos)  # "has the mouse cursor collided with me?"

        if self.clicked:
            pygame.draw.rect(self.surface, (65, 65, 65), self.rect, border_radius=8)
        elif self.mouseover:
            pygame.draw.rect(self.surface, (75, 75, 75), self.rect, border_radius=8)
        else:
            pygame.draw.rect(self.surface, (55, 55, 55), self.rect, border_radius=8)

        if self.active:
            pygame.draw.rect(self.surface, "deepskyblue2", self.rect, border_radius=8, width=2)
        else:
            pygame.draw.rect(self.surface, (40, 40, 40), self.rect, border_radius=8, width=2)

        # blit the text---the label---this centres the text on the centre of self.rect
        self.surface.blit(self.label, self.label.get_rect(center=self.rect.center))


    def event(self, event):
        # "have I been clicked?"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                return True

        # turn the clicked flag off when the user releases the button    
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.clicked:
                self.clicked = False
        return False



def draw_plus(surface, colour, size, x, y, width):
    offset = size // 2
    pygame.draw.line(surface, colour, (x - offset, y), (x + offset, y), width)
    pygame.draw.line(surface, colour, (x, y - offset), (x, y + offset), width)
















if __name__ == "__main__":
    WIDTH = 2000
    HEIGHT = 1200
    FPS = 60
    BG_COLOR = (18, 18, 18)
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

    btn = Button(screen, 750, 250, "poo", font)

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
        btn.draw()
        pygame.display.flip()


    pygame.quit()
    sys.exit()