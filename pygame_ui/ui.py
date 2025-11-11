import pygame
from core.game import Game

# --- Constants ---
# General
WIDTH, HEIGHT = 1280, 800  # Increased width for bear-off area

# Colors
BACKGROUND_COLOR = (210, 180, 140)
FONT_COLOR = (0, 0, 0)
INPUT_BOX_COLOR = (255, 255, 255)
INPUT_BOX_ACTIVE_COLOR = (200, 200, 200)
BUTTON_COLOR = (139, 69, 19)
BUTTON_TEXT_COLOR = (255, 255, 255)
BOARD_COLOR = (245, 222, 179)
POINT_BLACK = (0, 0, 0)
POINT_RED = (255, 0, 0)
CHECKER_WHITE = (255, 255, 255)
CHECKER_BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
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

# Elementos interactivos
roll_dice_button = pygame.Rect(50, 450, 200, 50)
input_box1 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 50)
input_box2 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)


# --- Coordinate Calculation Helpers ---


def _get_visual_column(point_index):
    """
    Convierte un índice de punto del tablero (0–23) en un índice de columna visual (0–11).

    Args:
        point_index (int): Índice del punto lógico del tablero.

    Returns:
        int: Índice de columna visual correspondiente.
    """
    if 0 <= point_index <= 5:
        return 11 - point_index
    if 6 <= point_index <= 11:
        return 5 - (point_index - 6)
    if 12 <= point_index <= 17:
        return point_index - 12
    if 18 <= point_index <= 23:
        return (point_index - 18) + 6
    return -1


def _get_column_x_coord(column_index):
    """
    Calcula la coordenada X central de una columna visual del tablero.

    Args:
        column_index (int): Índice de columna visual (0–11).

    Returns:
        float: Coordenada X central en píxeles.
    """
    offset = BAR_WIDTH if column_index >= 6 else 0
    return BOARD_X + MARGIN + (column_index * POINT_WIDTH) + (POINT_WIDTH / 2) + offset


def get_point_center(point_index):
    """
    Devuelve las coordenadas centrales del primer checker en un punto del tablero.

    Args:
        point_index (int): Índice del punto (0–23).

    Returns:
        tuple: Coordenadas (x, y) del centro del punto.
    """
    col = _get_visual_column(point_index)
    x = _get_column_x_coord(col)
    y = (
        MARGIN + CHECKER_RADIUS
        if 12 <= point_index <= 23
        else HEIGHT - MARGIN - CHECKER_RADIUS
    )
    return int(x), int(y)


def get_point_rect(point_index):
    """
    Devuelve el rectángulo interactivo correspondiente a un punto del tablero.

    Args:
        point_index (int): Índice del punto (0–23).

    Returns:
        pygame.Rect: Rectángulo que representa el área clickeable del punto.
    """
    col = _get_visual_column(point_index)
    x_base = _get_column_x_coord(col) - (POINT_WIDTH / 2)
    height = HEIGHT * 0.4
    y = MARGIN if point_index >= 12 else HEIGHT - MARGIN - height
    return pygame.Rect(x_base, y, POINT_WIDTH, height)


def get_point_from_pos(pos):
    """
    Convierte una posición del mouse en un índice de punto del tablero.

    Args:
        pos (tuple): Coordenadas (x, y) del mouse.

    Returns:
        int or str or None: Índice del punto (0–23), "bar", "off" o None si no coincide.
    """
    for i in range(24):
        if get_point_rect(i).collidepoint(pos):
            return i
    if BEAR_OFF_X < pos[0] < WIDTH:
        return "off"
    bar_x_start = BOARD_X + MARGIN + 6 * POINT_WIDTH
    if bar_x_start < pos[0] < bar_x_start + BAR_WIDTH:
        return "bar"
    return None


def draw_text(screen, text, font, color, x, y, center=True):
    """
    Dibuja un texto en pantalla con la fuente y color indicados.

    Args:
        screen: Superficie de Pygame donde se dibuja.
        text (str): Texto a mostrar.
        font: Fuente utilizada.
        color (tuple): Color RGB del texto.
        x (int): Coordenada horizontal.
        y (int): Coordenada vertical.
        center (bool): Si True, centra el texto en (x, y); si False, lo alinea arriba a la izquierda.
    """
    text_surface = font.render(text, True, color)
    text_rect = (
        text_surface.get_rect(center=(x, y))
        if center
        else text_surface.get_rect(topleft=(x, y))
    )
    screen.blit(text_surface, text_rect)


