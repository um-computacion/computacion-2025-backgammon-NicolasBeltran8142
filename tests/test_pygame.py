import unittest
from unittest.mock import patch, MagicMock
import pygame
from pygame_ui import ui
from core.game import Game

class TestUICoordinateFunctions(unittest.TestCase):

    def test_get_visual_column(self):
        self.assertEqual(ui._get_visual_column(0), 11)
        self.assertEqual(ui._get_visual_column(5), 6)
        self.assertEqual(ui._get_visual_column(6), 5)
        self.assertEqual(ui._get_visual_column(11), 0)
        self.assertEqual(ui._get_visual_column(12), 0)
        self.assertEqual(ui._get_visual_column(17), 5)
        self.assertEqual(ui._get_visual_column(18), 6)
        self.assertEqual(ui._get_visual_column(23), 11)
        self.assertEqual(ui._get_visual_column(24), -1)
        
    def test_get_column_x_coord(self):
        # Test a column in the left half
        x_left = ui._get_column_x_coord(0)
        self.assertTrue(ui.BOARD_X < x_left < ui.BOARD_X + (ui.WIDTH - ui.BOARD_X) / 2)
        # Test a column in the right half
        x_right = ui._get_column_x_coord(6)
        self.assertTrue(ui.BOARD_X + (ui.WIDTH - ui.BOARD_X) / 2 < x_right < ui.WIDTH)

    def test_get_point_center(self):
        x, y = ui.get_point_center(0)
        self.assertTrue(ui.BOARD_X < x < ui.WIDTH)
        self.assertTrue(ui.HEIGHT/2 < y < ui.HEIGHT)
        x, y = ui.get_point_center(12)
        self.assertTrue(ui.BOARD_X < x < ui.WIDTH)
        self.assertTrue(0 < y < ui.HEIGHT/2)

    def test_get_point_rect(self):
        rect = ui.get_point_rect(5)
        self.assertIsInstance(rect, pygame.Rect)
        self.assertTrue(rect.width > 0)
        self.assertTrue(rect.height > 0)

    @patch('pygame_ui.ui.get_point_rect')
    def test_get_point_from_pos(self, mock_get_point_rect):
        mock_get_point_rect.side_effect = lambda i: {
            0: pygame.Rect(300, 400, 50, 300),
            1: pygame.Rect(350, 400, 50, 300)
        }.get(i, pygame.Rect(0,0,0,0))
        self.assertEqual(ui.get_point_from_pos((325, 500)), 0)
        self.assertEqual(ui.get_point_from_pos((375, 500)), 1)
        self.assertIsNone(ui.get_point_from_pos((10, 10)))
        bar_x = ui.BOARD_X + ui.MARGIN + 6 * ui.POINT_WIDTH + 10
        self.assertEqual(ui.get_point_from_pos((bar_x, 300)), "bar")
        bear_off_x = ui.BEAR_OFF_X + 10
        self.assertEqual(ui.get_point_from_pos((bear_off_x, 300)), "off")

class TestUIDrawingFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_screen = MagicMock()
        self.mock_font = MagicMock()
        self.game = Game()

    @patch('pygame.font.Font')
    def test_draw_text(self, mock_font_constructor):
        mock_font_instance = MagicMock()
        mock_font_constructor.return_value = mock_font_instance
        ui.draw_text(self.mock_screen, "Test", mock_font_instance, (0,0,0), 100, 100)
        self.assertTrue(mock_font_instance.render.called)
        self.assertTrue(self.mock_screen.blit.called)

    @patch('pygame.font.Font')
    @patch('pygame.draw.rect')
    @patch('pygame.draw.polygon')
    @patch('pygame.draw.line')
    @patch('pygame_ui.ui.draw_text')
    def test_draw_board(self, mock_draw_text, mock_draw_line, mock_draw_polygon, mock_draw_rect, mock_font):
        ui.draw_board(self.mock_screen)
        self.assertTrue(mock_draw_rect.call_count > 0)
        self.assertTrue(mock_draw_polygon.call_count > 0)

    @patch('pygame.draw.circle')
    @patch('pygame_ui.ui.draw_text')
    def test_draw_checkers(self, mock_draw_text, mock_draw_circle):
        self.game.board._puntos_[0] = [MagicMock(_color_="blanco")]
        self.game.fichas_borneadas = MagicMock(return_value=[MagicMock()])
        self.game.fichas_en_barra = MagicMock(return_value=[MagicMock(_color_="blanco")])
        ui.draw_checkers(self.mock_screen, self.mock_font, self.game)
        self.assertTrue(mock_draw_circle.called)

    @patch('pygame.Surface')
    def test_draw_highlights(self, mock_surface):
        mock_surf_instance = MagicMock()
        mock_surface.return_value = mock_surf_instance
        ui.draw_highlights(self.mock_screen, [1, 2], "blanco")
        self.assertTrue(self.mock_screen.blit.called)

    @patch('pygame.draw.rect')
    @patch('pygame_ui.ui.draw_text')
    def test_draw_side_panel(self, mock_draw_text, mock_draw_rect):
        ui.draw_side_panel(self.mock_screen, self.mock_font, self.game)
        self.assertTrue(mock_draw_rect.called)
        self.assertTrue(mock_draw_text.call_count > 3)

    @patch('pygame_ui.ui.draw_text')
    def test_draw_dice_and_moves(self, mock_draw_text):
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        ui.draw_dice_and_moves(self.mock_screen, self.mock_font, self.game)
        self.assertTrue(mock_draw_text.call_count >= 4)

class TestHandleEvent(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock(spec=Game)
        self.game.jugador_actual.return_value.color = "blanco"
        self.game.board = MagicMock()
        self.game.board._puntos_ = [[] for _ in range(24)]
        self.game.available_moves = []
        self.game.last_roll = []

    @patch('pygame_ui.ui.Game')
    def test_start_screen_click_start_button(self, mock_game_class):
        mock_game_instance = MagicMock()
        mock_game_class.return_value = mock_game_instance
        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=ui.start_button.center)
        
        game, game_state, _, _, _, p1, p2, _, _, _ = ui.handle_event(event, None, ui.START_SCREEN, False, None, [], "P1", "P2", None)
        
        self.assertEqual(game_state, ui.GAME_SCREEN)
        self.assertIsNotNone(game)
        self.assertEqual(game.jugador1.nombre, "P1")

    @patch('pygame.mouse.get_pos')
    def test_game_screen_click_roll_dice(self, mock_get_pos):
        mock_get_pos.return_value = ui.roll_dice_button.center
        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=ui.roll_dice_button.center)

        _, _, dice_rolled, _, _, _, _, _, _, _ = ui.handle_event(event, self.game, ui.GAME_SCREEN, False, None, [], "P1", "P2", None)
        
        self.assertTrue(dice_rolled)
        self.game.tirar_dados.assert_called_once()

    @patch('pygame.mouse.get_pos')
    @patch('pygame_ui.ui.get_point_from_pos', return_value=17)
    def test_game_screen_move_checker_successfully(self, mock_get_point, mock_get_pos):
        mock_get_pos.return_value = (20, 20)
        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(20, 20))
        self.game.mover_ficha.return_value = True
        self.game.available_moves = []

        _, _, _, selected_point, possible_moves, _, _, _, _, _ = ui.handle_event(event, self.game, ui.GAME_SCREEN, True, 18, [17], "P1", "P2", None)
        
        self.game.mover_ficha.assert_called_with(18, 17, "blanco")
        self.assertIsNone(selected_point)
        self.assertEqual(possible_moves, [])

    def test_start_screen_type_in_input_box(self):
        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode='a')
        
        _, _, _, _, _, p1, _, _, _, _ = ui.handle_event(event, None, ui.START_SCREEN, False, None, [], "Player 1", "P2", ui.input_box1)
        
        self.assertEqual(p1, "Player 1a")
