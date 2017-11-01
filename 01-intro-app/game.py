import os
import random
import time
import sys
import colorama


class Game:
    def __init__(self):
        self.history = []  # empty list where the colours within each game will be saved
        self.plays = [
            (colorama.Fore.RED + 'Red', 'r'),
            (colorama.Fore.YELLOW + 'Yellow', 'y'),
            (colorama.Fore.GREEN + 'Green', 'g'),
            (colorama.Fore.BLUE + 'Blue', 'b')
        ]  # List om tuples, tuples enables us to enter multiple values for each possible play

    def show_level(self):
        self.clear()
        for h in self.history:
            print(h[0], end='  ')  # print each colour that the user needs to remember, with two spaces between
            sys.stdout.flush()
            time.sleep(1)  # This will add a delay between each colour displayed to the user

        self.clear()  # Clears the screen, now we need to test the player

    def add_move(self):
        self.history.append(random.choice(self.plays))  # Randomly selects a colour from "plays"-list

    def test_player(self):
        print(colorama.Fore.WHITE + "{} moves:".format(len(self.history)))
        for t, v in self.history:
            guess = input("Next [r,g,b,y]: ")
            if guess != v:
                return False

        return True

    def clear(self):
        os.system('clear')
