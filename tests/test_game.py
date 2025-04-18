import builtins
from unittest.mock import patch, MagicMock
from game import start_menu, countdown, mode_selector
from colorama import Fore,Style

# Test when user inputs '1'
@patch('game.input', return_value='1')
@patch('game.mode_selector')
@patch('game.clear_terminal')
@patch('game.print')  # to suppress output during test
def test_start_menu_valid_input_1(mock_print, mock_clear, mock_mode_selector, mock_input):
    start_menu()
    mock_clear.assert_called()
    mock_mode_selector.assert_called_once_with(1)

# Test when user inputs invalid data (e.g., 'abc')
@patch('game.input', side_effect=['abc', '3'])  # first input is invalid, then '3' to exit
@patch('game.mode_selector')
@patch('game.clear_terminal')
@patch('game.print')
@patch('game.time.sleep', return_value=None)
def test_start_menu_invalid_input_then_valid(mock_sleep, mock_print, mock_clear, mock_mode_selector, mock_input):
    start_menu()
    # Should call start_menu recursively, then mode_selector with 3
    assert mock_mode_selector.call_args[0][0] == 3
    assert mock_input.call_count >= 2  # because of recursion on wrong input
    mock_clear.assert_called()

@patch('game.time.sleep')
@patch('game.clear_terminal')
def test_countdown(mock_clear,mock_sleep):
    countdown(3)
    assert mock_sleep.call_args[0][0] == 1
    mock_clear.assert_called()

@patch('builtins.print')
@patch('game.words_per_minute_mode')
@patch('game.time.sleep')
@patch('game.clear_terminal')
def test_mode_selector_mode_1(mock_clear,mock_sleep,mock_wpm,mock_print):
    mode_selector(1)
    mock_print.assert_any_call(Fore.YELLOW + "Mode words per minute mode " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
    mock_sleep.assert_called()
    mock_clear.assert_called()
    mock_wpm.assert_called_once()

@patch('builtins.print')
@patch('game.vs_opponent')
@patch('game.time.sleep')
@patch('game.clear_terminal')
def test_mode_selector_mode_2(mock_clear,mock_sleep,mock_vs_opponent,mock_print):
    mode_selector(2)
    mock_print.assert_any_call(Fore.YELLOW + "Mode race against opponent " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
    mock_sleep.assert_called()
    mock_clear.assert_called()
    mock_vs_opponent.assert_called_once()

@patch('game.sys.exit')
@patch('builtins.print')
@patch('game.time.sleep')
@patch('game.clear_terminal')
def test_mode_selector_mode_3(mock_clear,mock_sleep,mock_print,sys_exit):
    mode_selector(3)
    mock_print.assert_any_call(Fore.YELLOW + "Exiting..." + Style.RESET_ALL)
    mock_sleep.assert_called()
    mock_clear.assert_called()
    sys_exit.assert_called_once_with(0)

@patch('builtins.print')
@patch('game.start_menu')
@patch('game.time.sleep')
@patch('game.clear_terminal')
def test_mode_selector_invalid(mock_clear,mock_sleep,mock_start_menu,mock_print):
    mode_selector(99)
    mock_print.assert_any_call(Fore.RED + "Wrong input! Try again! Restarting in 3 seconds..." + Style.RESET_ALL)
    mock_sleep.assert_called()
    mock_clear.assert_called()
    mock_start_menu.assert_called_once()