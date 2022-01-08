import pygame, random

from assets.Cell import Cell
from assets.Game_window import Game_window
from assets.Button import Button

HEIGHT, WIDTH = 800, 800
BACKGROUND = (220,220,220)
FPS = 30

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()
game_window = Game_window(screen, 100, 150)
state = 'setting'

buttons = []
button_args = {
    "dimension": (100, 30),
    "color": (156, 156, 156),
    "surface": screen
}

run_button = Button(pos = (125, 50), text = "Run", **button_args)
reset_button = Button(pos = (425, 50), text = "Reset", **button_args)
pause_button = Button(pos = (275, 50), text = "Pause", **button_args)
exit_button = Button(pos = (575, 50), text = "Exit", **button_args)
rand_button = Button(pos = (125, 100), text = "Random", **button_args)
get_button = Button(pos = (275, 100), text = "Get Last", **button_args)
inf_button = Button(pos = (425, 100), text = "Infinite", hover = False, **button_args)
load_button = Button(pos = (575, 100), text = "Load", **button_args)

buttons.extend([
    run_button, pause_button, reset_button, exit_button, 
    rand_button, get_button, inf_button, load_button
])

def mouse_on_grid(pos):
    return 100 <= pos[0] <= 700 and 150 <= pos[1] <= 750


def click_cell(pos):
    x_pix, y_pix = pos
    x = (x_pix - 100) // 20
    y = (y_pix - 150) // 20
    
    cell_grid = game_window.grid
    cell_grid[x][y].alive = not cell_grid[x][y].alive


def get_events(mouse_pos):
    global running
    global state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_on_grid(event.pos):
                click_cell(event.pos)

            if run_button.mouse_over(mouse_pos) and state != 'running':
                if state != 'pause':
                    game_window.last_grid = game_window.grid
                state = 'running'

            if pause_button.mouse_over(mouse_pos) and state == 'running':
                state = 'pause'

            if reset_button.mouse_over(mouse_pos) and state != 'setting':
                game_window.grid = [[Cell((x, y), game_window.image) for y in range(game_window.cols)] for x in range(game_window.rows)]
                state = 'setting'

            if exit_button.mouse_over(mouse_pos):
                running = False

            if rand_button.mouse_over(mouse_pos):
                for row in game_window.grid:
                    for cell in row:
                        cell.alive = random.choice([True, False, False, False])

            if get_button.mouse_over(mouse_pos) and state == 'setting':
                game_window.grid = game_window.last_grid

            if inf_button.mouse_over(mouse_pos):
                game_window.infinite = not game_window.infinite

            if load_button.mouse_over(mouse_pos) and state == 'setting':
                print('Not implemented yet')


def update(state, mouse_pos):
    pygame.display.update()
    game_window.update()
    if state == 'running':
        game_window.next_gen()
    for button in buttons:
        button.update(mouse_pos)


def draw(state, mouse_pos):
    screen.fill(BACKGROUND)
    game_window.draw()
    for button in buttons:
        if button == inf_button:
            button.color = (125, 185, 86) if game_window.infinite else (185, 87, 87)
        button.draw(mouse_pos)


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    get_events(mouse_pos)
    update(state, mouse_pos)
    draw(state, mouse_pos)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()