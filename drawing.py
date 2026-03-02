import pygame
import sys
import sorting_logic
import pygame_gui
#from random import randint

# constants
WIDTH, HEIGHT = 2000, 1200
FPS = 120
BG_COLOUR = (0, 0, 0)

# pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 32)
font_sml = pygame.font.Font(None, 28)
font_big = pygame.font.Font(None, 40)
pygame.display.set_caption("Sorting Algorithms")
clock = pygame.time.Clock()
running = True
next_iteration = 0
game_speed = 50
paused = False
muted = False

def find_bar_widths(arr_len, gap_len):
    width_for_bars = WIDTH - 40  # bit of space on either side
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



def reset_sort(surface, chosen_sort, arr_len):
    array = sorting_logic.generate_array(1, arr_len)
    sort = sorts[chosen_sort](array)
    step = next(sort)
    draw_array(surface, step.array, step.highlights, step.actions, bar_width, gap_len)
    pygame.display.flip()
    return array, sort, step

def mute_button_pressed(mute_btn):
    mute_btn.active = not mute_btn.active
    if mute_btn.active:
        return False  # sound is now muted
    return True  # sound is now unmuted

# logic vars
arr_len = 650  # max of 650 since 650 sized bars hit the top of the screen
gap_len = 1  #num pixels between bars
bar_width, leftover_bar_pixels = find_bar_widths(arr_len, gap_len)
chosen_sort = "selection"
sorts = {"selection": sorting_logic.selection_sort,
         "bubble": sorting_logic.bubble_sort,
         "insertion": sorting_logic.insertion_sort,
         "shell": sorting_logic.shell_sort}
array = sorting_logic.generate_array(1, arr_len)
sort = sorts[chosen_sort](array)
step = next(sort, None)

# button setup
btn_selection_sort = pygame_gui.Button(screen, 40, 1080, "Selection Sort", font)
btn_bubble_sort = pygame_gui.Button(screen, 240, 1080, "Bubble Sort", font)
btn_insertion_sort = pygame_gui.Button(screen, 440, 1080, "Insertion Sort", font)
btn_shell_sort = pygame_gui.Button(screen, 640, 1080, "Shell Sort", font)
btn_merge_sort = pygame_gui.Button(screen, 840, 1080, "Merge Sort", font)
btn_quicksort = pygame_gui.Button(screen, 1040, 1080, "Quicksort", font)
btn_heap_sort = pygame_gui.Button(screen, 1240, 1080, "Heap Sort", font)
btn_reset = pygame_gui.Button(screen, (1950 - pygame_gui.Button.width), 1080, "Reset", font)
btn_mute = pygame_gui.Button(screen, (btn_reset.rect.x - pygame_gui.Button.width - 20), 1080, "Mute", font)
buttons = [btn_selection_sort, btn_bubble_sort, btn_insertion_sort, btn_shell_sort, btn_merge_sort, btn_quicksort, btn_heap_sort, btn_reset, btn_mute]
chosen_sort_btn = btn_selection_sort
chosen_sort_btn.active = True

# 'controls' box setup
controls_box = pygame.Rect((btn_mute.rect.x, 670, (pygame_gui.Button.width * 2) + 20, 390))
controls_box_texts = [(font, "Controls"),
                      (font_sml, "1-7: Change sort"),
                      (font_sml, "R: Reset"),
                      (font_sml, "Space: Pause/Play"),
                      (font_sml, "K/L: Speed -/+"),
                      (font_sml, "S: Step forwards"),
                      (font_sml, "M: Mute sounds"),
                      (font_sml, "Esc: Quit")]

# 'sort info' box setup
sort_info_box = pygame.Rect((btn_selection_sort.rect.x, 670, (pygame_gui.Button.width * 2) + 40, 390))




# main loop
while running:

    curr_fps = clock.get_fps()
    if curr_fps < 60 and curr_fps > 0:
        print(curr_fps)

    dt = clock.tick(FPS)
    screen.fill(BG_COLOUR)

    if not paused:
        next_iteration += dt
    if next_iteration >= game_speed:
        next_iteration = 0

        # dont update step if the sort is finished
        new_step = next(sort, None)
        if new_step is not None:
            step = new_step

            if "pass_done" in step.actions:
                next_iteration -= ((game_speed + 12) * 10)

    draw_array(screen, step.array, step.highlights, step.actions, bar_width, gap_len)
    draw_buttons(buttons)
    draw_controls_box(screen, controls_box, controls_box_texts)
    draw_sort_info_box(screen, sort_info_box, chosen_sort_btn, step.stats, font_sml)
    pygame.display.flip()
    
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                array, sort = reset_sort(screen, chosen_sort, arr_len)
            elif event.key == pygame.K_l:
                if game_speed > 0:
                    game_speed -= 25
            elif event.key == pygame.K_k:
                game_speed += 25
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_s:
                new_step = next(sort, None)
                if new_step is not None:
                    step = new_step
                draw_array(screen, step.array, step.highlights, step.actions, bar_width, gap_len)
            elif event.key == pygame.K_m:
                muted = mute_button_pressed(btn_mute)

            elif event.key == pygame.K_1:
                chosen_sort = "selection"
                array, sort, step = reset_sort(screen, chosen_sort, arr_len)
            elif event.key == pygame.K_2:
                chosen_sort = "bubble"
                array, sort, step = reset_sort(screen, chosen_sort, arr_len)
            elif event.key == pygame.K_3:
                chosen_sort = "insertion"
                array, sort, step = reset_sort(screen, chosen_sort, arr_len)

        elif btn_reset.event(event):
            btn_reset.active = True
            array, sort, step = reset_sort(screen, chosen_sort, arr_len)
            btn_reset.active = False
        elif btn_mute.event(event):
            muted = mute_button_pressed(btn_mute)

        elif btn_selection_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_selection_sort
            chosen_sort_btn.active = True
            chosen_sort = "selection"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len)
        elif btn_bubble_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_bubble_sort
            chosen_sort_btn.active = True
            chosen_sort = "bubble"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len)
        elif btn_insertion_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_insertion_sort
            chosen_sort_btn.active = True
            chosen_sort = "insertion"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len)
        elif btn_shell_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_shell_sort
            chosen_sort_btn.active = True
            chosen_sort = "shell"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len)
        



    

pygame.quit()
sys.exit()