import pygame
import numpy as np
from minimax import State
import logging
import time

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(levelname)s - %(message)s',  # Log format
                    handlers=[logging.StreamHandler()])  # Output logs to console

# pygame screen's object
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 370
SQUARE_SIZE = int(SCREEN_WIDTH / 3)
GAME_REGION = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_WIDTH)
PLAYER_FIRST_BUTTON = pygame.Rect(
    0, SCREEN_WIDTH, SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_WIDTH)
MACHINE_FIRST_BUTTON = pygame.Rect(
    SCREEN_WIDTH / 2, SCREEN_WIDTH, SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_WIDTH)

# Color
GAME_REGION_C = (255, 255, 255)

# State variable
machine_turn = False
game_finished = False
game_started = False
has_winner = False
finished_line_drawn = False
current_state = State('X', 'O')  # The args are just temporary placeholder
human_first = False
machine_first = False

def draw_game_space(screen):
    global current_state, finished_line_drawn, game_started, has_winner, game_finished
    font = pygame.font.Font(None, 90)
    pygame.draw.rect(screen, GAME_REGION_C, GAME_REGION)
    for row in range(3):
        for col in range(3):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            # This draw the border, we dont draw the actual square
            pygame.draw.rect(screen, (0, 0, 0),
                             (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)
            # Draw the text icon
            if current_state.matrix[row, col] != ' ':
                text = font.render(
                    str(current_state.matrix[row, col]), True, (0, 0, 9))
                text_rect = text.get_rect(
                    center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw the finished line if game has win terminal state
    if game_finished and has_winner and not game_started:
        draw_winning_line(screen)

# Check if the current state is terminal, if terminal reset the game
def check_terminal():
    global game_finished, has_winner, game_started
    # If the current state is terminal, end
    if current_state.is_draw():
        logging.info("WE HAVE A DRAW!!!")
        game_finished = True
        game_started = False

    if current_state.is_win():
        if current_state.just_played == 'O':  # The player
            has_winner = True
            logging.info("YOU WIN!!!")

        if current_state.just_played == 'X':  # The machine
            has_winner = True
            logging.info("MACHINE WIN!!!")

        game_finished = True
        game_started = False

def machine_play():
    global current_state, machine_turn
    logging.info("--> Machine turn")
    logging.info("Machine is thinking...")
    time.sleep(1)

    # We guarantee the current_state is not terminal already
    children_state = current_state.get_children()
    smallest_child = children_state[0]
    smallest_score = smallest_child.minimax()
    for child in children_state[1:]:
        if child.minimax() < smallest_score:
            smallest_child = child
            smallest_score = child.minimax()

    # ============ Logging ===========
    logging.info("Current state is:\n%s", current_state.matrix)
    logging.info("Children:")
    for child in children_state:
        logging.info("Child state:\n%s", child.matrix)
        logging.info("Minimax: %s", child.minimax())
    logging.info("Machine choose:\n%s", smallest_child.matrix)

    # Update the current state to that child state
    current_state = smallest_child
    machine_turn = False

def handle_play_click(pos):
    global game_finished, machine_turn, current_state
    # If this is human turn to play
    if not game_finished and not machine_turn:
        if pos[0] < SQUARE_SIZE * 3 and pos[1] < SQUARE_SIZE * 3:
            col_clicked = pos[0] // SQUARE_SIZE
            row_clicked = pos[1] // SQUARE_SIZE
            if current_state.matrix[row_clicked, col_clicked] == ' ':
                logging.info("--> Human turn")
                next_to_play = current_state.next_to_play
                just_played = current_state.just_played
                current_state.matrix[row_clicked,
                                     col_clicked] = next_to_play
                current_state.just_played = next_to_play
                current_state.next_to_play = just_played

                logging.info(
                    f'Mouse clicked on ({row_clicked}, {col_clicked})')
                machine_turn = True

def find_winning_line():
    # Row
    for i in range(3):
        if current_state.matrix[i, 0] == current_state.matrix[i, 1] == current_state.matrix[i, 2] == current_state.just_played:
            return [(i, 0), (i, 2)]
    # Col
    for i in range(3):
        if current_state.matrix[0, i] == current_state.matrix[1, i] == current_state.matrix[2, i] == current_state.just_played:
            return [(0, i), (2, i)]
    # Dia
    if current_state.matrix[0, 0] == current_state.matrix[1, 1] == current_state.matrix[2, 2] == current_state.just_played:
        return [(0, 0), (2, 2)]
    if current_state.matrix[2, 0] == current_state.matrix[1, 1] == current_state.matrix[0, 2] == current_state.just_played:
        return [(2, 0), (0, 2)]

def draw_winning_line(screen):
    start, end = find_winning_line()
    # Convert grid coordinates to pixel coordinates
    start_pos = (start[1] * SQUARE_SIZE + SQUARE_SIZE // 2,
                 start[0] * SQUARE_SIZE + SQUARE_SIZE // 2)
    end_pos = (end[1] * SQUARE_SIZE + SQUARE_SIZE // 2,
               end[0] * SQUARE_SIZE + SQUARE_SIZE // 2)

    # Draw a line (color: red, thickness: 10)
    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 10)

def draw_button(screen):
    global game_started, game_finished, human_first, machine_first
    normal_c = (255, 255, 23)
    faded_c = (165, 165, 165)
    pressed_c = (9, 255, 0)

    if game_started and not game_finished and human_first:
        human_button_c = pressed_c
        machine_button_c = faded_c
    elif game_started and not game_finished and machine_first:
        human_button_c = faded_c
        machine_button_c = pressed_c
    else:
        human_button_c = normal_c
        machine_button_c = normal_c

    # Player button
    pygame.draw.rect(screen, human_button_c, PLAYER_FIRST_BUTTON)
    pygame.draw.rect(screen, (0, 0, 0), PLAYER_FIRST_BUTTON, 2)
    draw_multiline_text(screen, 'PLAYER\nFIRST', PLAYER_FIRST_BUTTON.center)

    pygame.draw.rect(screen, machine_button_c, MACHINE_FIRST_BUTTON)
    pygame.draw.rect(screen, (0, 0, 0), MACHINE_FIRST_BUTTON, 2)
    draw_multiline_text(screen, 'MACHINE\nFIRST', MACHINE_FIRST_BUTTON.center)

# CHATGPT CODE
def draw_multiline_text(screen, text, center):
    lines = text.split('\n')
    font = pygame.font.Font(None, 35)  # Adjust the font size as needed
    total_height = len(lines) * font.get_height()

    # Calculate the starting Y position
    start_y = center[1] - total_height // 2 + 10

    for i, line in enumerate(lines):
        rendered_line = font.render(line, True, (0, 0, 9))
        text_rect = rendered_line.get_rect(
            center=(center[0], start_y + i * font.get_height()))
        screen.blit(rendered_line, text_rect)

# main loop
def run_game():
    global running, current_state, machine_turn, human_first, machine_first, game_finished, game_started
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        # Check if the current state is terminal
        if not game_finished:
            check_terminal()

        # Check mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game exit...")
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Clicked on a square
                pos = pygame.mouse.get_pos()

                if game_started:
                    handle_play_click(pos)

                if PLAYER_FIRST_BUTTON.collidepoint(pos) and not game_started:
                    human_first = True
                    game_started = True
                    game_finished = False
                    current_state = State('X', 'O')
                    machine_turn = False

                if MACHINE_FIRST_BUTTON.collidepoint(pos) and not game_started:
                    machine_first = True
                    game_started = True
                    game_finished = False
                    current_state = State('O', 'X')
                    machine_turn = True

        # Do something
        draw_game_space(screen)
        draw_button(screen)

        # Update
        pygame.display.flip()
        clock.tick(120)

        # Check if the current state is terminal again since human just played
        if not game_finished:
            check_terminal()

        # If this is machine turn
        if machine_turn and game_started and not game_finished:
            machine_play()

    pygame.quit()
