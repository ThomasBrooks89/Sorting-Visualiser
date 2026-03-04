import pygame
import sys
import sorting_logic
import drawing
import pygame_gui

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
                      (font_sml, "A/D: Array size -/+"),
                      (font_sml, "Q/E: Change shuffle type"),
                      (font_sml, "S: Step forwards"),
                      (font_sml, "M: Mute sounds"),
                      (font_sml, "Esc: Quit")]

# 'sort info' box setup
sort_info_box = pygame.Rect((btn_selection_sort.rect.x, 670, (pygame_gui.Button.width * 2) + 20, 390))

# 'config' box setup
config_box = pygame.Rect((btn_quicksort.rect.x, 865, (pygame_gui.Button.width * 2) + 20, 195))

# 'sort_explanation' box setup
sort_explanation_box = pygame.Rect((btn_insertion_sort.rect.x, 670, (pygame_gui.Button.width * 3) + 40, 390))


def reset_sort(surface, chosen_sort, arr_len, shuffle_type):
    array = sorting_logic.generate_array(1, arr_len, shuffle_type)
    sort = sorts[chosen_sort](array)
    step = next(sort)
    drawing.draw_array(surface, step.array, step.highlights, step.actions, bar_width, gap_len)
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
bar_width, leftover_bar_pixels = drawing.find_bar_widths(arr_len, gap_len, WIDTH)
chosen_sort = "selection"
sorts = {"selection": sorting_logic.selection_sort,
         "bubble": sorting_logic.bubble_sort,
         "insertion": sorting_logic.insertion_sort,
         "shell": sorting_logic.shell_sort}
shuffle_next = {"Random":"Reversed", "Reversed":"Almost Sorted", "Almost Sorted":"Random"}
shuffle_prev = {"Random":"Almost Sorted", "Reversed":"Random", "Almost Sorted":"Reversed"}
shuffle_type = "Random"
array = sorting_logic.generate_array(1, arr_len, shuffle_type)
sort = sorts[chosen_sort](array)
step = next(sort, None)


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
                next_iteration -= ((game_speed + 10) * 8)

    drawing.draw_array(screen, step.array, step.highlights, step.actions, bar_width, gap_len)
    drawing.draw_buttons(buttons)
    drawing.draw_controls_box(screen, controls_box, controls_box_texts)
    drawing.draw_sort_info_box(screen, sort_info_box, chosen_sort_btn, step.stats, font_sml)
    drawing.draw_config_box(screen, config_box, arr_len, game_speed, shuffle_type, font_sml)
    drawing.draw_sort_explanation_box(screen, sort_explanation_box)
    pygame.display.flip()
    
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            elif event.key == pygame.K_l:
                if game_speed > 0:
                    game_speed -= 25
            elif event.key == pygame.K_k:
                if game_speed < 100:
                     game_speed += 25
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_s:
                new_step = next(sort, None)
                if new_step is not None:
                    step = new_step
                drawing.draw_array(screen, step.array, step.highlights, step.actions, bar_width, gap_len)
            elif event.key == pygame.K_m:
                muted = mute_button_pressed(btn_mute)
            elif event.key == pygame.K_a:
                if arr_len > 50:
                    arr_len -= 50
                    bar_width, leftover_bar_pixels = drawing.find_bar_widths(arr_len, gap_len, WIDTH)
                    array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            elif event.key == pygame.K_d:
                if arr_len < 650:
                    arr_len += 50
                    bar_width, leftover_bar_pixels = drawing.find_bar_widths(arr_len, gap_len, WIDTH)
                    array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            elif event.key == pygame.K_q:
                shuffle_type = shuffle_prev[shuffle_type]
                array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            elif event.key == pygame.K_e:
                shuffle_type = shuffle_next[shuffle_type]
                array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)

            elif event.key == pygame.K_1:
                chosen_sort = "selection"
                array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            elif event.key == pygame.K_2:
                chosen_sort = "bubble"
                array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            elif event.key == pygame.K_3:
                chosen_sort = "insertion"
                array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)

        elif btn_reset.event(event):
            btn_reset.active = True
            array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
            btn_reset.active = False
        elif btn_mute.event(event):
            muted = mute_button_pressed(btn_mute)

        elif btn_selection_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_selection_sort
            chosen_sort_btn.active = True
            chosen_sort = "selection"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
        elif btn_bubble_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_bubble_sort
            chosen_sort_btn.active = True
            chosen_sort = "bubble"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
        elif btn_insertion_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_insertion_sort
            chosen_sort_btn.active = True
            chosen_sort = "insertion"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
        elif btn_shell_sort.event(event):
            chosen_sort_btn.active = False
            chosen_sort_btn = btn_shell_sort
            chosen_sort_btn.active = True
            chosen_sort = "shell"
            array, sort, step = reset_sort(screen, chosen_sort, arr_len, shuffle_type)
        


pygame.quit()
sys.exit()