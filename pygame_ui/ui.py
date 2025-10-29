import pygame
import sys
from core.game import Game

# --- Constants ---
# General
WIDTH, HEIGHT = 1280, 800 # Increased width for bear-off area
# Colors
BACKGROUND_COLOR = (210, 180, 140)
FONT_COLOR = (0, 0, 0)
INPUT_BOX_COLOR = (255, 255, 255)
INPUT_BOX_ACTIVE_COLOR = (200, 200, 200)
BUTTON_COLOR = (139, 69, 19)
BUTTON_TEXT_COLOR = (255, 255, 255)
# Board Colors
BOARD_COLOR = (245, 222, 179)
POINT_BLACK = (0, 0, 0)
POINT_RED = (255, 0, 0)
CHECKER_WHITE = (255, 255, 255)
CHECKER_BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
# Panel & Bear-off Area
PANEL_COLOR = (205, 170, 125)

# Game states
START_SCREEN = "start_screen"
GAME_SCREEN = "game_screen"

# --- UI Layout Constants ---
PANEL_WIDTH = 300
BOARD_X = PANEL_WIDTH
MARGIN = 20
BEAR_OFF_WIDTH = 80
POINT_WIDTH = (WIDTH - PANEL_WIDTH - BEAR_OFF_WIDTH - 2 * MARGIN) / 13
BAR_WIDTH = POINT_WIDTH
CHECKER_RADIUS = int(POINT_WIDTH / 2.5)
BEAR_OFF_X = WIDTH - BEAR_OFF_WIDTH

# --- Coordinate Calculation Helpers ---
def _get_visual_column(point_index):
    """Converts a point index (0-23) to a visual column (0-11)."""
    if 0 <= point_index <= 5: return 11 - point_index
    if 6 <= point_index <= 11: return 5 - (point_index - 6)
    if 12 <= point_index <= 17: return point_index - 12
    if 18 <= point_index <= 23: return (point_index - 18) + 6
    return -1

def _get_column_x_coord(column_index):
    """Gets the center x-coordinate for a visual column."""
    offset = BAR_WIDTH if column_index >= 6 else 0
    return BOARD_X + MARGIN + (column_index * POINT_WIDTH) + (POINT_WIDTH / 2) + offset

def get_point_center(point_index):
    """Gets the center coordinates for the first checker on a point."""
    col = _get_visual_column(point_index)
    x = _get_column_x_coord(col)
    y = MARGIN + CHECKER_RADIUS if 12 <= point_index <= 23 else HEIGHT - MARGIN - CHECKER_RADIUS
    return int(x), int(y)

def get_point_rect(point_index):
    """Gets the clickable rect for a point."""
    col = _get_visual_column(point_index)
    x_base = _get_column_x_coord(col) - (POINT_WIDTH / 2)
    height = HEIGHT * 0.4
    y = MARGIN if point_index >= 12 else HEIGHT - MARGIN - height
    return pygame.Rect(x_base, y, POINT_WIDTH, height)

def get_point_from_pos(pos):
    """Converts mouse coordinates to a board point index."""
    for i in range(24):
        if get_point_rect(i).collidepoint(pos):
            return i
    # Check bear-off area
    if BEAR_OFF_X < pos[0] < WIDTH:
        return "off"
        
    # Check bar area
    bar_x_start = BOARD_X + MARGIN + 6 * POINT_WIDTH
    if bar_x_start < pos[0] < bar_x_start + BAR_WIDTH:
        return "bar"
        
    return None

# --- UI Drawing Functions ---
def draw_text(screen, text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y)) if center else text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

