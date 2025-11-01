import unittest
from unittest.mock import patch, MagicMock
import pygame
from pygame_ui import ui
from core.game import Game

class TestUICoordinateFunctions(unittest.TestCase):

    def test_get_visual_column(self):
        # Bottom-right quadrant (points 0-5)
        self.assertEqual(ui._get_visual_column(0), 11)
        self.assertEqual(ui._get_visual_column(5), 6)
        # Bottom-left quadrant (points 6-11)
        self.assertEqual(ui._get_visual_column(6), 5)
        self.assertEqual(ui._get_visual_column(11), 0)
        # Top-left quadrant (points 12-17)
        self.assertEqual(ui._get_visual_column(12), 0)
        self.assertEqual(ui._get_visual_column(17), 5)
        # Top-right quadrant (points 18-23)
        self.assertEqual(ui._get_visual_column(18), 6)
        self.assertEqual(ui._get_visual_column(23), 11)
        # Invalid
        self.assertEqual(ui._get_visual_column(24), -1)

    def test_get_point_center(self):
        # Test a few points to ensure coordinates are within screen bounds
        x, y = ui.get_point_center(0)
        self.assertTrue(ui.BOARD_X < x < ui.WIDTH)
        self.assertTrue(ui.HEIGHT/2 < y < ui.HEIGHT) # Bottom half

        x, y = ui.get_point_center(12)
        self.assertTrue(ui.BOARD_X < x < ui.WIDTH)
        self.assertTrue(0 < y < ui.HEIGHT/2) # Top half

    def test_get_point_rect(self):
        rect = ui.get_point_rect(5)
        self.assertIsInstance(rect, pygame.Rect)
        self.assertTrue(rect.width > 0)
        self.assertTrue(rect.height > 0)

    @patch('pygame_ui.ui.get_point_rect')
    def test_get_point_from_pos(self, mock_get_point_rect):
        # Mock the rects for points 0 and 1
        mock_get_point_rect.side_effect = lambda i: {
            0: pygame.Rect(300, 400, 50, 300),
            1: pygame.Rect(350, 400, 50, 300)
        }.get(i, pygame.Rect(0,0,0,0))

        # Test hitting point 0
        self.assertEqual(ui.get_point_from_pos((325, 500)), 0)
        # Test hitting point 1
        self.assertEqual(ui.get_point_from_pos((375, 500)), 1)
        # Test missing all points
        self.assertIsNone(ui.get_point_from_pos((10, 10)))

        # Test bar
        bar_x = ui.BOARD_X + ui.MARGIN + 6 * ui.POINT_WIDTH + 10
        self.assertEqual(ui.get_point_from_pos((bar_x, 300)), "bar")
        
        # Test bear-off
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
