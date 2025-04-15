from colorama import Fore, init, Style
import time
import os

init()
start = time.time()
start_minutes = start / 60

while True:
    word = input("Zadejte slovo: ").lower()
    if word == "colors":
        end = time.time()
        print(Fore.RED + "RED")
        print(Fore.GREEN + "GREEN")
        print(Fore.YELLOW + "YELLOW" + Style.RESET_ALL)
    if word == "end":
        end = time.time() / 60
        print(Fore.RED + str(round(end - start_minutes, 1)) + Style.RESET_ALL)
        break


def start_menu():
    pass

def count_words_per_minute():
    pass

def gm():
    pass

def load_words():
    pass