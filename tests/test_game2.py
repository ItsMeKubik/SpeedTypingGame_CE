import pytest
from unittest.mock import patch, mock_open, call
import builtins
import game
import os

# Test clear_terminal (just check it calls os.system correctly)
@patch("os.system")
def test_clear_terminal(mock_os_system):
    game.clear_terminal()
    mock_os_system.assert_called_once_with('cls' if os.name == 'nt' else 'clear')

# Test countdown with patching sleep and print
@patch("time.sleep", return_value=None)
@patch("builtins.print")
def test_countdown(mock_print, _):
    game.countdown(3)
    expected_calls = [call(f"\x1b[33mStarting in {i}...\x1b[0m") for i in range(3, 0, -1)]
    mock_print.assert_has_calls(expected_calls, any_order=False)

# Test simulate_opponent_progress
@patch("time.sleep", return_value=None)
@patch("builtins.print")
def test_simulate_opponent_progress(mock_print, _):
    game.simulate_opponent_progress(30)
    assert call("Opponent has finished typing, his wpm is 30 WPM. Can you beat it?") in mock_print.mock_calls

# Test count_words_per_minute for mode 2 (returns WPM)
@patch("game.clear_terminal")
@patch("time.sleep", return_value=None)
def test_count_words_per_minute_mode_2(_, __):
    time_start = (game.time.time() - 30) / 60  # simulate 30 seconds ago
    wpm = game.count_words_per_minute(time_start, mode=2, correct_words=15)
    assert isinstance(wpm, float)

# Test load_words with mock file
@patch("builtins.open", new_callable=mock_open, read_data="word1,word2,word3")
def test_load_words(mock_file):
    words = game.load_words()
    assert set(words) == {"word1", "word2", "word3"}
    mock_file.assert_called_once_with("words_to_play.txt")

# Test difficulty_chooser with input "1"
@patch("builtins.input", return_value="1")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_difficulty_chooser_easy(_, __, ___):
    with patch("random.randint", return_value=15):
        result = game.difficulty_chooser()
        assert result == 15

# Test difficulty_chooser with invalid input
@patch("builtins.input", return_value="invalid")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_difficulty_chooser_invalid(_, __, ___):
    with patch("random.randint", return_value=30):
        result = game.difficulty_chooser()
        assert result == 30  # defaults to medium

# Test mode_selector with valid inputs
@patch("game.words_per_minute_mode")
@patch("game.vs_opponent")
@patch("game.clear_terminal")
@patch("time.sleep", return_value=None)
def test_mode_selector_valid(mock_sleep, mock_clear, mock_vs_opponent, mock_wpm_mode):
    game.mode_selector(1)
    mock_wpm_mode.assert_called_once()
    game.mode_selector(2)
    mock_vs_opponent.assert_called_once()

# Test mode_selector with invalid input
@patch("game.start_menu")
@patch("game.clear_terminal")
@patch("time.sleep", return_value=None)
@patch("builtins.print")
def test_mode_selector_invalid(mock_print, _, __, mock_start):
    game.mode_selector(99)
    mock_start.assert_called_once()

# Test start_menu with valid and invalid input
@patch("game.mode_selector")
@patch("builtins.input", return_value="1")
@patch("game.clear_terminal")
def test_start_menu_valid(_, __, mock_mode_selector):
    game.start_menu()
    mock_mode_selector.assert_called_once_with(1)

@patch("game.start_menu")
@patch("builtins.input", return_value="invalid")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_start_menu_invalid(_, __, ___, mock_restart):
    game.start_menu()
    mock_restart.assert_called_once()

# Test gm function logic (light test)
#@patch("builtins.input", side_effect=lambda: "test")
#@patch("game.load_words", return_value=["test"])
#@patch("game.clear_terminal")
#@patch("time.sleep", return_value=None)
#def test_gm_mode1(_, __, ___, ____):
    #game.gm(mode=1)
