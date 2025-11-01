# Promp Con los Dosctrings que ya Puse en el codigo ayudame a terminar de completar todos los que faltan (Hice esto con todos los codigos)

# pygame_ui.py

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
    invalid_move_message = ""
    invalid_move_timer = 0

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
                        selected_point = clicked_dest
                        possible_moves = []
                        for move in set(game.available_moves):
                            if color == "blanco":
                                dest = (
                                    24 - move
                                    if selected_point == "bar"
                                    else selected_point - move
                                )
                            else:
                                dest = (
                                    move - 1
                                    if selected_point == "bar"
                                    else selected_point + move
                                )
                            if game.puede_mover(selected_point, dest, color):
                                possible_moves.append(dest)
                    else:
                        selected_point, possible_moves = None, []

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
        invalid_move_timer,
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
    invalid_move_timer = 0

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
                    invalid_move_timer,
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
                )

        screen.fill(BACKGROUND_COLOR)

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
            if pygame.time.get_ticks() - invalid_move_timer > 2000:
                invalid_move_message = ""
            else:
                draw_text(
                    screen,
                    invalid_move_message,
                    font,
                    (255, 0, 0),
                    WIDTH // 2,
                    HEIGHT // 2,
                )

        pygame.display.flip()

    pygame.quit()

# Dados.py:

import random


