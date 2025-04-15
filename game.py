from colorama import Fore, init, Style
import os,random,time

init()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_menu():

    print(Fore.LIGHTCYAN_EX + "SPEED TYPING GAME\n - Prusenovský Jakub\n --------------------" + Style.RESET_ALL)
    print("Select mode")
    print("1. Words per minute mode ")
    print("2. Race against opponent ")
    print("-------")
    selected_mode = int(input("Select mode (Enter 1 or 2): "))
    mode_selector(selected_mode)

def countdown(seconds=3):
    for i in range(seconds,0,-1):
        print(Fore.YELLOW + "Starting in {}...".format(i) + Style.RESET_ALL)
        time.sleep(1)
    clear_terminal()

def simulate_opponent_progress(opponent_wpm : int):
    for i in range(5):
        print(Fore.YELLOW + "Opponent is typing...")
        time.sleep(1)
    print("Opponent has finished typing, his wpm is {} WPM.".format(opponent_wpm) + " Can you beat it?")

def count_words_per_minute(time_start,mode, correct_words : int) :
    words_per_minute = (correct_words / ((time.time() / 60) - time_start))
    print(Fore.YELLOW + "GAME OVER! Counting words per minute..." + Style.RESET_ALL)
    time.sleep(2)
    clear_terminal()
    if mode == 1:
        print(Fore.YELLOW + "Your typing speed is: " + Fore.GREEN + str(round(words_per_minute,1)) + Fore.YELLOW + " Words per minute" + Style.RESET_ALL)
    elif mode == 2:
        return words_per_minute

def load_words():
    with open("words_to_play.txt") as f:
        words = f.read().split(",")
    random.shuffle(words)
    return words

def words_per_minute_mode(words_to_play):
    correct_words = 0
    index = 0
    run = True
    mode = 1

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
            count_words_per_minute(time_start,mode, correct_words)

def vs_opponent(words_to_play,difficulty: int):
    correct_words = 0
    index = 0
    run = True
    mode = 2
    clear_terminal()
    if difficulty == 1:
        opponent_wpm = random.randint(20,30)
    elif difficulty == 2:
        opponent_wpm = random.randint(31,45)
    elif difficulty == 3:
        opponent_wpm = random.randint(46,60)
    else:
        print(Fore.RED + "INVALID INPUT! Defaulting to medium difficulty!" + Style.RESET_ALL)
        opponent_wpm = random.randint(31,45)
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
    elif player_wpm < opponent_wpm:
        print(Fore.RED + "GAME OVER! You lost! Better luck next time!" + Style.RESET_ALL)
    elif player_wpm == opponent_wpm:
        print(Fore.YELLOW + "Its a draw!" + Style.RESET_ALL)


def mode_selector(mode : int):
    words_to_play = load_words()
    if mode == 1:
        clear_terminal()
        print(Fore.YELLOW + "Mode words per minute mode " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
        time.sleep(1)
        clear_terminal()
        words_per_minute_mode(words_to_play)
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

start_menu()

