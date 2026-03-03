import pygame


def find_bar_widths(arr_len, gap_len, window_width):
    width_for_bars = window_width - 40  # bit of space on either side
    width_for_bars -= gap_len * (arr_len - 1)

    remaining_pixels = width_for_bars % arr_len
    width_for_bars -= remaining_pixels

    bar_width = width_for_bars // arr_len
    return bar_width, remaining_pixels


def draw_array(surface, array, highlights, actions, bar_width, gap_size):
    colour_per_idx = {}
    for i, colour in highlights:  
        colour_per_idx[i] = colour  # then anything not in the dict can default to white        

    for i, height in enumerate(array):
        colour = colour_per_idx.get(i, "white")
        pygame.draw.rect(surface, colour, (((i * (bar_width + gap_size) + 20)), 650-height, bar_width, height))  


def draw_buttons(buttons):
    for button in buttons:
        button.draw()


def draw_controls_box(surface, controls_box, controls_box_texts):
    pygame.draw.rect(surface, (75,75,75), controls_box, 4)
    box_centre = controls_box.x + (controls_box.width // 2)
    y = controls_box.y + 20

    for font, text in controls_box_texts:
        text = font.render(text, True, "white")
        text_rect = text.get_rect()  # make a box around the text, to find its centre
        text_rect.centerx = box_centre  # the centre of the text is the centre of the box
        surface.blit(text, (text_rect.x, y))
        y += 40
    
    text = font.render("Thomas Loves Jen", True, "deeppink3")
    text_rect = text.get_rect()
    text_rect.centerx = box_centre
    text_rect.y = (controls_box.y + controls_box.height) - 40
    surface.blit(text, text_rect)


def draw_sort_info_box(surface, sort_info_box, chosen_sort_btn, stats, font):
    pygame.draw.rect(surface, (75,75,75), sort_info_box, 4)
    text = chosen_sort_btn.label
    text_rect = text.get_rect()
    text_rect.centerx = sort_info_box.centerx
    surface.blit(text, (text_rect.x, sort_info_box.y + 20))

    x = sort_info_box.x + 10
    y = sort_info_box.y + 60
    for stat in stats:
        text = font.render(stat, True, "white")
        surface.blit(text, (x, y))
        y += 40


def draw_config_box(surface, config_box):
    pygame.draw.rect(surface, (75,75,75), config_box, 4)


def draw_sort_explanation_box(surface, sort_explanation_box):
    pygame.draw.rect(surface, (75,75,75), sort_explanation_box, 4)


def mute_button_pressed(mute_btn):
    mute_btn.active = not mute_btn.active
    if mute_btn.active:
        return False  # sound is now muted
    return True  # sound is now unmuted