class Dice:
    """
    Clase que representa los dados del juego.

    Permite tirar los dados, obtener sus valores, detectar si se tiró doble,
    y calcular los movimientos disponibles según el resultado.
    """

    def __init__(self):
        """
        Inicializa los valores de los dados en (0, 0).
        """
        self.__values__ = (0, 0)

    def roll_dice(self):
        """
        Genera dos valores aleatorios entre 1 y 6 simulando el tiro de dados.

        Returns:
            tuple: Una tupla con los dos valores obtenidos.
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.__values__ = (die1, die2)
        return self.__values__

    def get_values(self):
        """
        Devuelve los valores actuales de los dados.

        Returns:
            tuple: Los valores del último tiro.
        """
        return self.__values__

    def is_double(self):
        """
        Verifica si los dados tienen el mismo valor (doble).

        Returns:
            bool: True si es doble, False si no.
        """
        return self.__values__[0] == self.__values__[1]

    def get_moves(self):
        """
        Calcula los movimientos disponibles según los valores de los dados.

        Returns:
            list: Lista de movimientos disponibles.
        """
        d1, d2 = self.__values__
        return [d1] * 4 if self.is_double() else [d1, d2]

    def set_values_for_test(self, val1, val2):
        """
        Establece manualmente los valores de los dados (para pruebas).

        Args:
            val1 (int): Valor del primer dado.
            val2 (int): Valor del segundo dado.
        """
        if not (1 <= val1 <= 6 and 1 <= val2 <= 6):
            raise ValueError("Los valores deben estar entre 1 y 6")
        self.__values__ = (val1, val2)

# Board.py:

from core.checker import Checker


class Board:
    """
    Represents the Backgammon board, composed of 24 numbered points (0 to 23).
    Each point can hold a stack of checkers belonging to a player.

    Attributes:
        _puntos_ (list): A list of 24 slots, each containing a stack of checkers.
        historial_de_jugadas (list): A record of all moves made during the game.
        fichas (list): A list of all 30 checkers.
    """

    def __init__(self):
        """
        Initializes the board with 24 empty points and an empty move history.
        """
        self._puntos_ = [[] for _ in range(24)]
        self.historial_de_jugadas = []
        self.fichas = []

    def inicializar_fichas(self):
        """
        Places the initial checkers on the board according to standard setup.
        """
        self.fichas = []
        posiciones = {
            "negro": {23: 2, 12: 5, 7: 3, 5: 5},
            "blanco": {0: 2, 11: 5, 16: 3, 18: 5},
        }
        for color, puntos in posiciones.items():
            for punto, cantidad in puntos.items():
                for _ in range(cantidad):
                    checker = Checker(color, punto)
                    self._puntos_[punto].append(checker)
                    self.fichas.append(checker)

    def mover_ficha(self, origen, destino, color):
        """
        Moves a checker from the origin point to the destination, validating basic rules.

        Args:
            origen (int): Index of the origin point (0–23).
            destino (int): Index of the destination point (0–23).
            color (str): Color of the player making the move ("blanco" or "negro").

        Raises:
            ValueError: If the move is invalid due to range, color mismatch, or blocked destination.
        """
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise ValueError("Points must be between 0 and 23")

        punto_origen = self._puntos_[origen]
        punto_destino = self._puntos_[destino]

        if not punto_origen:
            raise ValueError(f"No checkers at point {origen}")

        ficha = punto_origen[-1]
        if ficha._color_ != color:
            raise ValueError(
                f"The checker at point {origen} does not match color {color}"
            )

        captura = False
        if (
            punto_destino
            and punto_destino[-1]._color_ != color
            and len(punto_destino) == 1
        ):
            punto_destino.pop()
            captura = True

        ficha._position_ = destino
        punto_origen.pop()
        punto_destino.append(ficha)

        self.registrar_jugada(color, origen, destino, captura)

    def eliminar_ficha_si_unica(self, punto, color):
        """
        Removes a checker from the point if it's the only one and matches the given color.

        Args:
            punto (int): Index of the point (0–23).
            color (str): Player color.

        Returns:
            Checker: The removed checker.

        Raises:
            ValueError: If the point is out of range or conditions are not met.
        """
        if not (0 <= punto < 24):
            raise ValueError("Point must be between 0 and 23")

        casilla = self._puntos_[punto]
        if len(casilla) == 1 and casilla[0]._color_ == color:
            ficha = casilla.pop()
            return ficha
        else:
            raise ValueError("Cannot remove checker: invalid conditions")

    def puede_entrar_desde_bar(self, color, entrada):
        """
        Checks if a checker can re-enter from the bar to the specified point.

        Args:
            color (str): Player color.
            entrada (int): Entry point (0–5 for blanco, 18–23 for negro).

        Returns:
            bool: True if entry is allowed, False if blocked.
        """
        punto = self._puntos_[entrada]
        return not punto or punto[-1]._color_ == color or len(punto) < 2

    def intentar_reingreso(self, color):
        """
        Attempts to re-enter a checker from the bar onto the board.

        Args:
            color (str): Player color.

        Returns:
            int or None: Entry point if successful, None if all are blocked.
        """
        entradas = range(0, 6) if color == "blanco" else range(18, 24)
        for entrada in entradas:
            if self.puede_entrar_desde_bar(color, entrada):
                self._puntos_[entrada].append(Checker(color, entrada))
                print(f"{color} re-enters at point {entrada}")
                return entrada
        print(f"{color} cannot re-enter: all points are blocked.")
        return None

    def registrar_jugada(self, jugador, origen, destino, captura=False):
        """
        Records a move in the game history.

        Args:
            jugador (str): Player color.
            origen (int): Origin point.
            destino (int): Destination point.
            captura (bool): Whether a capture occurred.
        """
        jugada = {
            "jugador": jugador,
            "origen": origen,
            "destino": destino,
            "captura": captura,
        }
        self.historial_de_jugadas.append(jugada)

    def mostrar_historial(self):
        """
        Prints the history of moves made during the game.
        """
        print("\nMove history:")
        for j in self.historial_de_jugadas:
            texto = f"{j['jugador']} moved from {j['origen']} to {j['destino']}"
            if j["captura"]:
                texto += " (capture)"
            print(texto)

    def mostrar_tablero(self):
        """
        Prints the current state of the board in a visual format.
        """
        print("\nWelcome to Backgammon Compucation 2025\n")

        print("TOP ZONE (13 → 24):")
        print(" ".join([f"{i:2}" for i in range(12, 24)]))
        print(
            " ".join(
                [
                    (
                        "".join(
                            [
                                "B" if f._color_ == "blanco" else "N"
                                for f in self._puntos_[i]
                            ]
                        )
                        if self._puntos_[i]
                        else "--"
                    )
                    for i in range(12, 24)
                ]
            )
        )

        print("\n" + "-" * 50 + "\n")

        print("BOTTOM ZONE (12 → 1):")
        print(" ".join([f"{i:2}" for i in reversed(range(12))]))
        print(
            " ".join(
                [
                    (
                        "".join(
                            [
                                "B" if f._color_ == "blanco" else "N"
                                for f in self._puntos_[i]
                            ]
                        )
                        if self._puntos_[i]
                        else "--"
                    )
                    for i in reversed(range(12))
                ]
            )
        )

# Checker.py:

class Checker:
    """
    Represents a game piece (checker) with a color and current position.
    The position can be:
        - an integer from 0 to 23 (on the board),
        - "bar" (captured),
        - "off" (borne off),
        - or None (unplaced).
    """

    def __init__(self, color, position=None):
        self._color_ = color
        self._position_ = position

        if position not in range(24) and position not in [None, "bar", "off"]:
            raise ValueError("Invalid position")

    @property
    def color(self):
        """Returns the color of the checker."""
        return self._color_

    @property
    def posicion(self):
        """Returns the current position of the checker."""
        return self._position_

    def mover_a(self, nueva_posicion):
        """
        Moves the checker to a new position.

        Args:
            nueva_posicion (int or str): Target position (0–23, "bar", or "off").

        Raises:
            ValueError: If the position is invalid.
        """
        if nueva_posicion not in range(24) and nueva_posicion not in ["bar", "off"]:
            raise ValueError("Invalid new position")
        self._position_ = nueva_posicion

    def __repr__(self):
        return f"Checker({self._color_}, {self._position_})"

    def __eq__(self, other):
        return (
            isinstance(other, Checker)
            and self._color_ == other._color_
            and self._position_ == other._position_
        )

    def __hash__(self):
        return hash((self._color_, self._position_))


class Punto:
    """
    Represents a point on the board. It may contain checkers belonging to a player.

    Attributes:
        _jugador_ (str): The owner of the point.
        _cantidad_ (int): Number of checkers on the point.
    """

    def __init__(self, jugador=None, cantidad=0):
        self._jugador_ = jugador
        self._cantidad_ = cantidad

    def esta_vacio(self):
        """Returns True if the point has no checkers."""
        return self._cantidad_ == 0

    def es_del_jugador(self, jugador):
        """Returns True if the point belongs to the given player."""
        return self._jugador_ == jugador

    def es_del_oponente(self, jugador):
        """Returns True if the point belongs to the opponent."""
        return self._jugador_ is not None and self._jugador_ != jugador

    def esta_bloqueado(self, jugador):
        """
        Returns True if the point is blocked for the given player.
        A point is blocked if it belongs to the opponent and has more than one checker.
        """
        return self.es_del_oponente(jugador) and self._cantidad_ > 1


def validar_movimiento(tablero, jugador, origen, destino, valor_dado):
    """
    Validates whether a move is legal based on basic game rules.

    Args:
        tablero (list of Punto): The current board state.
        jugador (str): The player's identifier ("Jugador1" or "Jugador2").
        origen (int): Origin point index (0–23).
        destino (int): Destination point index (0–23).
        valor_dado (int): The value of the die used for the move.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if origen not in range(24) or destino not in range(24):
        return False

    punto_origen = tablero[origen]
    punto_destino = tablero[destino]

    if punto_origen.esta_vacio() or not punto_origen.es_del_jugador(jugador):
        return False

    if abs(destino - origen) != valor_dado:
        return False

    if punto_destino.esta_bloqueado(jugador):
        return False

    if jugador == "Jugador1" and destino < origen:
        return False
    if jugador == "Jugador2" and destino > origen:
        return False

    return True

# Game.py:

from core.board import Board
from core.dados import Dice
from core.player import Jugador, TurnManager


