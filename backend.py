from random import randint
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font

from userproof_inputs import ask_user_for_number, ask_user_for_specific_inputs
import trs_graphics


POSSIBLE_COLOURS = ["Blue", "Green", "Red", "Purple", "Gold"]


class Game():

    def __init__(self) -> None:
        self.number_of_players = 0
        self.counters_per_player = 0
        self.board = [[] for i in range(28)]
        self.finished_tokens = []

    @property
    def total_number_of_counters(self) -> int:
        return self.number_of_players * self.counters_per_player

class Player():

    def __init__(self, colour: str) -> None:
        self.colour = colour
        self.die_roll = 0


def main():
    
    game = Game()
    players = []

    window = Tk()
    window.title('The Roman Stones')
    window.geometry("720x800+10+20")
    window.configure(bg="black")

    game_settings = {'colours': [], 'board': [[]
                                              for i in range(28)], 'die_roll': 0, 'finished_tokens': []}
    trs_graphics.new_game_pop_up_players_and_tokens(window, game)

    trs_graphics.new_game_pop_up_colours(window, game, players)

    trs_graphics.draw_board(window, game, players)

    window.mainloop()


def find_counter_on_board(counter_ID: int, board: list[list[int]]) -> int:
    """Function to find the index of the square on board with the given counter id in it."""
    for i in range(len(board)):
        if counter_ID in board[i]:
            return i
    return 28


if __name__ == "__main__":
    main()
