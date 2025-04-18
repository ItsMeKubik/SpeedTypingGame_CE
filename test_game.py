import unittest, sys
from unittest.mock import patch, MagicMock
import builtins

from game import start_menu, mode_selector

class TestStartMenu(unittest.TestCase):

    @patch("builtins.input", return_value="1")
    @patch("game.mode_selector")
    @patch("game.clear_terminal")
    def test_valid_input_1(self, mock_clear, mock_mode_selector, mock_input):
        start_menu()
        mock_mode_selector.assert_called_once_with(1)
        mock_clear.assert_called_once()

    @patch("builtins.input", return_value="2")
    @patch("game.mode_selector")
    @patch("game.clear_terminal")
    def test_valid_input_2(self, mock_clear, mock_mode_selector, mock_input):
        start_menu()
        mock_mode_selector.assert_called_once_with(2)
        mock_clear.assert_called_once()

    @patch("builtins.input", return_value="abc")
    @patch("game.start_menu")  # Mock recursive call
    @patch("game.clear_terminal")
    @patch("game.time.sleep")
    def test_invalid_input(self, mock_sleep, mock_clear, mock_start_menu, mock_input):
        start_menu()
        mock_input.assert_called()
        mock_sleep.assert_called_once_with(3)
        mock_start_menu.assert_called_once()
        mock_clear.assert_called()


class TestModeSelector(unittest.TestCase):
    @patch("game.words_per_minute_mode")
    @patch("game.clear_terminal")
    @patch("game.time.sleep")
    def test_mode_1(self, mock_sleep, mock_clear, mock_words_mode):
        mode_selector(1)
        mock_words_mode.assert_called_once()
        mock_clear.assert_called()
        mock_sleep.assert_called()

    @patch("game.vs_opponent")
    @patch("game.clear_terminal")
    @patch("game.time.sleep")
    def test_mode_2(self, mock_sleep, mock_clear, mock_vs_opponent):
        mode_selector(2)
        mock_vs_opponent.assert_called_once()
        mock_clear.assert_called()
        mock_sleep.assert_called()

    @patch("game.clear_terminal")
    @patch("game.time.sleep")
    @patch("sys.exit")
    def test_mode_3(self, mock_exit, mock_sleep, mock_clear):
        mode_selector(3)
        mock_exit.assert_called_once()
        mock_clear.assert_called()
        mock_sleep.assert_called()

    @patch("game.start_menu")
    @patch("game.clear_terminal")
    @patch("game.time.sleep")
    def test_invalid_mode(self, mock_sleep, mock_clear, mock_start_menu):
        mode_selector(5)  # Any invalid mode
        mock_start_menu.assert_called_once()
        mock_clear.assert_called()
        mock_sleep.assert_called_with(3)

if __name__ == "__main__":
    unittest.main()