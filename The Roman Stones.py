from random import randint

def validate_user_input(msg, options):
    while True:
        user_input = input(msg)
        if user_input in options:
            return user_input
        print("Not a valid entry!\n")

def roll_die():
    return randint(1,6)

def move_piece(current_index, num, colour):
    if board[current_index].count(colour) == 0:
        return False
    for place in board[current_index+1:current_index+num]:
        if len(place) > 1 and place.count(colour) != len(place):
            return False
    if current_index + num > 28:
        return False
    board[current_index].remove(colour)
    if current_index + num == 28:
        finished_tokens.append(colour)
    else:
        board[current_index + num].append(colour)
    for i in range(current_index+1,current_index+num):
        if board[i] and i not in (7,14,21):
            for piece in board[i]:
                if piece != colour:
                    board[i].remove(piece)
                    board[0].append(piece)
    #Might cause errors at end of board
    return True

def print_board(board):
    spaces = []
    for place in board:
        if place:
            spaces.append(int((6-len(place))/2)*" " + "".join(place) + (6-len(place)-int((6-len(place))/2))*" ")
        else:
            spaces.append(6*" ")
    board_graphics = """
       (s)     12     11     10      9      8      7     (s)
      _______________________________________________________
 (s) |      |      |      |      |      |      |      |      | (s)
     |{}|{}|{}|{}|{}|{}|{}|{}|
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
 (s) |{}|{}|{}|{}|{}|{}|{}|{}| (s)
     |______|______|______|______|______|______|______|______|

       (s)     19     20     21     22     23     24    (s)
""".format(*spaces[::-1][13:21], spaces[15], spaces[6], spaces[16], spaces[5], spaces[17],spaces[4], spaces[18], spaces[3], spaces[19], spaces[2], spaces[20], spaces[1], *spaces[21:28], spaces[0])
    print(board_graphics)

board = [[] for i in range(28)]
finished_tokens = []
possible_colours = ["Blue","Green","Red","White"]
players = []
turn_counter = 1

num_players = int(validate_user_input("Please enter the number of players (2-4): ", "234"))
num_tokens = int(validate_user_input("How many tokens should each player have? (1-3) ", "123"))

for i in range(1,num_players + 1):
    player_colour = validate_user_input(f"Player {i}, what colour do you want to be? ({', '.join(possible_colours)}) ", possible_colours)
    players.append(player_colour)
    possible_colours.remove(player_colour)
    for i in range(num_tokens):
        board[0].append(player_colour[0])

print_board(board)

while not max([finished_tokens.count(colour) for colour in players]) == num_tokens:
    print("\n{} player turn".format(players[turn_counter-1]))
    input("Press any key to roll the die: ")
    die_roll = roll_die()
    print(die_roll)
    while True:
        current_index = int(input("Which piece would you like to move? "))
        if move_piece(current_index,die_roll,players[turn_counter-1][0]):
            break
        print("Not a valid move")
    print_board(board)
    turn_counter = (turn_counter + 1) % num_players


    continue

