import pygame

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


def stitch_text(text_list, font):  # list of (text string, colour) tuples
    # render all the strings
    rendered_texts = []
    for string, colour in text_list:
         rendered_text = font.render(string, True, colour)
         rendered_texts.append(rendered_text)

    # work out the size of the strings all together
    width, height = 0, 0
    for text in rendered_texts:
        width += text.get_width()
        height = max(height, text.get_height())

    # create the surface to blit the strings, and blit them all to it
    text_surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
    x = 0
    for text in rendered_texts:
        text_surface.blit(text, (x, (height - text.get_height())))
        x += text.get_width()

    return text_surface