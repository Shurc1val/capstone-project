from random import randint
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font

from userproof_inputs import ask_user_for_number, ask_user_for_specific_inputs
import trs_graphics


def main():

    finished_tokens = []
    possible_colours = ["Blue", "Green", "Red", "Purple", "Gold"]
    players = []
    turn_counter = 1

    window = Tk()

    window.title('The Roman Stones')
    window.geometry("720x800+10+20")
    window.configure(bg="black")

    game_settings = {'colours': [], 'board': [[]
                                              for i in range(28)], 'die_roll': 0, 'finished_tokens': []}
    trs_graphics.new_game_pop_up_players_and_tokens(window, game_settings)

    trs_graphics.new_game_pop_up_colours(window, game_settings, possible_colours)
    trs_graphics.draw_board(window, game_settings)

    window.mainloop()


def find_counter_on_board(counter_ID: int, board: list[list[int]]) -> int:
    for i in range(len(board)):
        if counter_ID in board[i]:
            return i
    return 28


if __name__ == "__main__":
    main()