def draw_board(screen):
    BOARD_WIDTH = WIDTH - PANEL_WIDTH - BEAR_OFF_WIDTH
    POINT_HEIGHT = HEIGHT * 0.4
    pygame.draw.rect(screen, BOARD_COLOR, (BOARD_X, 0, BOARD_WIDTH, HEIGHT))

    for i in range(12):
        x_base = _get_column_x_coord(i) - (POINT_WIDTH / 2)
        point_1_index = 12 + i if i < 6 else 18 + (i - 6)
        color_top = POINT_RED if point_1_index % 2 != 0 else POINT_BLACK
        pygame.draw.polygon(screen, color_top, [(x_base, MARGIN), (x_base + POINT_WIDTH, MARGIN), (x_base + POINT_WIDTH / 2, MARGIN + POINT_HEIGHT)])
        point_2_index = 11 - i if i < 6 else 5 - (i - 6)
        color_bottom = POINT_RED if point_2_index % 2 != 0 else POINT_BLACK
        pygame.draw.polygon(screen, color_bottom, [(x_base, HEIGHT - MARGIN), (x_base + POINT_WIDTH, HEIGHT - MARGIN), (x_base + POINT_WIDTH / 2, HEIGHT - MARGIN - POINT_HEIGHT)])

    pygame.draw.rect(screen, PANEL_COLOR, (BOARD_X + MARGIN + 6 * POINT_WIDTH, 0, BAR_WIDTH, HEIGHT))
    # Draw Bear-off areas
    pygame.draw.rect(screen, PANEL_COLOR, (BEAR_OFF_X, 0, BEAR_OFF_WIDTH, HEIGHT))
    pygame.draw.line(screen, FONT_COLOR, (BEAR_OFF_X, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
    draw_text(screen, "White Off", pygame.font.Font(None, 24), FONT_COLOR, BEAR_OFF_X + BEAR_OFF_WIDTH/2, 10)
    draw_text(screen, "Black Off", pygame.font.Font(None, 24), FONT_COLOR, BEAR_OFF_X + BEAR_OFF_WIDTH/2, HEIGHT - 20)


def draw_checkers(screen, font, game):
    # Draw checkers on board
    for point_index, point in enumerate(game.board._puntos_):
        if point:
            color = CHECKER_WHITE if point[-1]._color_ == "blanco" else CHECKER_BLACK
            x, y_base = get_point_center(point_index)
            for i, _ in enumerate(point):
                y_offset = i * (CHECKER_RADIUS * 1.8)
                y = y_base + y_offset if 12 <= point_index <= 23 else y_base - y_offset
                if abs(y - y_base) > (HEIGHT/2 - MARGIN - (2.5 * CHECKER_RADIUS)):
                    draw_text(screen, f"+{len(point) - i}", font, (255,0,0), x, y)
                    break
                pygame.draw.circle(screen, color, (x, int(y)), CHECKER_RADIUS)
                pygame.draw.circle(screen, (128,128,128), (x, int(y)), CHECKER_RADIUS, 2)
    # Draw borne-off checkers
    for i, checker in enumerate(game.fichas_borneadas("blanco")):
        pygame.draw.circle(screen, CHECKER_WHITE, (BEAR_OFF_X + CHECKER_RADIUS + 10, HEIGHT/2 - MARGIN - i * CHECKER_RADIUS), CHECKER_RADIUS)
    for i, checker in enumerate(game.fichas_borneadas("negro")):
        pygame.draw.circle(screen, CHECKER_BLACK, (BEAR_OFF_X + CHECKER_RADIUS + 10, HEIGHT/2 + MARGIN + i * CHECKER_RADIUS), CHECKER_RADIUS)

    # Draw checkers on the bar
    bar_x = BOARD_X + MARGIN + 6 * POINT_WIDTH + (BAR_WIDTH / 2)
    for i, checker in enumerate(game.fichas_en_barra("blanco")):
        pygame.draw.circle(screen, CHECKER_WHITE, (bar_x, HEIGHT/2 - MARGIN - i * CHECKER_RADIUS), CHECKER_RADIUS)
    for i, checker in enumerate(game.fichas_en_barra("negro")):
        pygame.draw.circle(screen, CHECKER_BLACK, (bar_x, HEIGHT/2 + MARGIN + i * CHECKER_RADIUS), CHECKER_RADIUS)


def draw_highlights(screen, moves, color):
    for move in moves:
        if move == "off":
            rect = pygame.Rect(BEAR_OFF_X, 0 if color == "blanco" else HEIGHT/2, BEAR_OFF_WIDTH, HEIGHT/2)
        else:
            rect = get_point_rect(move)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill(HIGHLIGHT_COLOR)
        screen.blit(s, rect.topleft)

def draw_side_panel(screen, font, game):
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, PANEL_WIDTH, HEIGHT))
    draw_text(screen, "Backgammon", font, FONT_COLOR, PANEL_WIDTH // 2, 50)
    if game:
        p1, p2, current = game.jugador1, game.jugador2, game.jugador_actual()
        draw_text(screen, f"White: {p1.nombre}", font, FONT_COLOR, PANEL_WIDTH // 2, 150)
        draw_text(screen, f"Black: {p2.nombre}", font, FONT_COLOR, PANEL_WIDTH // 2, 200)
        draw_text(screen, "Turn:", font, FONT_COLOR, PANEL_WIDTH // 2, 300)
        draw_text(screen, current.nombre, font, (255, 0, 0), PANEL_WIDTH // 2, 350)

def draw_dice_and_moves(screen, font, game):
    if game.last_roll:
        draw_text(screen, "Dice:", font, FONT_COLOR, 150, 550)
        draw_text(screen, f"{game.last_roll[0]} & {game.last_roll[1]}", font, (0,0,255), 150, 600)
    if game.available_moves:
        draw_text(screen, "Moves:", font, FONT_COLOR, 150, 650)
        draw_text(screen, str(game.available_moves), font, (0,0,255), 150, 700)

def ejecutar_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backgammon")
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 60)
    
    game_state = START_SCREEN
    game = None

    player1_name, player2_name = "Player 1", "Player 2"
    input_box1 = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 100, 300, 50)
    input_box2 = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 50)
    start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
    active_box = None

    roll_dice_button = pygame.Rect(50, 450, 200, 50)
    dice_rolled, selected_point, possible_moves = False, None, []
    
    invalid_move_message = ""
    invalid_move_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            if game_state == START_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos):
                        active_box = input_box1
                        player1_name = ""
                    elif input_box2.collidepoint(event.pos):
                        active_box = input_box2
                        player2_name = ""
                    elif start_button.collidepoint(event.pos):
                        game, game_state = Game(), GAME_SCREEN
                        game.jugador1.nombre, game.jugador2.nombre = player1_name, player2_name
                    else:
                        active_box = None
                if event.type == pygame.KEYDOWN and active_box:
                    name_ptr = player1_name if active_box == input_box1 else player2_name
                    if event.key == pygame.K_BACKSPACE: name_ptr = name_ptr[:-1]
                    else: name_ptr += event.unicode
                    if active_box == input_box1: player1_name = name_ptr
                    else: player2_name = name_ptr

            elif game_state == GAME_SCREEN:
                color = game.jugador_actual().color
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if roll_dice_button.collidepoint(pos) and not dice_rolled:
                        game.tirar_dados()
                        dice_rolled = True
                    elif dice_rolled:
                        clicked_dest = get_point_from_pos(pos)
                        if selected_point is not None and clicked_dest in possible_moves:
                            if game.mover_ficha(selected_point, clicked_dest, color):
                                selected_point, possible_moves = None, []
                                if not game.available_moves:
                                    game.cambiar_turno()
                                    dice_rolled = False
                            else:
                                invalid_move_message = "Invalid Move"
                                invalid_move_timer = pygame.time.get_ticks()
                        elif clicked_dest is not None:
                            # One-click bear-off
                            if game.jugador_actual().puede_sacar_fichas(game.board) and game.puede_mover(clicked_dest, "off", color):
                                if game.mover_.ficha(clicked_dest, "off", color):
                                    if not game.available_moves:
                                        game.cambiar_turno()
                                        dice_rolled = False
                                else:
                                    invalid_move_message = "Invalid Move"
                                    invalid_move_timer = pygame.time.get_ticks()
                            elif clicked_dest == "bar" or (clicked_dest != "off" and game.board._puntos_[clicked_dest] and game.board._puntos_[clicked_dest][-1]._color_ == color):
                                selected_point = clicked_dest
                                possible_moves = []
                                for move in set(game.available_moves):
                                    if color == "blanco":
                                        dest = 24 - move if selected_point == "bar" else selected_point - move
                                    else:
                                        dest = move - 1 if selected_point == "bar" else selected_point + move
                                    
                                    if game.puede_mover(selected_point, dest, color):
                                        possible_moves.append(dest)
                            else:
                                selected_point, possible_moves = None, []
        
        screen.fill(BACKGROUND_COLOR)
        if game_state == START_SCREEN:
            draw_text(screen, "Backgammon", title_font, FONT_COLOR, WIDTH//2, HEIGHT//4)
            pygame.draw.rect(screen, INPUT_BOX_ACTIVE_COLOR if active_box == input_box1 else INPUT_BOX_COLOR, input_box1)
            draw_text(screen, player1_name, font, FONT_COLOR, input_box1.centerx, input_box1.centery)
            pygame.draw.rect(screen, INPUT_BOX_ACTIVE_COLOR if active_box == input_box2 else INPUT_BOX_COLOR, input_box2)
            draw_text(screen, player2_name, font, FONT_COLOR, input_box2.centerx, input_box2.centery)
            pygame.draw.rect(screen, BUTTON_COLOR, start_button)
            draw_text(screen, "Start Game", font, BUTTON_TEXT_COLOR, start_button.centerx, start_button.centery)
        elif game_state == GAME_SCREEN:
            draw_side_panel(screen, font, game)
            draw_board(screen)
            if possible_moves: draw_highlights(screen, possible_moves, game.jugador_actual().color)
            draw_checkers(screen, font, game)
            if not dice_rolled:
                pygame.draw.rect(screen, BUTTON_COLOR, roll_dice_button)
                draw_text(screen, "Roll Dice", font, BUTTON_TEXT_COLOR, roll_dice_button.centerx, roll_dice_button.centery)
            else:
                draw_dice_and_moves(screen, font, game)
        
        if invalid_move_message:
            if pygame.time.get_ticks() - invalid_move_timer > 2000:
                invalid_move_message = ""
            else:
                draw_text(screen, invalid_move_message, font, (255, 0, 0), WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    ejecutar_pygame()
