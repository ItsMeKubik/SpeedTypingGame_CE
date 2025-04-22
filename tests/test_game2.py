import pytest
from unittest.mock import patch, mock_open, call
import builtins
import game
import os
from colorama import Fore,Style

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

@patch("game.input", return_value="")  # Simulates pressing ENTER
@patch("game.gm")
@patch("game.countdown")
@patch("game.clear_terminal")
def test_words_per_minute_mode(mock_clear, mock_countdown, mock_gm, mock_input):
    game.words_per_minute_mode()
    mock_input.assert_called_once()
    mock_clear.assert_called_once()
    mock_countdown.assert_called_once()
    mock_gm.assert_called_once_with(1)

@patch("game.input", return_value="")
@patch("game.gm")
@patch("game.countdown")
@patch("game.clear_terminal")
@patch("game.simulate_opponent_progress")
@patch("game.difficulty_chooser", return_value=50)
def test_vs_opponent(mock_diff, mock_sim, mock_clear, mock_countdown, mock_gm, mock_input):
    game.vs_opponent()
    assert mock_clear.call_count >= 2  # Called multiple times
    mock_diff.assert_called_once()
    mock_sim.assert_called_once_with(50)
    mock_input.assert_called_once()
    mock_countdown.assert_called_once()
    mock_gm.assert_called_once_with(2, 50)

# Test simulate_opponent_progress
@patch("time.sleep", return_value=None)
@patch("builtins.print")
def test_simulate_opponent_progress(mock_print, _):
    game.simulate_opponent_progress(30)
    assert call("Opponent has finished typing, his wpm is 30 WPM. Can you beat it?") in mock_print.mock_calls

# Test count_words_per_minute for mode 1 (returns WPM)
@patch("builtins.print")
@patch("game.clear_terminal")
@patch("time.sleep", return_value=None)
def test_count_words_per_minute_mode_1(_, __,mock_print):
    time_start = (game.time.time() - 30) / 60  # simulate 30 seconds ago
    wpm = game.count_words_per_minute(time_start, mode=1, correct_words=15)
    assert call(Fore.YELLOW + "Your typing speed is: " + Fore.GREEN + str(wpm) + Fore.YELLOW + " Words per minute" + Style.RESET_ALL)

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
    mock_file.assert_called_once_with("Assets/words_to_play.txt")

# Test difficulty_chooser with input "1"
@patch("builtins.input", return_value="1")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_difficulty_chooser_easy(_, __, ___):
    with patch("random.randint", return_value=15):
        result = game.difficulty_chooser()
        assert result == 15

# Test difficulty_chooser with input "2"
@patch("builtins.input", return_value="2")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_difficulty_chooser_medium(_, __, ___):
    with patch("random.randint", return_value=30):
        result = game.difficulty_chooser()
        assert result == 30

# Test difficulty_chooser with input "3"
@patch("builtins.input", return_value="3")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_difficulty_chooser_hard(_, __, ___):
    with patch("random.randint", return_value=45):
        result = game.difficulty_chooser()
        assert result == 45

# Test difficulty_chooser with invalid input
@patch("builtins.input", return_value="invalid")
@patch("time.sleep", return_value=None)
@patch("game.clear_terminal")
def test_difficulty_chooser_invalid(_, __, ___):
    with patch("random.randint", return_value=30):
        result = game.difficulty_chooser()
        assert result == 30  # defaults to medium

# Test mode_selector with valid inputs
@patch("sys.exit")
@patch("game.words_per_minute_mode")
@patch("game.vs_opponent")
@patch("game.clear_terminal")
@patch("time.sleep", return_value=None)
def test_mode_selector_valid(mock_sleep, mock_clear, mock_vs_opponent, mock_wpm_mode,mock_exit):
    game.mode_selector(1)
    mock_wpm_mode.assert_called_once()
    game.mode_selector(2)
    mock_vs_opponent.assert_called_once()
    game.mode_selector(3)
    mock_exit.assert_called_once()


# Test mode_selector with invalid input
@patch("game.start_menu")
@patch("game.clear_terminal")
@patch("time.sleep", return_value=None)
@patch("builtins.print")
def test_mode_selector_invalid(mock_print, _, __, mock_start):
    game.mode_selector(99)
    mock_start.assert_called_once()

# Test valid mode selection (e.g. '1')
@patch("game.clear_terminal")
@patch("game.mode_selector")
@patch("game.input", return_value="1")
def test_start_menu_valid_input(mock_input, mock_mode_selector, mock_clear):
    game.start_menu()
    mock_mode_selector.assert_called_once_with(1)
    mock_clear.assert_called()

# Test invalid input (non-digit), should retry
@patch("game.clear_terminal")
@patch("game.input", side_effect=["abc","3"])
@patch("game.mode_selector")
@patch("game.time.sleep")
def test_start_menu_invalid_then_valid(mock_sleep, mock_mode_selector, mock_input, mock_clear):
    game.start_menu()
    assert mock_input.call_count == 2  # Tried twice
    mock_mode_selector.assert_called_once_with(3)
    mock_sleep.assert_called_once()

@patch("game.clear_terminal")
@patch("game.count_words_per_minute", return_value=70)
@patch("game.load_words", return_value=["HELLO"] * 25)
@patch("game.input", side_effect=["hello"] * 25)
@patch("game.time.time", return_value=600.0)  # Simulated start time
def test_gm_mode_1(mock_time, mock_input, mock_load, mock_count, mock_clear):
    game.gm(mode=1)
    assert mock_input.call_count == 25
    mock_load.assert_called_once()
    mock_count.assert_called_once_with(10.0, 1, 25)  # 600.0 / 60 = 10.0 start
    assert mock_clear.call_count > 0

@patch("game.clear_terminal")
@patch("game.count_words_per_minute", return_value=70)
@patch("game.load_words", return_value=["HELLO"] * 25)
@patch("game.input", side_effect=["hello"] * 25)
@patch("game.time.time", return_value=600.0)
def test_gm_mode_2_win(mock_time, mock_input, mock_load, mock_count, mock_clear):
    game.gm(mode=2, opponent_wpm=50)
    mock_count.assert_called_once_with(10.0, 2, 25)  # Same as before
    assert mock_input.call_count == 25

@patch("game.clear_terminal")
@patch("game.count_words_per_minute", return_value=50)
@patch("game.load_words", return_value=["HELLO"] * 25)
@patch("game.input", side_effect=["hello"] * 25)
@patch("game.time.time", return_value=600.0)
def test_gm_mode_2_draw(mock_time, mock_input, mock_load, mock_count, mock_clear):
    game.gm(mode=2, opponent_wpm=50)

@patch("game.clear_terminal")
@patch("game.count_words_per_minute", return_value=40)
@patch("game.load_words", return_value=["HELLO"] * 25)
@patch("game.input", side_effect=["hello"] * 25)
@patch("game.time.time", return_value=600.0)
def test_gm_mode_2_lose(mock_time, mock_input, mock_load, mock_count, mock_clear):
    game.gm(mode=2, opponent_wpm=50)
