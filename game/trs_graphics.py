
import os
from time import sleep
import requests
from copy import deepcopy

from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
import math as m
import random as r

CANVAS = {'height': 750, 'width': 650}
BOARD_SQUARE = {'width': 70, 'spacer': 5}
NUM_SQUARES = 8
GAP_FROM_EDGE = (CANVAS['width'] - NUM_SQUARES *
                 (BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) + BOARD_SQUARE['spacer'])/2

GAP_FROM_TOP = GAP_FROM_EDGE
COUNTER_DIAMETER = 20

PLAYER = ""

POSSIBLE_COLOURS = ["Blue", "Green", "Red", "Purple", "Gold"]

GAME = {
    'id': -1,
    'ec2_url': None,
    'number_of_players': 0,
    'counters_per_player': 0,
    'board': [[] for i in range(28)],
    'finished_tokens': [],
}

PLAYERS = []


def find_counter_on_board(counter_ID: int) -> int:
    """Function to find the index of the square on board with the given counter id in it."""
    for i in range(len(GAME['board'])):
        if counter_ID in GAME['board'][i]:
            return i
    return 28


def get_num_players_and_tokens_selection(pop_up: Toplevel, num_player_menu: StringVar, num_counters_menu: StringVar):
    """Function to assign users' choice of player and counter number to board settings."""
    GAME['number_of_players'] = int(num_player_menu.get())
    GAME['counters_per_player'] = int(num_counters_menu.get())
    GAME['total_number_of_counters'] = GAME['number_of_players'] * GAME['counters_per_player']
    pop_up.destroy()
    pop_up.quit()


def new_game_pop_up_players_and_tokens(window):
    """
    Displays new game pop up window to choose number of players, tokens, and to choose colours.
    """

    pop_up = Toplevel(window, bg="white")
    pop_up.geometry("260x110")
    pop_up.title("New game")
    pop_up.attributes('-topmost', 'true')

    Label(pop_up, text="Please enter the number of players: ", font=(
        'Times'), bg="white", fg="black").place(x=10, y=10)

    num_player_menu = StringVar()
    num_player_menu.set("2")
    num_player_drop = OptionMenu(pop_up, num_player_menu, "1", "2", "3", "4", "5")
    num_player_drop.config(bg="white", fg="black")
    num_player_drop.place(x=200, y=10)

    Label(pop_up, text="Number of tokens for each player:", font=(
        'Times'), bg="white", fg="black").place(x=10, y=40)

    num_counters_menu = StringVar()
    num_counters_menu.set("3")
    num_counters_drop = OptionMenu(pop_up, num_counters_menu, "1", "2", "3")
    num_counters_drop.config(bg="white", fg="black")
    num_counters_drop.place(x=200, y=40)

    choose_colours_button = Button(pop_up, bg="white", fg="white",
                                   text="Choose Colours", command=lambda: get_num_players_and_tokens_selection(pop_up, num_player_menu, num_counters_menu))
    choose_colours_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white")
    choose_colours_button.place(x=120, y=68)

    window.mainloop()


def get_colour_selection(pop_up: Toplevel, colour_menu: Listbox):
    """Function to declare the players of the game by user's colour choice."""
    for i in colour_menu.curselection():
        PLAYERS.append({
            'colour': colour_menu.get(i),
            'die_roll': 0
        })
    pop_up.destroy()
    pop_up.quit()


def check_win(current_player_colour: str) -> bool:
    """Function to check if the given player has won the game."""
    if GAME['finished_tokens'].count(current_player_colour) == GAME['counters_per_player']:
        return True
    return False


