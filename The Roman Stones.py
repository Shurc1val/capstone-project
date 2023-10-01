from random import randint
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font

from userproof_inputs import ask_user_for_number, ask_user_for_specific_inputs
from testing_PIL_graphics import *


def main():

    board = [[] for i in range(28)]
    finished_tokens = []
    possible_colours = ["Blue", "Green", "Red", "Purple"]
    players = []
    turn_counter = 1

    window = Tk()

    window.title('The Roman Stones')
    window.geometry("720x800+10+20")
    window.configure(bg="black")

    game_settings = {"colours": []}
    new_game_pop_up_players_and_tokens(window, game_settings)

    new_game_pop_up_colours(window, game_settings, possible_colours)
    print(game_settings)

    draw_board(window, game_settings['colours'], game_settings['num_counters'])

    window.mainloop()

    """while not max([finished_tokens.count(colour[0]) for colour in players]) == num_counters:
        print("\n{} player turn".format(players[turn_counter-1]))
        input("Press any [enter] to roll the die: ")
        die_roll = roll_die()
        print(die_roll)
        while True:
            move_possible = False
            for i in range(0, 28):
                if validate_move(i, die_roll, players[turn_counter-1][0]):
                    move_possible = True
            if move_possible:
                current_index = user_num_to_index[ask_user_for_specific_inputs(
                    "Which piece would you like to move? (enter place name) ", user_num_to_index.keys())]
                if validate_move(current_index, die_roll, players[turn_counter-1][0]):
                    move_piece(current_index, die_roll,
                               players[turn_counter-1][0])
                    break
                print("Not a valid move")
            else:
                print("No moves possible!!")
                input("(press [enter] to continue)")
                break
        print_board(board)
        turn_counter = (turn_counter + 1) % num_players

    print(f"Congratulations {players[turn_counter-1]} player, you win!!")"""


def roll_die():
    return randint(1, 6)


def validate_move(current_index, num, colour):
    if board[current_index].count(colour) == 0:
        return False
    for place in board[current_index+1:current_index+num]:
        if len(place) > 1 and place.count(colour) != len(place):
            return False
    if current_index + num > 28:
        return False
    return True


def move_piece(current_index, num, colour):
    board[current_index].remove(colour)
    if current_index + num == 28:
        finished_tokens.append(colour)
    else:
        board[current_index + num].append(colour)
    for i in range(current_index+1, current_index+num):
        if board[i] and i not in (7, 14, 21):
            for piece in board[i]:
                if piece != colour:
                    board[i].remove(piece)
                    board[0].append(piece)
    # Might cause errors at end of board
    return True


def print_board(board):
    spaces = []
    for place in board:
        if place:
            spaces.append(int((6-len(place))/2)*" " + "".join(place) +
                          (6-len(place)-int((6-len(place))/2))*" ")
        else:
            spaces.append(6*" ")
    board_graphics = """
       (s3)     12     11     10      9      8      7    (s2)
      _______________________________________________________
     |      |      |      |      |      |      |      |      | 
(s3) |{}|{}|{}|{}|{}|{}|{}|{}| (s2)
     |______|______|______|______|______|______|______|______|
     |      |                                         |      |    
  13 |{}|                                         |{}|  6
     |______|                                         |______| 
     |      |                                         |      |    
  14 |{}|                                         |{}|  5
     |______|                                         |______| 
     |      |                                         |      |    
  15 |{}|                                         |{}|  4
     |______|                                         |______| 
     |      |                                         |      |    
  16 |{}|                                         |{}|  3
     |______|                                         |______| 
     |      |                                         |      |    
  17 |{}|                                         |{}|  2
     |______|                                         |______| 
     |      |                                         |      |    
  18 |{}|                                         |{}|  1
     |______|_________________________________________|______|
     |      |      |      |      |      |      |      |      |     
(s4) |{}|{}|{}|{}|{}|{}|{}|{}| (s1)       Off-board: {}
     |______|______|______|______|______|______|______|______|

       (s4)    19     20     21     22     23     24    (s1)
""".format(*spaces[::-1][13:21], spaces[15], spaces[6], spaces[16], spaces[5], spaces[17], spaces[4], spaces[18], spaces[3], spaces[19], spaces[2], spaces[20], spaces[1], *spaces[21:28], spaces[0], ",".join(finished_tokens))
    print(board_graphics)


if __name__ == "__main__":
    main()
