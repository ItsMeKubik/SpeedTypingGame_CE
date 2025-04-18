from colorama import Fore, init, Style
import os
import random
import time
import sys

init()

"""DEFINE DIFFICULTIES.

Defines difficulty levels.
"""
EASY = random.randint(10,24)
MEDIUM = random.randint(25,39)
HARD = random.randint(40,50)

def clear_terminal():
    """
    Clears the terminal screen.
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(seconds=3):

    """
    Counts down the given number of seconds.
    """
    for i in range(seconds,0,-1):
        print(Fore.YELLOW + f"Starting in {i}..." + Style.RESET_ALL)
        time.sleep(1)
    clear_terminal()

def simulate_opponent_progress(opponent_wpm : int):
    """
    Simulates the opponent progress.

    Parameters
    ----------
    opponent_wpm: int
    """
    for i in range(4):
        print(Fore.YELLOW + "Opponent is typing...")
        time.sleep(1)
    print(f"Opponent has finished typing, his wpm is {opponent_wpm} WPM. Can you beat it?")

def count_words_per_minute(time_start,mode, correct_words : int):
    end_time = (time.time() / 60)
    final_time = end_time - time_start
    words_per_minute = (correct_words / final_time)
    print(Fore.YELLOW + "GAME OVER! Counting words per minute..." + Style.RESET_ALL)
    time.sleep(2)
    clear_terminal()
    if mode == 1:
        print(Fore.YELLOW + "Your typing speed is: " + Fore.GREEN + str(round(words_per_minute,1)) + Fore.YELLOW + " Words per minute" + Style.RESET_ALL)
    elif mode == 2:
        return round(words_per_minute,1)

def load_words():
    with open("words_to_play.txt") as f:
        words = f.read().split(",")
    random.shuffle(words)
    return words

def words_per_minute_mode():
    input(Style.RESET_ALL + "Press ENTER to start...")
    clear_terminal()
    countdown()
    gm(1)

def difficulty_chooser():
    print(Fore.YELLOW + "Please select difficulty (1,2,3)" + Style.RESET_ALL)
    print("1.Easy\n2.Medium\n3.Hard")
    difficulty = input()
    opponent_wpm = MEDIUM
    if difficulty.isdigit() and (difficulty == "1" or difficulty == "2" or difficulty == "3"):
        if difficulty == "1":
            opponent_wpm = EASY
        elif difficulty == "2":
            opponent_wpm = MEDIUM
        elif difficulty == "3":
            opponent_wpm = HARD
    else:
        print(Fore.RED + "INVALID INPUT! Defaulting to medium difficulty!" + Style.RESET_ALL)
        time.sleep(2)
        clear_terminal()
        opponent_wpm = MEDIUM
    return opponent_wpm

def vs_opponent():
    clear_terminal()
    opponent_wpm = difficulty_chooser()
    clear_terminal()
    simulate_opponent_progress(opponent_wpm)
    input(Style.RESET_ALL + "Press ENTER to start...")
    clear_terminal()
    countdown()
    gm(2,opponent_wpm)

def mode_selector(mode : int):
    if mode == 1:
        clear_terminal()
        print(Fore.YELLOW + "Mode words per minute mode " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
        time.sleep(1)
        clear_terminal()
        words_per_minute_mode()
    elif mode == 2:
        clear_terminal()
        print(Fore.YELLOW + "Mode race against opponent " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
        time.sleep(1)
        clear_terminal()
        vs_opponent()
    elif mode == 3:
        print(Fore.YELLOW + "Exiting..." + Style.RESET_ALL)
        time.sleep(1)
        clear_terminal()
        sys.exit(0)
    elif mode not in [1,2,3]:
        print(Fore.RED + "Wrong input! Try again! Restarting in 3 seconds..." + Style.RESET_ALL)
        time.sleep(3)
        clear_terminal()
        start_menu()

def start_menu():
    """
    Displays the main menu for the game and handles user input.

    The menu allows the user to choose between different game modes:
        1. Words per minute mode
        2. Race against an opponent
        3. Exit the game

    The function validates user input and either proceeds to the selected mode
    via the `mode_selector()` function or prompts the user to enter a valid choice.
    Invalid inputs will trigger an error message and reload the menu after a short delay.
    """
    clear_terminal()
    print(Fore.LIGHTCYAN_EX + "SPEED TYPING GAME\n- Prusenovský Jakub\n--------------------" + Style.RESET_ALL)
    print("Select mode")
    print("1. Words per minute mode ")
    print("2. Race against opponent ")
    print("3. Exit")
    print("-------")
    selected_mode = input("Select mode (Enter 1 or 2 or 3): ")
    if selected_mode.isdigit():
        mode_selector(int(selected_mode))
    else:
        print(Fore.RED + "Wrong input! Try again! Restarting in 3 seconds..." + Style.RESET_ALL)
        time.sleep(3)
        clear_terminal()
        start_menu()

def gm(mode : int, opponent_wpm = 0):
    """
    Runs a typing game session where the player types a sequence of words as fast and accurately as possible.

    Parameters:
    -----------
    - mode : int
        -- The game mode. If mode == 2, the player's speed is compared against an opponent's WPM to determine the result.
    - opponent_wpm : int, optional
        -- The opponent's words per minute speed, used only when mode == 2 (default is 0).

    Gameplay:
    ---------
    - A list of words is loaded for the player to type.
    - The player types each word one-by-one. Words must match exactly (case-insensitive).
    - The game tracks the time taken and the number of correct words.
    - After all words are typed, the player's WPM (words per minute) is calculated.
    - In mode 2, the player's WPM is compared against the opponent's WPM to declare a winner, loser, or draw.

    Outputs:
    --------
    - Prints game instructions and progress.
    - At the end, displays the player's speed.
    - In mode 2, displays the game result based on comparison with the opponent.
    """
    words_to_play = load_words()
    time_start = time.time() / 60
    correct_words = 0
    index = 0
    run = True
    player_wpm = 0
    words_count = 25
    while run:
        print("Type this word: " + Fore.LIGHTBLUE_EX + f"{words_to_play[index]}" +  Style.RESET_ALL + f" {index}/{words_count}")
        if input().upper() == words_to_play[index]:
            correct_words += 1
            index += 1
            clear_terminal()
        clear_terminal()
        if correct_words == words_count:
            run = False
            clear_terminal()
            player_wpm = count_words_per_minute(time_start, mode, correct_words)

    if mode == 2:
        if player_wpm > opponent_wpm:
            print(Fore.LIGHTGREEN_EX + "Congratulations, you won!" + Style.RESET_ALL)
            print(Fore.YELLOW + "Your speed was: " + Fore.CYAN + str(player_wpm) + " Words per minute" + Style.RESET_ALL)
        elif player_wpm < opponent_wpm:
            print(Fore.LIGHTRED_EX + "GAME OVER! You lost! Better luck next time!" + Style.RESET_ALL)
            print(Fore.YELLOW + "Your speed was: " + Fore.CYAN + str(player_wpm) + " Words per minute" + Style.RESET_ALL)
        elif player_wpm == opponent_wpm:
            print(Fore.YELLOW + "Its a draw!" + Style.RESET_ALL)

if __name__ == "__main__":
    start_menu()