def new_game_pop_up_colours(window):
    """Function to allow player to select the colours for the game."""

    number_words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

    pop_up = Toplevel(window, bg="white")
    pop_up.geometry("260x110")
    pop_up.title("New game")
    pop_up.attributes('-topmost', 'true')

    Label(pop_up, text=f"Please choose {number_words[GAME['number_of_players']]} colours:", font=(
        'Times'), bg="white", fg="black").place(x=10, y=10)

    colour_menu = Listbox(pop_up, selectmode=MULTIPLE,
                          width=10, height=len(POSSIBLE_COLOURS))
    
    for colour in POSSIBLE_COLOURS:
        colour_menu.insert(END, colour)

    selected_button_indices = []
    colour_menu.config(bg="white", fg="black")
    colour_menu.place(x=160, y=12)
    colour_menu.bind("<<ListboxSelect>>", lambda *args: limit_colour_selection(
        colour_menu, selected_button_indices, GAME['number_of_players']))

    play_game_button = Button(pop_up, bg="white", fg="white",
                              text="Play Game", command=lambda: get_colour_selection(pop_up, colour_menu))
    play_game_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white")
    play_game_button.place(x=25, y=40)

    window.mainloop()


def new_or_join_game_pop_up(window):
    """Function to allow player to choose whether to start a new game or join one."""

    def new_game():
        GAME['id'] = -1
        pop_up.destroy()
        pop_up.quit()

    def join_game():
        pop_up.destroy()
        pop_up.quit()

    pop_up = Toplevel(window, bg="white")
    pop_up.geometry("260x80")
    pop_up.title("Join Game")
    pop_up.attributes('-topmost', 'true')

    new_game_button = Button(pop_up, bg="white", fg="white",
                              text="New Game", command=lambda: new_game())
    new_game_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white", width=22)
    
    new_game_button.place(x=9, y=3)

    join_game_button = Button(pop_up, bg="white", fg="white",
                              text="Join Game", command=lambda: join_game())
    join_game_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white", width=22)
    
    join_game_button.place(x=9, y=36)

    window.mainloop()


def join_game_pop_up_ids(window):
    """Function to allow player to enter game id to join a game."""

    def get_game_ID():
        GAME['id'] = game_ID_field.get(1.0, "end-1c")
        pop_up.destroy()
        pop_up.quit()

    pop_up = Toplevel(window, bg="white")
    pop_up.geometry("260x80")
    pop_up.title("Join Game")
    pop_up.attributes('-topmost', 'true')

    Label(pop_up, text=f"Please enter game ID:", font=(
        'Times'), bg="white", fg="black").place(x=10, y=10)

    game_ID_field = Text(pop_up, width=16, height=1)
    game_ID_field.pack()

    game_ID_field.config(bg="white", fg="black")
    game_ID_field.place(x=130, y=12)

    join_game_button = Button(pop_up, bg="white", fg="white",
                              text="Join Game", command=lambda: get_game_ID())
    join_game_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white")
    
    join_game_button.place(x=80, y=36)

    window.mainloop()


def server_address_pop_up(window):
    """Function to allow player to enter game server to join or start a game."""

    def get_server():
        global GAME
        GAME['ec2_url'] = server_address_field.get(1.0, "end-1c")
        print(GAME['ec2_url'])
        pop_up.destroy()
        pop_up.quit()

    pop_up = Toplevel(window, bg="white")
    pop_up.geometry("260x80")
    pop_up.title("Server Details")
    pop_up.attributes('-topmost', 'true')

    Label(pop_up, text=f"Please server URL:", font=(
        'Times'), bg="white", fg="black").place(x=10, y=10)

    server_address_field = Text(pop_up, width=16, height=1)
    server_address_field.pack()

    server_address_field.config(bg="white", fg="black")
    server_address_field.place(x=130, y=12)

    add_server_button = Button(pop_up, bg="white", fg="white",
                              text="Add Server", command=lambda: get_server())
    add_server_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white")
    
    add_server_button.place(x=80, y=36)

    window.mainloop()


def limit_colour_selection(colour_menu: Listbox, previous_selection: list[int], choice_limit: int):
    for selection in list(colour_menu.curselection()):
        if selection not in previous_selection:
            previous_selection.append(selection)

    for selection in previous_selection:
        if selection not in list(colour_menu.curselection()):
            previous_selection.remove(selection)

    if len(colour_menu.curselection()) > choice_limit:
        colour_menu.select_clear(previous_selection[-1])
        previous_selection.pop()


