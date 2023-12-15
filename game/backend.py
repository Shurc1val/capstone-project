from random import randint
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font

import trs_graphics


POSSIBLE_COLOURS = ["Blue", "Green", "Red", "Purple", "Gold"]


def main():

    window = Tk()
    window.title('The Roman Stones')
    window.geometry("720x800+10+20")
    window.configure(bg="black")

    trs_graphics.new_game_pop_up_players_and_tokens(window)

    trs_graphics.new_game_pop_up_colours(window)

    trs_graphics.initiate_board(window)

    window.mainloop()


def find_counter_on_board(counter_ID: int, board: list[list[int]]) -> int:
    """Function to find the index of the square on board with the given counter id in it."""
    for i in range(len(board)):
        if counter_ID in board[i]:
            return i
    return 28


if __name__ == "__main__":
    main()
