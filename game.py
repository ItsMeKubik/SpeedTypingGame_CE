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
    gm(selected_mode)

def countdown(seconds=3):
    for i in range(seconds,0,-1):
        print(Fore.YELLOW + "Starting in {}...".format(i) + Style.RESET_ALL)
        time.sleep(1)
    clear_terminal()

def count_words_per_minute(time_start, correct_words : int) :
    print(Fore.YELLOW + "GAME OVER! Counting words per minute..." + Style.RESET_ALL)
    words_per_minute = (correct_words / ((time.time() / 60) - time_start))
    time.sleep(2)
    clear_terminal()
    print(Fore.YELLOW + "Your typing speed is: " + Fore.GREEN + str(round(words_per_minute,1)) + Fore.YELLOW + " Words per minute" + Style.RESET_ALL)

def load_words():
    with open("words_to_play.txt") as f:
        words = f.read().split(",")
    random.shuffle(words)
    return words

def words_per_minute_mode(words_to_play):
    correct_words = 0
    index = 0
    run = True
    input("Press ENTER to start...")
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
        if correct_words == 25:
            run = False
            clear_terminal()
            count_words_per_minute(time_start, correct_words)

def gm(mode : int):
    words_to_play = load_words()
    if mode == 1:
        clear_terminal()
        print(Fore.YELLOW + "Mode words per minute mode " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
        time.sleep(2)
        clear_terminal()
        words_per_minute_mode(words_to_play)
    elif mode == 2:
        clear_terminal()
        print(Fore.YELLOW + "Mode race against opponent " + Fore.GREEN + "ENABLED" + Style.RESET_ALL)
    elif mode != 1 or mode !=2:
        print(Fore.RED + "Wrong input! Try again! Restarting in 3 seconds..." + Style.RESET_ALL)
        time.sleep(3)
        clear_terminal()
        start_menu()


start_menu()