def counter_clicked_on(canvas: Canvas, player_turn_label: Label, *args):
    """Function called when a counter is clicked on."""
    counter_id = list(canvas.find_withtag("current"))[0]
    current_index = find_counter_on_board(counter_id)
    
    if PLAYERS[0]['colour'] != get_counter_colour_from_id(canvas, counter_id):
        # Player clicked on wrong counter colour
        return None
    if PLAYERS[0]['die_roll'] == 0:
        # Die has not yet been rolled
        return None
    
    if validate_move(canvas, current_index, PLAYERS[0]):
        # Move is valid
        move_piece(canvas, PLAYERS[0],
                   list(canvas.find_withtag("current"))[0], current_index)
        if check_win(PLAYERS[0]['colour']):
            pop_up_message(title="Winner!",
                           message=f"Congratulations {PLAYERS[0]['colour']} player,\nyou've won!!!", button_text="Okay")
        next_player_turn(canvas, player_turn_label)
        update_server()


def pop_up_message(title: str, message: str, button_text: str):
    """Function the make a pop-up window with given title, message, and button text."""
    pop_up = Tk()
    pop_up.geometry("260x110")
    pop_up.title(title)
    pop_up.attributes('-topmost', 'true')
    label = Label(pop_up, text=message)
    label.pack(side="top", padx=10, pady=10)
    okay_button = Button(pop_up, text=button_text, command=pop_up.destroy)
    okay_button.pack(side='bottom', pady=10)


def validate_move(canvas: Canvas, current_index: int, current_player: dict) -> bool:
    """
    Function to validate a given move for a given counter of a given colour on a given square of
    the given board.
    """
    if (current_index == 28) or (get_number_of_colour_on_square(canvas, GAME['board'][current_index], current_player['colour']) == 0):
    # Piece licked is off the board or pieces of that colour in the square given
        return False
    
    for place in GAME['board'][(current_index + 1):(current_index + current_player['die_roll'])]:
        # Checks every place from one ahead of the current to where the die roll would land
        if (place.count(None) < (GAME['total_number_of_counters'] - 1)) and (get_number_of_colour_on_square(canvas, place, current_player['colour']) != len(place)-place.count(None)):
        # Checks there are 2+ counters in square not all belonging to current player
            return False
        
    if current_index + current_player['die_roll'] > 28:
    # Checks if roll would keep counter within board.
        return False
    return True


def move_piece(canvas: Canvas, current_player: dict, counter_ID: int, current_index: int):
    """
    Moves piece with the given counter id from the current index by the die roll.
    """
    remove_from_board(current_index, counter_ID)

    if current_index + current_player['die_roll'] == 28:
        # Die roll takes the piece off the board
        GAME['finished_tokens'].append(current_player['colour'])
    else:
        add_to_board(current_index + current_player['die_roll'], counter_ID)

    # Send back overtaken pieces:
    for i in range(current_index + 1, current_index + current_player['die_roll']):
        if i not in (7, 14, 21):
            # If the square is not a safety
            for piece in GAME['board'][i]:
                # For each piece in the square
                if piece:
                    if list(canvas.gettags(piece))[0] != current_player['colour']:
                        # If the piece is not the same colour as the current player
                        remove_from_board(i, piece)
                        add_to_board(0, piece)
    
    draw_board(canvas)


def remove_from_board(index: int, counter_ID):
    """Function to remove the counter with given id from given index."""
    for i in range(len(GAME['board'][index])):
        if GAME['board'][index][i] == counter_ID:
            GAME['board'][index][i] = None
            return None


def add_to_board(index: int, counter_ID):
    """Function to add a piece to the next empty slot in the given square of the board."""
    for i in range(len(GAME['board'][index])):
        if GAME['board'][index][i] == None:
            GAME['board'][index][i] = counter_ID
            return None


def nearest_square_root(number: int) -> int:
    return m.ceil(m.sqrt(number))


def get_position_in_square(counter_number, total_number_of_counters):
    gap_from_side = 2
    num_counters_across = nearest_square_root(total_number_of_counters)
    width_per_counter = (
        BOARD_SQUARE['width'] - 2*gap_from_side)/num_counters_across
    x = gap_from_side + (counter_number %
                         num_counters_across) * width_per_counter
    y = gap_from_side + (counter_number //
                         num_counters_across) * width_per_counter
    return x, y


