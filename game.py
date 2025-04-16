from colorama import Fore, init, Style
import os,random,time

init()

#DEFINE DIFFICULTIES
EASY = random.randint(20,30)
MEDIUM = random.randint(31,45)
HARD = random.randint(46,60)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(seconds=3):
    for i in range(seconds,0,-1):
        print(Fore.YELLOW + "Starting in {}...".format(i) + Style.RESET_ALL)
        time.sleep(1)
    clear_terminal()

def simulate_opponent_progress(opponent_wpm : int):
    for i in range(4):
        print(Fore.YELLOW + "Opponent is typing...")
        time.sleep(1)
    print("Opponent has finished typing, his wpm is {} WPM.".format(opponent_wpm) + " Can you beat it?")

def count_words_per_minute(time_start,mode, correct_words : int):
    end_time = (time.time() / 60)
    final_time = end_time - time_start
    words_per_minute = (correct_words / final_time)
    print(Fore.YELLOW + "GAME OVER! Counting words per minute..." + Style.RESET_ALL)
    time.sleep(2)
    clear_terminal()
    if mode == 1:
        print(Fore.YELLOW + "Your typing speed is: " + Fore.GREEN + str(round(words_per_minute,1)) + Fore.YELLOW + " Words per minute" + Style.RESET_ALL)
        print(correct_words)
        print(final_time)
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

def difficulty_chooser(difficulty):
    if difficulty == 1:
        opponent_wpm = EASY
    elif difficulty == 2:
        opponent_wpm = MEDIUM
    elif difficulty == 3:
        opponent_wpm = HARD
    else:
        print(Fore.RED + "INVALID INPUT! Defaulting to medium difficulty!" + Style.RESET_ALL)
        time.sleep(2)
        clear_terminal()
        opponent_wpm = MEDIUM
    return opponent_wpm

def vs_opponent(words_to_play,difficulty: int):
    correct_words = 0
    index = 0
    run = True
    mode = 2
    clear_terminal()
    opponent_wpm = difficulty_chooser(difficulty)
    simulate_opponent_progress(opponent_wpm)
    input(Style.RESET_ALL + "Press ENTER to start...")
    clear_terminal()
    countdown()
    time_start = time.time() / 60
    while run:
        print("Type this word: " + Fore.LIGHTBLUE_EX + "{}".format(words_to_play[index]) + Style.RESET_ALL)
        if input().upper() == words_to_play[index]:
            correct_words += 1
            index += 1
            clear_terminal()
        clear_terminal()
        if correct_words == 5:
            run = False
            clear_terminal()
            player_wpm = count_words_per_minute(time_start,mode,correct_words)

    if player_wpm > opponent_wpm:
        print(Fore.LIGHTGREEN_EX + "Congratulations, you won!" + Style.RESET_ALL)
        print(player_wpm)
    elif player_wpm < opponent_wpm:
        print(Fore.LIGHTRED_EX + "GAME OVER! You lost! Better luck next time!" + Style.RESET_ALL)
        print(player_wpm)
    elif player_wpm == opponent_wpm:
        print(Fore.YELLOW + "Its a draw!" + Style.RESET_ALL)


def mode_selector(mode : int):
    words_to_play = load_words()
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
        print(Fore.YELLOW + "Please select difficulty (1,2,3)" + Style.RESET_ALL)
        print("1.Easy\n2.Medium\n3.Hard")
        difficulty = input()
        vs_opponent(words_to_play,int(difficulty))
    elif mode != 1 or mode !=2:
        print(Fore.RED + "Wrong input! Try again! Restarting in 3 seconds..." + Style.RESET_ALL)
        time.sleep(3)
        clear_terminal()
        start_menu()

def start_menu():
    print(Fore.LIGHTCYAN_EX + "SPEED TYPING GAME\n- Prusenovský Jakub\n--------------------" + Style.RESET_ALL)
    print("Select mode")
    print("1. Words per minute mode ")
    print("2. Race against opponent ")
    print("-------")
    selected_mode = input("Select mode (Enter 1 or 2): ")
    if selected_mode.isdigit():
        mode_selector(int(selected_mode))
    else:
        print(Fore.RED + "Wrong input! Try again! Restarting in 3 seconds..." + Style.RESET_ALL)
        time.sleep(3)
        clear_terminal()
        start_menu()

def gm(mode : int):
    words_to_play = load_words()
    time_start = time.time() / 60
    correct_words = 0
    index = 0
    run = True
    while run:
        print("Type this word: " + Fore.LIGHTBLUE_EX + "{}".format(words_to_play[index]) + Style.RESET_ALL)
        if input().upper() == words_to_play[index]:
            correct_words += 1
            index += 1
            clear_terminal()
        clear_terminal()
        if correct_words == 5:
            run = False
            clear_terminal()
            player_wpm = count_words_per_minute(time_start, mode, correct_words)

start_menu()