def draw_board(screen):
    """
    Dibuja el tablero de juego, incluyendo los triangulos de puntos, barra y zona de borneado.

    Args:
        screen: Superficie de Pygame donde se dibuja.
    """
    BOARD_WIDTH = WIDTH - PANEL_WIDTH - BEAR_OFF_WIDTH
    POINT_HEIGHT = HEIGHT * 0.4
    pygame.draw.rect(screen, BOARD_COLOR, (BOARD_X, 0, BOARD_WIDTH, HEIGHT))

    for i in range(12):
        x_base = _get_column_x_coord(i) - (POINT_WIDTH / 2)
        point_1_index = 12 + i if i < 6 else 18 + (i - 6)
        color_top = POINT_RED if point_1_index % 2 != 0 else POINT_BLACK
        pygame.draw.polygon(
            screen,
            color_top,
            [
                (x_base, MARGIN),
                (x_base + POINT_WIDTH, MARGIN),
                (x_base + POINT_WIDTH / 2, MARGIN + POINT_HEIGHT),
            ],
        )
        point_2_index = 11 - i if i < 6 else 5 - (i - 6)
        color_bottom = POINT_RED if point_2_index % 2 != 0 else POINT_BLACK
        pygame.draw.polygon(
            screen,
            color_bottom,
            [
                (x_base, HEIGHT - MARGIN),
                (x_base + POINT_WIDTH, HEIGHT - MARGIN),
                (x_base + POINT_WIDTH / 2, HEIGHT - MARGIN - POINT_HEIGHT),
            ],
        )

    pygame.draw.rect(
        screen, PANEL_COLOR, (BOARD_X + MARGIN + 6 * POINT_WIDTH, 0, BAR_WIDTH, HEIGHT)
    )
    pygame.draw.rect(screen, PANEL_COLOR, (BEAR_OFF_X, 0, BEAR_OFF_WIDTH, HEIGHT))
    pygame.draw.line(
        screen, FONT_COLOR, (BEAR_OFF_X, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2
    )
    draw_text(
        screen,
        "Fichas Blancas",
        pygame.font.Font(None, 24),
        FONT_COLOR,
        BEAR_OFF_X + BEAR_OFF_WIDTH / 2,
        10,
    )
    draw_text


def draw_checkers(screen, font, game):
    """
    Dibuja todas las fichas en el tablero, barra y zona de borneado.

    Args:
        screen: Superficie de Pygame donde se dibuja.
        font: Fuente utilizada para mostrar cantidades.
        game (Game): Instancia actual del juego.
    """
    if not game:
        return
    for point_index, point in enumerate(game.board._puntos_):
        if point:
            color = CHECKER_WHITE if point[-1]._color_ == "blanco" else CHECKER_BLACK
            x, y_base = get_point_center(point_index)
            for i, _ in enumerate(point):
                y_offset = i * (CHECKER_RADIUS * 1.8)
                y = y_base + y_offset if 12 <= point_index <= 23 else y_base - y_offset
                if abs(y - y_base) > (HEIGHT / 2 - MARGIN - (2.5 * CHECKER_RADIUS)):
                    draw_text(screen, f"+{len(point) - i}", font, (255, 0, 0), x, y)
                    break
                pygame.draw.circle(screen, color, (x, int(y)), CHECKER_RADIUS)
                pygame.draw.circle(
                    screen, (128, 128, 128), (x, int(y)), CHECKER_RADIUS, 2
                )

    for i, checker in enumerate(game.fichas_borneadas("blanco")):
        pygame.draw.circle(
            screen,
            CHECKER_WHITE,
            (
                BEAR_OFF_X + CHECKER_RADIUS + 10,
                HEIGHT / 2 - MARGIN - i * CHECKER_RADIUS,
            ),
            CHECKER_RADIUS,
        )
    for i, checker in enumerate(game.fichas_borneadas("negro")):
        pygame.draw.circle(
            screen,
            CHECKER_BLACK,
            (
                BEAR_OFF_X + CHECKER_RADIUS + 10,
                HEIGHT / 2 + MARGIN + i * CHECKER_RADIUS,
            ),
            CHECKER_RADIUS,
        )

    bar_x = BOARD_X + MARGIN + 6 * POINT_WIDTH + (BAR_WIDTH / 2)
    for i, checker in enumerate(game.fichas_en_barra("blanco")):
        pygame.draw.circle(
            screen,
            CHECKER_WHITE,
            (bar_x, HEIGHT / 2 - MARGIN - i * CHECKER_RADIUS),
            CHECKER_RADIUS,
        )
    for i, checker in enumerate(game.fichas_en_barra("negro")):
        pygame.draw.circle(
            screen,
            CHECKER_BLACK,
            (bar_x, HEIGHT / 2 + MARGIN + i * CHECKER_RADIUS),
            CHECKER_RADIUS,
        )


def draw_highlights(screen, moves, color):
    """
    Dibuja resaltado en los destinos posibles para una ficha seleccionada.

    Args:
        screen: Superficie de Pygame donde se dibuja.
        moves (list): Lista de destinos validos.
        color (str): Color del jugador actual.
    """
    for move in moves:
        if move == "off":
            rect = pygame.Rect(
                BEAR_OFF_X,
                0 if color == "blanco" else HEIGHT / 2,
                BEAR_OFF_WIDTH,
                HEIGHT / 2,
            )
        else:
            rect = get_point_rect(move)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill(HIGHLIGHT_COLOR)
        screen.blit(s, rect.topleft)


def draw_side_panel(screen, font, game):
    """
    Dibuja el panel lateral con informacion de jugadores y turno actual.

    Args:
        screen: Superficie de Pygame donde se dibuja.
        font: Fuente utilizada para los textos.
        game (Game): Instancia actual del juego.
    """
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, PANEL_WIDTH, HEIGHT))
    draw_text(screen, "Backgammon", font, FONT_COLOR, PANEL_WIDTH // 2, 50)
    if game:
        p1, p2, current = game.jugador1, game.jugador2, game.jugador_actual()
        draw_text(
            screen, f"Blancas: {p1.nombre}", font, FONT_COLOR, PANEL_WIDTH // 2, 150
        )
        draw_text(
            screen, f"Negras: {p2.nombre}", font, FONT_COLOR, PANEL_WIDTH // 2, 200
        )
        draw_text(screen, "Turno:", font, FONT_COLOR, PANEL_WIDTH // 2, 300)
        draw_text(screen, current.nombre, font, (255, 0, 0), PANEL_WIDTH // 2, 350)


def draw_dice_and_moves(screen, font, game):
    """
    Muestra los valores de los dados y los movimientos disponibles.

    Args:
        screen: Superficie de Pygame donde se dibuja.
        font: Fuente utilizada para los textos.
        game (Game): Instancia actual del juego.
    """
    if not game:
        return
    if game.last_roll:
        draw_text(screen, "Dados:", font, FONT_COLOR, 150, 550)
        draw_text(
            screen,
            f"{game.last_roll[0]} y {game.last_roll[1]}",
            font,
            (0, 0, 255),
            150,
            600,
        )
    if game.available_moves:
        draw_text(screen, "Movimientos:", font, FONT_COLOR, 150, 650)
        draw_text(screen, str(game.available_moves), font, (0, 0, 255), 150, 700)


def handle_event(
    event,
    game,
    game_state,
    dice_rolled,
    selected_point,
    possible_moves,
    player1_name,
    player2_name,
    active_box,
    invalid_move_message,
    no_moves_message,
):
    """
    Maneja un evento de Pygame y actualiza el estado del juego segun la accion del usuario.

    Esta funcion controla tanto la pantalla de inicio como la logica de seleccion y movimiento
    de fichas durante la partida.

    Args:
        event: Evento capturado por Pygame.
        game (Game): Instancia actual del juego.
        game_state (str): Estado actual del juego ("start_screen" o "game_screen").
        dice_rolled (bool): Indica si los dados ya fueron tirados en el turno actual.
        selected_point (int or str): Punto seleccionado por el jugador.
        possible_moves (list): Lista de destinos validos para la ficha seleccionada.
        player1_name (str): Nombre del jugador 1.
        player2_name (str): Nombre del jugador 2.
        active_box: Caja de texto activa en pantalla de inicio.

    Returns:
        tuple: Estado actualizado del juego y variables de interfaz.
    """
    no_moves_timer = 0

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
            if event.key == pygame.K_BACKSPACE:
                name_ptr = name_ptr[:-1]
            else:
                name_ptr += event.unicode
            if active_box == input_box1:
                player1_name = name_ptr
            else:
                player2_name = name_ptr

    elif game_state == GAME_SCREEN:
        color = game.jugador_actual().color
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if roll_dice_button.collidepoint(pos) and not dice_rolled:
                game.tirar_dados()
                dice_rolled = True
                if not game.hay_movimientos_posibles(color):
                    no_moves_message = "No tienes movimientos posibles. Se cede el turno."
                    no_moves_timer = pygame.time.get_ticks()
            elif dice_rolled:
                clicked_dest = get_point_from_pos(pos)
                if selected_point is not None and clicked_dest in possible_moves:
                    if game.mover_ficha(selected_point, clicked_dest, color):
                        selected_point, possible_moves = None, []
                        if not game.available_moves:
                            game.cambiar_turno()
                            dice_rolled = False
                    else:
                        invalid_move_message = "Movimiento invalido"
                        invalid_move_timer = pygame.time.get_ticks()
                elif clicked_dest is not None:
                    if game.jugador_actual().puede_sacar_fichas(
                        game.board
                    ) and game.puede_mover(clicked_dest, "off", color):
                        if game.mover_ficha(clicked_dest, "off", color):
                            if not game.available_moves:
                                game.cambiar_turno()
                                dice_rolled = False
                        else:
                            invalid_move_message = "Movimiento invalido"
                            invalid_move_timer = pygame.time.get_ticks()
                    elif clicked_dest == "bar" or (
                        clicked_dest != "off"
                        and game.board._puntos_[clicked_dest]
                        and game.board._puntos_[clicked_dest][-1]._color_ == color
                    ):
                        
                        temp_possible_moves = []
                        for move in set(game.available_moves):
                            if color == "blanco":
                                dest = (
                                    24 - move
                                    if clicked_dest == "bar"
                                    else clicked_dest - move
                                )
                            else:
                                dest = (
                                    move - 1
                                    if clicked_dest == "bar"
                                    else clicked_dest + move
                                )
                            if game.puede_mover(clicked_dest, dest, color):
                                temp_possible_moves.append(dest)

                        if not temp_possible_moves:
                            invalid_move_message = "Esta ficha no tiene movimientos posibles"
                            invalid_move_timer = pygame.time.get_ticks()
                            selected_point, possible_moves = None, []
                        else:
                            selected_point = clicked_dest
                            possible_moves = temp_possible_moves
                    else:
                        selected_point, possible_moves = None, []
                        invalid_move_message = ""

    return (
        game,
        game_state,
        dice_rolled,
        selected_point,
        possible_moves,
        player1_name,
        player2_name,
        active_box,
        invalid_move_message,
        no_moves_message,
        no_moves_timer,
    )


def ejecutar_pygame():
    """
    Ejecuta el ciclo principal del juego Backgammon usando Pygame.

    Esta funcion inicializa la ventana, fuentes, estados y variables del juego.
    Controla la transicion entre la pantalla de inicio y la partida,
    gestiona eventos del usuario y actualiza la interfaz grafica en cada frame.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backgammon")
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 60)

    game_state = START_SCREEN
    game = None

    player1_name, player2_name = "Jugador 1", "Jugador 2"
    active_box = None

    dice_rolled, selected_point, possible_moves = False, None, []

    invalid_move_message = ""
    no_moves_message = ""
    no_moves_timer = 0

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            else:
                (
                    game,
                    game_state,
                    dice_rolled,
                    selected_point,
                    possible_moves,
                    player1_name,
                    player2_name,
                    active_box,
                    invalid_move_message,
                    no_moves_message,
                    no_moves_timer,
                ) = handle_event(
                    event,
                    game,
                    game_state,
                    dice_rolled,
                    selected_point,
                    possible_moves,
                    player1_name,
                    player2_name,
                    active_box,
                    invalid_move_message,
                    no_moves_message,
                )

        screen.fill(BACKGROUND_COLOR)

        if no_moves_message:
            if pygame.time.get_ticks() - no_moves_timer > 3000:
                no_moves_message = ""
                game.cambiar_turno()
                dice_rolled = False
            else:
                draw_text(
                    screen,
                    no_moves_message,
                    font,
                    (255, 0, 0),
                    WIDTH // 2,
                    HEIGHT // 2,
                )

        if game_state == START_SCREEN:
            draw_text(
                screen, "Backgammon", title_font, FONT_COLOR, WIDTH // 2, HEIGHT // 4
            )
            pygame.draw.rect(
                screen,
                INPUT_BOX_ACTIVE_COLOR if active_box == input_box1 else INPUT_BOX_COLOR,
                input_box1,
            )
            draw_text(
                screen,
                player1_name,
                font,
                FONT_COLOR,
                input_box1.centerx,
                input_box1.centery,
            )
            pygame.draw.rect(
                screen,
                INPUT_BOX_ACTIVE_COLOR if active_box == input_box2 else INPUT_BOX_COLOR,
                input_box2,
            )
            draw_text(
                screen,
                player2_name,
                font,
                FONT_COLOR,
                input_box2.centerx,
                input_box2.centery,
            )
            pygame.draw.rect(screen, BUTTON_COLOR, start_button)
            draw_text(
                screen,
                "Iniciar Juego",
                font,
                BUTTON_TEXT_COLOR,
                start_button.centerx,
                start_button.centery,
            )

        elif game_state == GAME_SCREEN:
            draw_side_panel(screen, font, game)
            draw_board(screen)
            if possible_moves:
                draw_highlights(screen, possible_moves, game.jugador_actual().color)
            draw_checkers(screen, font, game)
            if not dice_rolled:
                pygame.draw.rect(screen, BUTTON_COLOR, roll_dice_button)
                draw_text(
                    screen,
                    "Tirar Dados",
                    font,
                    BUTTON_TEXT_COLOR,
                    roll_dice_button.centerx,
                    roll_dice_button.centery,
                )
            else:
                draw_dice_and_moves(screen, font, game)

        if invalid_move_message:
            draw_text(
                screen,
                invalid_move_message,
                    font,
                    (255, 0, 0),
                    PANEL_WIDTH // 2,
                    750,
                )

        pygame.display.flip()

    pygame.quit()