def check_if_moves_exist(canvas: Canvas, current_player: dict) -> bool:
    """
    Function to check if there is a move possible for any counter of a given colour on the board.
    """
    for index in range(len(GAME['board'])):
        if get_number_of_colour_on_square(canvas, GAME['board'][index], current_player['colour']) > 0:
            if validate_move(canvas, index, current_player):
                return True
    return False


def board_number_to_position(place_index: int) -> int:
    if place_index < 7:
        x_coord = GAP_FROM_EDGE + 7 * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])
        y_coord = GAP_FROM_TOP + (7 - place_index) * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])

    elif place_index < 15:
        place_index -= 7
        x_coord = GAP_FROM_EDGE + (7 - place_index) * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])
        y_coord = GAP_FROM_TOP

    elif place_index < 22:
        place_index -= 14
        x_coord = GAP_FROM_EDGE
        y_coord = GAP_FROM_TOP + place_index * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])

    elif place_index < 28:
        place_index -= 21
        x_coord = GAP_FROM_EDGE + place_index * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])
        y_coord = GAP_FROM_TOP + 7 * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])

    else:
        x_coord = GAP_FROM_EDGE + 4.5 * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])
        y_coord = GAP_FROM_TOP + 8.25 * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])

    return x_coord, y_coord


def initiate_board(window: Tk) -> Canvas:
    """Function to initialise the game for the start of a game."""
    global PLAYERS
    global GAME
    GAME['board'] = [[] for i in range(28)]

    canvas = Canvas(window, width=CANVAS['width'],
                    height=CANVAS['height'], background="black")

    place_numbering = [
        "S", "XII", "XI", "X", "IX", "IIX", "VII", "S",
        "S", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "S",
        "S", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "S",
        "S", "VI", "V", "IV", "III", "II", "I", "S"
        ]

    count = 0
    for i in range(2):
        for j in range(2):
            for k in range(8):
                r = 5
                x_1 = (1-i)*k*(BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + i*j * \
                    7*(BOARD_SQUARE['width'] +
                       BOARD_SQUARE['spacer']) + GAP_FROM_EDGE
                y_1 = i*k*(BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + (1-i)*j*7 * \
                    (BOARD_SQUARE['width'] +
                     BOARD_SQUARE['spacer']) + GAP_FROM_TOP
                x_2 = (1-i)*(k+1)*BOARD_SQUARE['width'] + (1-i)*k*BOARD_SQUARE['spacer'] + i * \
                    BOARD_SQUARE['width'] + i*j*7 * \
                    (BOARD_SQUARE['width'] +
                     BOARD_SQUARE['spacer']) + GAP_FROM_EDGE
                y_2 = GAP_FROM_TOP + (1-i)*BOARD_SQUARE['width'] + (1-i)*j*7*(
                    BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + i*(k+1)*BOARD_SQUARE['width'] + i*k*BOARD_SQUARE['spacer']
                points = (x_1, y_1, x_2, y_2)
                canvas.create_rectangle(points, fill="white")
                canvas.create_text(
                    (x_1+x_2)/2, (y_1+y_2)/2, text=place_numbering[count], font=Font(family="Times New Roman", size=22), fill="black")
                count += 1

    # Draw player turn label text
    player_turn_label_text = Label(canvas, text="Player turn:", font=Font(
        family="Times New Roman", size=20), background="black", foreground="white", highlightthickness=0)
    player_turn_label_text.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'], y=2 *
                            GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)

    PLAYERS = PLAYERS[::-1]

    # Draw player turn label
    player_turn_label_colour = Label(canvas, text = PLAYERS[0]['colour'].title(),
                                     font = Font(family="Times New Roman", size=25),
                                     background = "black", foreground = PLAYERS[0]['colour'], highlightthickness = 0)
    player_turn_label_colour.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'] + 100, y=2 *
                            GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)

    count = 0
    
    # Gives each board square 6 'None's as its pieces
    for i in range(1, len(GAME['board'])):
        GAME['board'][i] = [None]*GAME['total_number_of_counters']

    # Loops over each colour
    for player in PLAYERS:
        # Loops over each counter
        for i in range(GAME['counters_per_player']):
            x, y = map(lambda a, b: a + b, board_number_to_position(0),
                       get_position_in_square(counter_number=count, total_number_of_counters=GAME['total_number_of_counters']))
            GAME['board'][0].append(canvas.create_oval(x, y, x+COUNTER_DIAMETER, y+COUNTER_DIAMETER,
                                                    fill=player['colour'].lower(), tags=f"{player['colour']}"))
            canvas.tag_bind(GAME['board'][0][-1], "<Button-1>",
                            lambda *args: counter_clicked_on(canvas, player_turn_label_colour, GAME, PLAYERS, *args))
            count += 1

    roman_mosaic = Image.open(os.path.join("images", "bc.png"))

    resized_roman_mosaic = roman_mosaic.resize(
        (6*(BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) - 2*BOARD_SQUARE['spacer'], 6*(BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) - 2*BOARD_SQUARE['spacer']))
    board_centre_image = ImageTk.PhotoImage(resized_roman_mosaic)
    window.board_centre_image = board_centre_image
    board_centre = canvas.create_image(canvas.winfo_reqwidth()/2,
                                       canvas.winfo_reqwidth()/2, anchor=CENTER, image=board_centre_image)

    new_game_button = Button(canvas, bg="blue", fg="blue",
                             text="New Game", command=lambda: start_new_game(window))
    new_game_button_window = canvas.create_window(GAP_FROM_EDGE + 6*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), 2*GAP_FROM_TOP + 8*(
        BOARD_SQUARE['spacer']+BOARD_SQUARE['width']) + BOARD_SQUARE["spacer"], anchor=W, window=new_game_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    quit_button = Button(canvas, bg="blue", fg="red",
                         text="Exit", command=quit)
    quit_button_window = canvas.create_window(GAP_FROM_EDGE + 6*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), 2*GAP_FROM_TOP + 8*(
        BOARD_SQUARE['spacer']+BOARD_SQUARE['width']) + BOARD_SQUARE['width']/2 + 3*BOARD_SQUARE['spacer'], anchor=W, window=quit_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    roll_die_button = Button(canvas, bg="white", fg="black",
                             text="Roll Die", command=lambda: roll_die_animation(canvas, 10, player_turn_label_colour))
    roll_die_button_window = canvas.create_window(GAP_FROM_EDGE + 2*BOARD_SQUARE['spacer'], 2 *
                                                  GAP_FROM_TOP + 16*BOARD_SQUARE['spacer'] + 8*BOARD_SQUARE['width'], anchor=W, window=roll_die_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    canvas.pack(fill=NONE)
    return canvas


def draw_board(canvas: Canvas):
    for i, square in enumerate(GAME['board'] + GAME['finished_tokens']):
        for j, piece in enumerate(square):
            if piece:
                x, y = map(lambda a, b: a + b,
                        board_number_to_position(i),
                        get_position_in_square(counter_number = j,
                                                total_number_of_counters = \
                                                    GAME['total_number_of_counters']))
                canvas.moveto(piece, x, y)
    
    canvas.update()


def start_new_game(window: Tk):
    """Function to kill the current game and start a new one."""
    window.destroy()
    main()


def next_player_turn(canvas: Canvas, player_turn_label: Label):
    """Function to change the current player turn to the next one in the player list."""
    PLAYERS[0]['die_roll'] = 0  # Reset player's die roll
    PLAYERS.append(PLAYERS.pop(0))
    display_player_turn(canvas, player_turn_label, PLAYERS[0]['colour'])


def display_player_turn(canvas: Canvas, player_turn_label: Label, player_colour: str):
    """Function to update the current player turn shown on main window."""
    player_turn_label.config(text=player_colour, foreground=player_colour)
    canvas.update()


def roll_die_animation(canvas: Canvas, time_period_ms: int, player_turn_label: Label):
    """
    Recursive function to show a rolling die and pick random number between 1 and 6 when roll die
    button is clicked on.
    """
    if PLAYERS[0]['die_roll'] and time_period_ms == 10:
        return None
    
    die_number = r.randint(1, 6)
    die_image_raw = Image.open(os.path.join("images", "die_faces", f"die_face_{die_number}.png"))
    resized_die_image = die_image_raw.resize((80, 80))
    die_image = ImageTk.PhotoImage(resized_die_image)
    canvas.die_image = die_image
    die = canvas.create_image(250, 685, image=die_image)
    canvas.update()
    if time_period_ms < 150:
        canvas.after(time_period_ms,
                     lambda: roll_die_animation(canvas, int(1.2*time_period_ms), player_turn_label))
    else:
        PLAYERS[0]['die_roll'] = die_number
        if not check_if_moves_exist(canvas, PLAYERS[0]):
            # No moves exist
            pop_up_message(title="OH DEAR",
                        message="No moves available - sorry", button_text="Okay")
            next_player_turn(canvas, player_turn_label)
            PLAYERS[0]['die_roll'] = 0


def print_player_turn(canvas: Canvas):
    current_player_turn = Label(canvas, text="Player turn:", font=Font(
        family="Times New Roman", size=20), background="black", foreground="white")
    current_player_turn.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'], y=2 *
                              GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)


def get_counter_colour_from_id(canvas: Canvas, counter_id: int) -> str:
    """Function to return the colour of a counter from its ID."""
    return list(canvas.gettags(counter_id))[0]


def get_number_of_colour_on_square(canvas: Canvas, square: list[int], colour: str = "any") -> int:
    """
    Function to return the number of counters of a given colour on a given index of the board.
    """
    counter_colours = [get_counter_colour_from_id(canvas, counter) for counter in square if counter]
    if colour == 'any':
        return counter_colours.count()
    return counter_colours.count(colour)


def get_new_game_ID():
    return r.randint(10000, 99999)


def server_new_game():
    """Function to start a new game on the ec2 server."""
    response = requests.post(f"{GAME['ec2_url']}/new_game", json={
        'game': GAME,
        'players': PLAYERS})
    if response.status_code != 200:
        print(response.text)
        raise ValueError("Error connecting to the server!!")


def join_game():
    """Function to join a game on the ec2 server."""
    global PLAYER
    response = requests.post(f"{GAME['ec2_url']}/new_player", json={'game_id': GAME['id']})
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise ValueError("Error connecting to the server!!")
    PLAYER = response.json().get('player')


def update_server():
    """Function to update ec2 server based on local game state."""
    global GAME
    requests.post(f"{GAME['ec2_url']}/update", json={'game': GAME, 'players': PLAYERS})


def update_local():
    global GAME
    global PLAYERS
    response = requests.get(f"{GAME['ec2_url']}/update")
    if response.status_code != 200:
        return response.json
    
    server_state = response.json()
    GAME['board'] = deepcopy(server_state['game']['board'])
    GAME['finished_tokens'] = deepcopy(server_state['game']['finished_tokens'])
    GAME['number_of_players']: server_state['game']['number_of_players']
    GAME['counters_per_player']: server_state['game']['counters_per_player']
    GAME['total_number_of_counters'] = GAME['number_of_players'] * GAME['counters_per_player']
    PLAYERS = deepcopy(server_state['players'])


def main():
    global GAME
    GAME = {
        'number_of_players': 0,
        'counters_per_player': 0,
        'board': [[] for i in range(28)],
        'finished_tokens': []
        }
    global PLAYERS
    PLAYERS = []
    
    window = Tk()
    window.title('The Roman Stones')
    window.geometry("720x800+10+20")
    window.configure(bg="black")

    server_address_pop_up(window)
    new_or_join_game_pop_up(window)
    
    if GAME.get('id', None) == -1:
        new_game_pop_up_players_and_tokens(window)
        new_game_pop_up_colours(window)
        GAME['id'] = get_new_game_ID()
        server_new_game()
        join_game()
        pop_up_message('New Game', f"Your game ID is: {GAME['id']}", 'Start Game')
    else:
        join_game_pop_up_ids(window)
        join_game()


    update_local()
    print(GAME)
    canvas = initiate_board(window)

    draw_board(canvas)

    while PLAYERS[0]['colour'] != PLAYER:
        print(PLAYERS[0]['colour'], PLAYER)
        update_local()
        draw_board(canvas)

    window.mainloop()


if __name__ == "__main__":
    main()
    