class Game:
    """
    Coordina la lógica general del juego de Backgammon, incluyendo el estado del tablero,
    tiradas de dados, turnos de jugadores, validación de movimientos y condición de victoria.

    Atributos:
        board (Board): El tablero de juego.
        dice (Dice): El gestor de dados.
        jugador1 (Jugador): Jugador 1 (blanco).
        jugador2 (Jugador): Jugador 2 (negro).
        turnos (TurnManager): Administra la rotación de turnos.
        last_roll (list): Última tirada de dados.
        available_moves (list): Movimientos disponibles según los dados.
        historial (list): Historial de movimientos realizados.
    """

    def __init__(self):
        """
        Inicializa el juego con tablero, jugadores, dados y gestor de turnos.
        """
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Jugador("Jugador 1", "blanco")
        self.jugador2 = Jugador("Jugador 2", "negro")
        self.turnos = TurnManager(self.jugador1, self.jugador2)
        self.last_roll = []
        self.available_moves = []
        self.historial = []

        self._asignar_fichas_a_jugadores()

    def _asignar_fichas_a_jugadores(self):
        """
        Asigna las posiciones iniciales de las fichas según la configuración estándar.
        """
        posiciones = {
            "blanco": [0] * 2 + [11] * 5 + [16] * 3 + [18] * 5,
            "negro": [23] * 2 + [12] * 5 + [7] * 3 + [5] * 5,
        }
        for point in self.board._puntos_:
            point.clear()

        for color, puntos in posiciones.items():
            jugador = self.jugador1 if color == "blanco" else self.jugador2
            for ficha in jugador.fichas:
                ficha._position_ = None

            for i, punto in enumerate(puntos):
                jugador.fichas[i]._position_ = punto
                self.board._puntos_[punto].append(jugador.fichas[i])

    def tirar_dados(self):
        """
        Lanza los dados y actualiza los movimientos disponibles.

        Retorna:
            list: Valores obtenidos en la tirada.
        """
        self.last_roll = self.dice.roll_dice()
        self.available_moves = self.dice.get_moves()
        return self.last_roll

    def jugador_actual(self):
        """
        Retorna el jugador que tiene el turno actual.

        Retorna:
            Jugador: El jugador activo.
        """
        return self.turnos.jugador_actual()

    def cambiar_turno(self):
        """
        Cambia al turno del siguiente jugador.
        """
        self.turnos.siguiente_turno()

    def fichas_en_punto(self, punto, color):
        """
        Retorna las fichas de un color en un punto específico del tablero.

        Args:
            punto (int): Índice del punto en el tablero.
            color (str): Color del jugador.

        Retorna:
            list: Fichas en ese punto.
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        """
        Retorna las fichas de un color que están en la barra.

        Args:
            color (str): Color del jugador.

        Retorna:
            list: Fichas en la barra.
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        """
        Retorna las fichas de un color que ya fueron retiradas del tablero.

        Args:
            color (str): Color del jugador.

        Retorna:
            list: Fichas con posición "off".
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "off"]

    def puntos_validos_de_origen(self, color):
        """
        Retorna los puntos válidos desde donde el jugador puede mover fichas.

        Args:
            color (str): Color del jugador.

        Retorna:
            list: Puntos válidos o ["bar"] si hay fichas en la barra.
        """
        if self.fichas_en_barra(color):
            return ["bar"]
        return [p for p in range(24) if self.fichas_en_punto(p, color)]

    def puede_mover(self, origen, destino, color):
        """
        Verifica si un movimiento es válido según las reglas del juego.

        Args:
            origen (int o str): Punto de origen o "bar".
            destino (int o str): Punto de destino o "off".
            color (str): Color del jugador.

        Retorna:
            bool: True si el movimiento es válido, False si no lo es.
        """
        if self.fichas_en_barra(color) and origen != "bar":
            return False

        jugador = self._jugador_por_color(color)
        if destino == "off":
            if not jugador.puede_sacar_fichas(self.board):
                return False
            distancia = (24 - origen) if color == "blanco" else (origen + 1)
            return distancia in self.available_moves

        if not (0 <= destino <= 23):
            return False

        distancia = self._calcular_distancia(origen, destino, color)
        if distancia not in self.available_moves:
            return False

        destino_fichas = self.board._puntos_[destino]
        if (
            destino_fichas
            and destino_fichas[-1]._color_ != color
            and len(destino_fichas) > 1
        ):
            return False

        return True

    def mover_ficha(self, origen, destino, color):
        """
        Ejecuta un movimiento válido, incluyendo captura y registro en el historial.

        Args:
            origen (int o str): Punto de origen o "bar".
            destino (int o str): Punto de destino o "off".
            color (str): Color del jugador.

        Retorna:
            bool: True si el movimiento fue exitoso, False si no lo fue.
        """
        if not self.puede_mover(origen, destino, color):
            return False

        ficha = self._obtener_ficha_a_mover(origen, color)
        if not ficha:
            return False

        distancia = self._calcular_distancia(origen, destino, color)

        # Movimiento hacia fuera del tablero
        if destino == "off":
            ficha._position_ = "off"
            if origen != "bar" and self.board._puntos_[origen]:
                self.board._puntos_[origen].pop()

        else:
            destino_fichas = self.board._puntos_[destino]

            # Captura si hay una sola ficha rival
            if (
                destino_fichas
                and destino_fichas[-1]._color_ != color
                and len(destino_fichas) == 1
            ):
                rival = destino_fichas[-1]
                rival._position_ = "bar"
                self.board._puntos_[destino].pop()

            ficha._position_ = destino

            if origen != "bar" and self.board._puntos_[origen]:
                self.board._puntos_[origen].pop()

            self.board._puntos_[destino].append(ficha)

        if distancia in self.available_moves:
            self.available_moves.remove(distancia)

        self.historial.append(
            {
                "jugador": color,
                "origen": origen,
                "destino": destino,
                "dados": self.last_roll,
            }
        )

        return True

    def _obtener_ficha_a_mover(self, origen, color):
        """
        Obtiene la ficha que se va a mover desde el origen.

        Args:
            origen (int o str): Punto de origen o "bar".
            color (str): Color del jugador.

        Retorna:
            Ficha o None: La ficha a mover, si existe.
        """
        fichas = (
            self.fichas_en_barra(color)
            if origen == "bar"
            else self.fichas_en_punto(origen, color)
        )
        return fichas[0] if fichas else None

    def _jugador_por_color(self, color):
        """
        Retorna el objeto jugador según el color.

        Args:
            color (str): "blanco" o "negro".

        Retorna:
            Jugador: El jugador correspondiente.
        """
        return self.jugador1 if color == "blanco" else self.jugador2

    def _calcular_distancia(self, origen, destino, color):
        """
        Calcula la distancia del movimiento según origen, destino y color.

        Args:
            origen (int o str): Punto de origen o "bar".
            destino (int o str): Punto de destino o "off".
            color (str): Color del jugador.

        Retorna:
            int: Distancia del movimiento.
        """
        if origen == "bar":
            return (24 - destino) if color == "blanco" else (destino + 1)
        if destino == "off":
            return (24 - origen) if color == "blanco" else (origen + 1)
        return abs(destino - origen)

    def verificar_ganador(self):
        """
        Verifica si algún jugador ha ganado la partida.

        Retorna:
            str o None: Nombre del jugador ganador, o None si aún no hay ganador.
        """
        if len(self.fichas_borneadas("blanco")) == 15:
            return self.jugador1.nombre
        if len(self.fichas_borneadas("negro")) == 15:
            return self.jugador2.nombre
        return None

    def mostrar_estado(self):
        """
        Muestra el estado actual del juego en la consola.
        """
        jugador = self.jugador_actual()
        print(f"\nTurno: {jugador.nombre} ({jugador.color})")
        print(f"Fichas en la barra: {len(self.fichas_en_barra(jugador.color))}")
        print(f"Fichas retiradas: {len(self.fichas_borneadas(jugador.color))}")
        print(f"Última tirada: {self.last_roll}")
        print(f"Movimientos disponibles: {self.available_moves}")

# player.py:

"""Modulo que contiene las clases Jugador y TurnManager."""

from .checker import Checker


class Jugador:
    """
    Representa a un jugador de Backgammon.
    Administra nombre, color, fichas, puntaje y condicion de victoria.

    Atributos:
        nombre (str): Nombre del jugador.
        color (str): Color de sus fichas ("blanco" o "negro").
        puntos (int): Puntaje acumulado.
        fichas_fuera (int): Cantidad de fichas retiradas del tablero.
        fichas (list): Lista de 15 objetos Checker que pertenecen al jugador.
    """

    def __init__(self, nombre, color):
        """
        Inicializa un jugador con nombre, color y 15 fichas.

        Args:
            nombre (str): Nombre del jugador.
            color (str): Color de las fichas ("blanco" o "negro").
        """
        self.nombre = nombre
        self.color = color
        self.puntos = 0
        self.fichas_fuera = 0
        self.fichas = [Checker(color, None) for _ in range(15)]

    def __str__(self):
        """
        Representacion en texto del jugador.

        Returns:
            str: Descripcion del jugador y su color de fichas.
        """
        return f"{self.nombre} juega con fichas {self.color}"

    def sumar_puntos(self, cantidad, verbose=True):
        """
        Suma puntos al puntaje del jugador.

        Args:
            cantidad (int): Cantidad de puntos a sumar.
            verbose (bool): Si se debe imprimir el resultado.
        """
        self.puntos += cantidad
        if verbose:
            print(f"{self.nombre} gana {cantidad} puntos. Total: {self.puntos}")

    def sacar_ficha(self, verbose=True):
        """
        Marca una ficha como retirada del tablero.

        Args:
            verbose (bool): Si se debe imprimir el resultado.
        """
        self.fichas_fuera += 1
        if verbose:
            print(
                f"{self.nombre} ha retirado una ficha. Total fuera: {self.fichas_fuera}"
            )

    def ha_ganado(self):
        """
        Verifica si el jugador ha ganado (todas sus fichas estan fuera).

        Returns:
            bool: True si todas las fichas estan en posicion "off".
        """
        return all(f._position_ == "off" for f in self.fichas)

    def fichas_en_estado(self, estado):
        """
        Devuelve las fichas que estan en un estado especifico.

        Args:
            estado (str): Estado de la ficha ("bar", "off" o None).

        Returns:
            list: Fichas que coinciden con el estado dado.
        """
        return [f for f in self.fichas if f._position_ == estado]

    def fichas_en_punto(self, punto):
        """
        Devuelve las fichas que estan en un punto especifico del tablero.

        Args:
            punto (int): Indice del punto en el tablero.

        Returns:
            list: Fichas ubicadas en ese punto.
        """
        return [f for f in self.fichas if f._position_ == punto]

    def puede_sacar_fichas(self, board):
        """
        Verifica si el jugador puede comenzar a retirar fichas.

        Args:
            board (Board): El tablero de juego.

        Returns:
            bool: True si todas las fichas activas estan en la zona de salida.
        """
        if self.color == "blanco":
            # Zona de salida del blanco: puntos 18 a 23
            rango_casa = range(18, 24)
        else:
            # Zona de salida del negro: puntos 0 a 5
            rango_casa = range(6)

        return all(
            f._position_ in rango_casa or f._position_ == "off"
            for f in self.fichas
            if f._position_ != "bar"
        )


class TurnManager:
    """
    Administra la rotacion de turnos entre dos jugadores.

    Atributos:
        jugadores (list): Lista de dos objetos Jugador.
        indice_actual (int): Indice del jugador actual.
    """

    def __init__(self, jugador1, jugador2):
        """
        Inicializa el gestor de turnos con dos jugadores.

        Args:
            jugador1 (Jugador): Primer jugador.
            jugador2 (Jugador): Segundo jugador.
        """
        self.jugadores = [jugador1, jugador2]
        self.indice_actual = 0

    def jugador_actual(self):
        """
        Devuelve el jugador que tiene el turno actual.

        Returns:
            Jugador: Jugador activo.
        """
        return self.jugadores[self.indice_actual]

    def siguiente_turno(self):
        """
        Cambia al turno del siguiente jugador.
        """
        self.indice_actual = (self.indice_actual + 1) % len(self.jugadores)

    def mostrar_turno(self, verbose=True):
        """
        Muestra en consola el turno actual.

        Args:
            verbose (bool): Si se debe imprimir el turno.
        """
        if verbose:
            jugador = self.jugador_actual()
            print(f"\nTurno: {jugador.nombre} ({jugador.color})")

# test_player.py:

import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from core.player import Jugador, TurnManager


class TestJugador(unittest.TestCase):
    """Pruebas unitarias para la clase Jugador."""

    def setUp(self):
        """Inicializa dos jugadores antes de cada prueba."""
        self.jugador = Jugador("Jugador 1", "blanco")
        self.jugador_negro = Jugador("Jugador 2", "negro")

    def test_jugador_se_inicializa_correctamente(self):
        """Verifica que los atributos iniciales del jugador sean correctos."""
        self.assertEqual(self.jugador.nombre, "Jugador 1")
        self.assertEqual(self.jugador.color, "blanco")
        self.assertEqual(self.jugador.puntos, 0)
        self.assertEqual(self.jugador.fichas_fuera, 0)
        self.assertEqual(len(self.jugador.fichas), 15)

    def test_str_representacion(self):
        """Verifica la representación en texto del jugador."""
        self.assertEqual(str(self.jugador), "Jugador 1 juega con fichas blanco")

    def test_sumar_puntos_incrementa_correctamente(self):
        """Verifica que los puntos se acumulen correctamente."""
        self.jugador.sumar_puntos(5)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3)
        self.assertEqual(self.jugador.puntos, 8)

    def test_sacar_ficha_incrementa_fichas_fuera(self):
        """Verifica que sacar fichas aumente el contador de fichas fuera."""
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 1)
        for _ in range(4):
            self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 5)

    def test_ha_ganado_devuelve_false_si_faltan_fichas(self):
        """Verifica que no se declare victoria si faltan fichas fuera."""
        self.assertFalse(self.jugador.ha_ganado())
        for _ in range(14):
            self.jugador.sacar_ficha()
        self.assertFalse(self.jugador.ha_ganado())

    def test_ha_ganado_devuelve_true_si_tiene_15_fichas_fuera(self):
        """Verifica que se declare victoria si todas las fichas están fuera."""
        for ficha in self.jugador.fichas:
            ficha._position_ = "off"
        self.assertTrue(self.jugador.ha_ganado())

    def test_fichas_en_estado(self):
        """Verifica que se filtren correctamente las fichas por estado."""
        self.jugador.fichas[0]._position_ = "bar"
        self.jugador.fichas[1]._position_ = "off"
        self.assertEqual(len(self.jugador.fichas_en_estado("bar")), 1)
        self.assertEqual(len(self.jugador.fichas_en_estado("off")), 1)

    def test_fichas_en_punto(self):
        """Verifica que se filtren correctamente las fichas por punto."""
        self.jugador.fichas[0]._position_ = 5
        self.jugador.fichas[1]._position_ = 5
        self.assertEqual(len(self.jugador.fichas_en_punto(5)), 2)

    def test_puede_sacar_fichas_blancas(self):
        """Verifica que las fichas blancas puedan ser borneadas si están en casa."""
        mock_board = MagicMock()
        for i in range(15):
            self.jugador.fichas[i]._position_ = 18 + (i % 6)
        self.assertTrue(self.jugador.puede_sacar_fichas(mock_board))

    def test_puede_sacar_fichas_negras(self):
        """Verifica que las fichas negras puedan ser borneadas si están en casa."""
        mock_board = MagicMock()
        for i in range(15):
            self.jugador_negro.fichas[i]._position_ = i % 6
        self.assertTrue(self.jugador_negro.puede_sacar_fichas(mock_board))

    def test_no_puede_sacar_fichas_si_no_estan_en_casa(self):
        """Verifica que no se puedan bornear fichas si alguna está fuera de casa."""
        mock_board = MagicMock()
        self.jugador.fichas[0]._position_ = 17
        self.assertFalse(self.jugador.puede_sacar_fichas(mock_board))


class TestTurnManager(unittest.TestCase):
    """Pruebas unitarias para la clase TurnManager."""

    def setUp(self):
        """Inicializa dos jugadores y el administrador de turnos."""
        self.jugador_a = Jugador("A", "white")
        self.jugador_b = Jugador("B", "black")
        self.tm = TurnManager(self.jugador_a, self.jugador_b)

    def test_alternancia_de_turnos_funciona_correctamente(self):
        """Verifica que los turnos alternen correctamente entre jugadores."""
        self.assertEqual(self.tm.jugador_actual().nombre, "A")
        self.tm.siguiente_turno()
        self.assertEqual(self.tm.jugador_actual().nombre, "B")
        self.tm.siguiente_turno()
        self.assertEqual(self.tm.jugador_actual().nombre, "A")

    @patch("sys.stdout", new_callable=StringIO)
    def test_mostrar_turno(self, mock_stdout):
        """Verifica que se imprima correctamente el turno actual."""
        self.tm.mostrar_turno()
        self.assertIn("Turno: A (white)", mock_stdout.getvalue())
        self.tm.siguiente_turno()
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        self.tm.mostrar_turno()
        self.assertIn("Turno: B (black)", mock_stdout.getvalue())

#  test_checker.py:

import unittest
from core.checker import Checker, Punto, validar_movimiento


class TestChecker(unittest.TestCase):
    def test_init(self):
        checker = Checker("blanco", 1)
        self.assertEqual(checker.color, "blanco")
        self.assertEqual(checker.posicion, 1)

    def test_init_invalid_position(self):
        with self.assertRaises(ValueError):
            Checker("blanco", 24)

    def test_mover_a(self):
        checker = Checker("blanco", 1)
        checker.mover_a(2)
        self.assertEqual(checker.posicion, 2)

    def test_mover_a_invalid_position(self):
        checker = Checker("blanco", 1)
        with self.assertRaises(ValueError):
            checker.mover_a(24)

    def test_repr(self):
        checker = Checker("blanco", 1)
        self.assertEqual(repr(checker), "Checker(blanco, 1)")

    def test_eq(self):
        checker1 = Checker("blanco", 1)
        checker2 = Checker("blanco", 1)
        self.assertEqual(checker1, checker2)

    def test_hash(self):
        checker1 = Checker("blanco", 1)
        checker2 = Checker("blanco", 1)
        self.assertEqual(hash(checker1), hash(checker2))


class TestPunto(unittest.TestCase):
    def test_esta_vacio(self):
        punto = Punto()
        self.assertTrue(punto.esta_vacio())

    def test_es_del_jugador(self):
        punto = Punto("Jugador1", 1)
        self.assertTrue(punto.es_del_jugador("Jugador1"))

    def test_es_del_oponente(self):
        punto = Punto("Jugador2", 1)
        self.assertTrue(punto.es_del_oponente("Jugador1"))

    def test_esta_bloqueado(self):
        punto = Punto("Jugador2", 2)
        self.assertTrue(punto.esta_bloqueado("Jugador1"))


class TestValidacion(unittest.TestCase):

    def test_valido_sin_obstaculos_en_rango_correcto(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[8] = Punto(None, 0)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_valido_con_captura_de_oponente(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador2", 1)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_dado_incorrecto(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[9] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 9, 3))

    def test_invalido_por_punto_bloqueado(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[8] = Punto("Jugador2", 2)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_direccion_contraria(self):
        tablero = [Punto() for _ in range(24)]
        tablero[8] = Punto("Jugador1", 1)
        tablero[5] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 8, 5, 3))

    def test_fuera_de_rango_origen(self):
        tablero = [Punto() for _ in range(24)]
        self.assertFalse(validar_movimiento(tablero, "Jugador1", -1, 5, 3))

    def test_fuera_de_rango_destino(self):
        tablero = [Punto() for _ in range(24)]
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 24, 3))

    def test_sin_fichas_en_origen(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto(None, 0)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_color_incorrecto_en_origen(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador2", 1)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_valido_a_punto_propio(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador1", 2)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_doble_ficha_oponente(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador2", 2)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_direccion_contraria_jugador2(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador2", 1)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador2", 5, 8, 3))

# test_dados.py:

import unittest
from core.dados import Dice


class TestDice(unittest.TestCase):
    """Pruebas unitarias para la clase Dice (dados del juego)."""

    def test_roll_dice_returns_valid_values(self):
        """Verifica que al tirar los dados se obtengan valores entre 1 y 6."""
        dice = Dice()
        val1, val2 = dice.roll_dice()
        self.assertIn(val1, range(1, 7))
        self.assertIn(val2, range(1, 7))

    def test_get_values_reflects_last_roll(self):
        """Verifica que get_values devuelva el último resultado de los dados."""
        dice = Dice()
        rolled = dice.roll_dice()
        self.assertEqual(dice.get_values(), rolled)

    def test_is_double_true(self):
        """Verifica que is_double devuelva True cuando ambos dados son iguales."""
        dice = Dice()
        dice.set_values_for_test(4, 4)
        self.assertTrue(dice.is_double())

    def test_is_double_false(self):
        """Verifica que is_double devuelva False cuando los dados son distintos."""
        dice = Dice()
        dice.set_values_for_test(3, 5)
        self.assertFalse(dice.is_double())

    def test_set_values_for_test_sets_correctly(self):
        """Verifica que set_values_for_test asigne correctamente los valores."""
        dice = Dice()
        dice.set_values_for_test(2, 6)
        self.assertEqual(dice.get_values(), (2, 6))

    def test_get_moves_for_double(self):
        """Verifica que get_moves devuelva cuatro movimientos si hay doble."""
        dice = Dice()
        dice.set_values_for_test(5, 5)
        self.assertEqual(dice.get_moves(), [5, 5, 5, 5])

    def test_get_moves_for_non_double(self):
        """Verifica que get_moves devuelva dos movimientos si no hay doble."""
        dice = Dice()
        dice.set_values_for_test(2, 4)
        self.assertEqual(dice.get_moves(), [2, 4])

    def test_set_values_for_test_invalid_values(self):
        """Verifica que set_values_for_test lance error con valores inválidos."""
        dice = Dice()
        with self.assertRaises(ValueError):
            dice.set_values_for_test(0, 5)
        with self.assertRaises(ValueError):
            dice.set_values_for_test(7, 5)

# test_board.py:

import unittest
import io
from unittest.mock import patch
from core.board import Board
from core.checker import Checker


class TestBoard(unittest.TestCase):
    """Pruebas unitarias para el módulo Board."""

    def setUp(self):
        """Inicializa un tablero con fichas estándar antes de cada prueba."""
        self.board = Board()
        self.board.inicializar_fichas()

    def test_inicializacion_correcta(self):
        """Verifica que las fichas iniciales estén en las posiciones correctas."""
        self.assertEqual(len(self.board._puntos_[0]), 2)
        self.assertTrue(all(f._color_ == "blanco" for f in self.board._puntos_[0]))
        self.assertEqual(len(self.board._puntos_[23]), 2)
        self.assertTrue(all(f._color_ == "negro" for f in self.board._puntos_[23]))

    def test_mover_ficha_valida(self):
        """Verifica que una ficha se mueva correctamente entre puntos válidos."""
        self.board._puntos_[12] = []
        self.board.mover_ficha(11, 12, "blanco")
        self.assertEqual(len(self.board._puntos_[11]), 4)
        self.assertEqual(len(self.board._puntos_[12]), 1)
        self.assertEqual(self.board._puntos_[12][0]._position_, 12)

    def test_mover_ficha_con_captura(self):
        """Verifica que se capture una ficha rival si hay una sola en destino."""
        self.board._puntos_[12] = [Checker("negro", 12)]
        self.board._puntos_[11] = [Checker("blanco", 11)]
        self.board.mover_ficha(11, 12, "blanco")
        self.assertEqual(len(self.board._puntos_[12]), 1)
        self.assertEqual(self.board._puntos_[12][0]._color_, "blanco")

    def test_mover_ficha_color_incorrecto(self):
        """Verifica que no se pueda mover una ficha si el color no coincide."""
        self.board._puntos_[12] = [Checker("negro", 12)]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(12, 13, "blanco")

    def test_mover_ficha_origen_vacio(self):
        """Verifica que no se pueda mover desde un punto vacío."""
        self.board._puntos_[10] = []
        with self.assertRaises(ValueError):
            self.board.mover_ficha(10, 11, "blanco")

    def test_mover_ficha_fuera_de_rango(self):
        """Verifica que no se pueda mover desde o hacia posiciones inválidas."""
        self.board._puntos_[0] = [Checker("blanco", 0)]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(-1, 5, "blanco")
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 24, "blanco")

    def test_eliminar_ficha_si_unica(self):
        """Verifica que se elimine correctamente una ficha única del punto."""
        self.board._puntos_[5] = [Checker("negro", 5)]
        ficha = self.board.eliminar_ficha_si_unica(5, "negro")
        self.assertEqual(ficha._color_, "negro")
        self.assertEqual(self.board._puntos_[5], [])

    def test_eliminar_ficha_falla_si_multiple(self):
        """Verifica que no se elimine si hay más de una ficha en el punto."""
        self.board._puntos_[5] = [Checker("negro", 5), Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "negro")

    def test_eliminar_ficha_color_incorrecto(self):
        """Verifica que no se elimine si el color no coincide con el jugador."""
        self.board._puntos_[5] = [Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "blanco")

    def test_eliminar_ficha_fuera_de_rango(self):
        """Verifica que no se pueda eliminar desde una posición inválida."""
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(24, "blanco")

    def test_puede_entrar_desde_bar_blanco(self):
        """Verifica los casos válidos e inválidos de entrada desde la barra para blanco."""
        self.board._puntos_[3] = []
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 3))
        self.board._puntos_[4] = [Checker("blanco", 4)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 4))
        self.board._puntos_[5] = [Checker("negro", 5)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 5))
        self.board._puntos_[6] = [Checker("negro", 6), Checker("negro", 6)]
        self.assertFalse(self.board.puede_entrar_desde_bar("blanco", 6))

    def test_puede_entrar_desde_bar_negro(self):
        """Verifica la entrada desde la barra para el jugador negro."""
        for i in range(18, 24):
            self.board._puntos_[i] = []
        self.assertTrue(self.board.puede_entrar_desde_bar("negro", 18))

    def test_reingreso_exitoso(self):
        """Verifica que se pueda reingresar desde la barra si hay espacio disponible."""
        entrada = self.board.intentar_reingreso("blanco")
        self.assertIn(entrada, range(0, 6))
        self.assertTrue(
            any(f._color_ == "blanco" for f in self.board._puntos_[entrada])
        )

    def test_reingreso_prioriza_punto_mas_bajo(self):
        """Verifica que el reingreso se haga en el primer punto disponible."""
        self.board._puntos_[0] = []
        self.board._puntos_[1] = []
        entrada = self.board.intentar_reingreso("blanco")
        self.assertEqual(entrada, 0)

    def test_reingreso_fallido(self):
        """Verifica que no se pueda reingresar si todos los puntos están bloqueados."""
        b = Board()
        for i in range(6):
            b._puntos_[i] = [Checker("negro", i), Checker("negro", i)]
        entrada = b.intentar_reingreso("blanco")
        self.assertIsNone(entrada)

    def test_registro_de_jugada_con_captura(self):
        """Verifica que se registre correctamente una jugada con captura."""
        self.board.registrar_jugada("blanco", 0, 5, captura=True)
        self.assertEqual(len(self.board.historial_de_jugadas), 1)
        jugada = self.board.historial_de_jugadas[0]
        self.assertEqual(jugada["jugador"], "blanco")
        self.assertEqual(jugada["origen"], 0)
        self.assertEqual(jugada["destino"], 5)
        self.assertTrue(jugada["captura"])

    def test_registro_de_jugada_sin_captura(self):
        """Verifica que se registre correctamente una jugada sin captura."""
        self.board.registrar_jugada("negro", 5, 10)
        jugada = self.board.historial_de_jugadas[0]
        self.assertEqual(jugada["jugador"], "negro")
        self.assertEqual(jugada["origen"], 5)
        self.assertEqual(jugada["destino"], 10)
        self.assertFalse(jugada["captura"])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_mostrar_historial(self, mock_stdout):
        """Verifica que el historial de jugadas se imprima correctamente."""
        self.board.registrar_jugada("blanco", 0, 5, captura=True)
        self.board.mostrar_historial()
        output = mock_stdout.getvalue()
        self.assertIn("Move history:", output)
        self.assertIn("blanco moved from 0 to 5 (capture)", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_mostrar_tablero(self, mock_stdout):
        """Verifica que el tablero se imprima correctamente en consola."""
        self.board.mostrar_tablero()
        output = mock_stdout.getvalue()
        self.assertIn("TOP ZONE", output)
        self.assertIn("BOTTOM ZONE", output)
        self.assertIn("B", output)
        self.assertIn("N", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_mostrar_tablero_con_barra_y_borneadas(self, mock_stdout):
        """Verifica que se impriman correctamente las fichas en barra y borneadas."""
        self.board._barra_bl

# test_cli.py:

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import TableroView, EstadoView, fichas_movibles, ejecutar_cli
from core.game import Game


class TestCli(unittest.TestCase):
    """Pruebas completas para la interfaz de linea de comandos."""

    def setUp(self):
        self.juego = Game()
        self.tablero_view = TableroView()
        self.estado_view = EstadoView()

    def test_mostrar_tablero(self):
        """Verifica que el tablero se imprime correctamente."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Estado del tablero", output)
            self.assertIn("BARRA", output)
            self.assertIn("Fichas borneadas", output)

    def test_mostrar_estado(self):
        """Verifica que el estado se muestra correctamente."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Turno de", output)
            self.assertIn("Fichas en barra", output)
            self.assertIn("Movimientos disponibles", output)

    def test_mostrar_tablero_vacio(self):
        """Cubre tablero vacio sin fichas."""
        self.juego.board._puntos_ = [[] for _ in range(24)]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Estado del tablero", output)

    def test_mostrar_estado_con_datos(self):
        """Cubre el caso donde hay fichas en barra y borneadas."""
        self.juego.turno = "negro"
        self.juego.fichas_en_barra = MagicMock(return_value=[1, 2])
        self.juego.available_moves = [4, 6]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Turno de", output)
            self.assertIn("Jugador", output)

    def test_fichas_movibles_con_movimientos(self):
        """Cubre fichas movibles."""
        self.juego.available_moves = [3, 4]
        self.juego.board.inicializar_fichas()
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertTrue(isinstance(fichas, list))

    def test_fichas_movibles_sin_movimientos(self):
        """Cubre el caso sin movimientos."""
        self.juego.available_moves = []
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertEqual(len(fichas), 0)

    @patch("builtins.input")
    def test_ejecutar_cli_movimiento_valido_y_salida(self, mock_input):
        """Flujo basico con movimiento y salida."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3, 4]

        def mover_y_limpiar(*args):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover_y_limpiar)
        mock_input.side_effect = ["", "0", "4", "n"]

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()

        salida = fake_out.getvalue()
        self.assertIn("Movimiento exitoso", salida)
        self.assertIn("Fin del juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_sin_movimientos_posibles(self, mock_input):
        """Jugador sin movimientos."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 1]
        mock_input.side_effect = ["", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("No hay movimientos posibles", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_entrada_invalida(self, mock_input):
        """Entrada no numerica."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 2]

        def mover(*args):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover)
        mock_input.side_effect = ["", "abc", "0", "3", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles", return_value=[(MagicMock(_position_=1), [3])]
            ):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Entrada invalida", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_victoria(self, mock_input):
        """Flujo donde un jugador gana."""
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 1"])
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        mock_input.side_effect = ["", "s", ""]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Jugador 1 ha ganado el juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_continuar_turno_y_ganar(self, mock_input):
        """Jugador continua y luego gana."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 2"])
        mock_input.side_effect = ["", "s", ""]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Jugador 2 ha ganado el juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_index_error_en_seleccion(self, mock_input):
        """Seleccion fuera del rango."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [2]
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_input.side_effect = ["", "99", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles", return_value=[(MagicMock(_position_=0), [2])]
            ):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Entrada invalida", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_sin_ganador_y_salida_manual(self, mock_input):
        """Jugador sale sin ganar."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_input.side_effect = ["", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Fin del juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_movimiento_invalido_reintento(self, mock_input):
        """Cubre un intento de movimiento invalido seguido de exito."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3]
        self.juego.mover_ficha = MagicMock(side_effect=[False, True])
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_input.side_effect = ["", "0", "4", "0", "3", "n"]
        mock_ficha = MagicMock(_position_=0, _color_="blanco")
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[(mock_ficha, [3])]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Movimiento invalido", salida)
        self.assertIn("Movimiento exitoso", salida)

    def test_tablero_view_con_fichas_largas(self):
        """Punto con muchas fichas."""
        mock_ficha = MagicMock(_color_="blanco")
        self.juego.board._puntos_[0] = [mock_ficha] * 6
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_ficha] * 6)
        self.juego.fichas_borneadas = MagicMock(return_value=[])
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            salida = fake_out.getvalue()
            self.assertIn("6", salida)

    def test_tablero_view_con_fichas_en_todos_los_segmentos(self):
        """Puntos, barra y borneadas activas."""
        mock_blanca = MagicMock(_color_="blanco")
        mock_negra = MagicMock(_color_="negro")
        self.juego.board._puntos_[12] = [mock_blanca] * 3
        self.juego.board._puntos_[18] = [mock_negra] * 2
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_blanca, mock_negra])
        self.juego.fichas_borneadas = MagicMock(
            side_effect=lambda color: (
                [mock_blanca] * 2 if color == "blanco" else [mock_negra]
            )
        )
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            salida = fake_out.getvalue()
            self.assertIn("Estado del tablero", salida)
            self.assertIn("BARRA", salida)
            self.assertIn("Fichas borneadas", salida)

    def test_estado_view_con_muchos_movimientos(self):
        """Cubre el caso con varios movimientos disponibles."""
        self.juego.available_moves = [1, 2, 3, 4]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            salida = fake_out.getvalue()
            self.assertIn("Movimientos disponibles", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_con_instancia_real(self, mock_input):
        """Ejecuta el CLI con Game real para cubrir líneas finales."""
        mock_input.side_effect = ["", "n"]  # tirar dados, salir

        with patch("sys.stdout", new=StringIO()) as fake_out:
            ejecutar_cli()

        salida = fake_out.getvalue()
        self.assertIn("Fin del juego", salida)


if __name__ == "__main__":
    unittest.main()


