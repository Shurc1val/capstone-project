from random import randint

def validate_user_input(msg, options):
    while True:
        user_input = input(msg)
        if user_input in options:
            return user_input
        print("Not a valid entry!\n")

def roll_die():
    return randint(1,6)

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
""".format(*spaces[::-1][13:21], spaces[15], spaces[6], spaces[16], spaces[5], spaces[17],spaces[4], spaces[18], spaces[3], spaces[19], spaces[2], spaces[20], spaces[1], *spaces[21:28], spaces[0], ",".join(finished_tokens))
    print(board_graphics)

board = [[] for i in range(28)]
finished_tokens = []
possible_colours = ["Blue","Green","Red","White"]
user_num_to_index = {"s1":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"s2":7,"7":8,"8":9,"9":10,"10":11,"11":12,"12":13,"s3":14,"13":15,"14":16,"15":17,"16":18,"17":19,"18":20,"s4":21,"19":22,"20":23,"21":24,"22":25,"23":26,"24":27}
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

while not max([finished_tokens.count(colour[0]) for colour in players]) == num_tokens:
    print("\n{} player turn".format(players[turn_counter-1]))
    input("Press any [enter] to roll the die: ")
    die_roll = roll_die()
    print(die_roll)
    while True:
        move_possible = False
        for i in range(0,28):
            if validate_move(i,die_roll,players[turn_counter-1][0]):
                move_possible = True
        if move_possible:
            current_index = user_num_to_index[validate_user_input("Which piece would you like to move? (enter place name) ", user_num_to_index.keys())]
            if validate_move(current_index,die_roll,players[turn_counter-1][0]):
                move_piece(current_index,die_roll,players[turn_counter-1][0])
                break
            print("Not a valid move")
        else:
            print("No moves possible!!")
            input("(press [enter] to continue)")
            break
    print_board(board)
    turn_counter = (turn_counter + 1) % num_players

print(f"Congratulations {players[turn_counter-1]} player, you win!!")
