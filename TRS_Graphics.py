
import os
from time import sleep

from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
import math as m
import random as r
import backend


CANVAS = {'height': 750, 'width': 650}
BOARD_SQUARE = {'width': 70, 'spacer': 5}
NUM_SQUARES = 8
GAP_FROM_EDGE = (CANVAS['width'] - NUM_SQUARES *
                 (BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) + BOARD_SQUARE['spacer'])/2

GAP_FROM_TOP = GAP_FROM_EDGE
COUNTER_DIAMETER = 20


def get_num_players_and_tokens_selection(pop_up: Toplevel, num_player_menu: StringVar, num_counters_menu: StringVar, game_settings):
    game_settings['num_players'] = int(num_player_menu.get())
    game_settings['num_counters'] = int(num_counters_menu.get())
    pop_up.destroy()
    pop_up.quit()


def new_game_pop_up_players_and_tokens(window, user_options: dict):
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
                                   text="Choose Colours", command=lambda: get_num_players_and_tokens_selection(pop_up, num_player_menu, num_counters_menu, user_options))
    choose_colours_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white")
    choose_colours_button.place(x=120, y=68)

    window.mainloop()


def get_colour_selection(pop_up: Toplevel, colours: list[str], colour_menu: Listbox):
    for i in colour_menu.curselection():
        colours.append(colour_menu.get(i))
    pop_up.destroy()
    pop_up.quit()


def check_win(finished_tokens: list, current_player: str, number_of_tokens: int) -> bool:
    """Function to check if the given player has won the game."""
    if finished_tokens.count(current_player) == number_of_tokens:
        return True
    return False


def new_game_pop_up_colours(window, game_settings: dict, colour_options: list[str]):
    number_words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

    pop_up = Toplevel(window, bg="white")
    pop_up.geometry("260x110")
    pop_up.title("New game")

    Label(pop_up, text=f"Please choose {number_words[game_settings['num_players']]} colours:", font=(
        'Times'), bg="white", fg="black").place(x=10, y=10)

    colour_menu = Listbox(pop_up, selectmode=MULTIPLE,
                          width=10, height=len(colour_options))
    for colour in colour_options:
        colour_menu.insert(END, colour)

    selected_button_indices = []
    colour_menu.config(bg="white", fg="black")
    colour_menu.place(x=160, y=12)
    colour_menu.bind("<<ListboxSelect>>", lambda *args: limit_colour_selection(
        colour_menu, selected_button_indices, game_settings['num_players']))

    play_game_button = Button(pop_up, bg="white", fg="white",
                              text="Play Game", command=lambda: get_colour_selection(pop_up, game_settings['colours'], colour_menu))
    play_game_button.config(
        bg="red", fg="black", borderwidth=5, highlightbackground="white")
    play_game_button.place(x=25, y=40)

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


def counter_clicked_on(canvas: Canvas, player_turn_label: Label, game_settings, *args):
    """Function called when a counter is clicked on."""
    counter_id = list(canvas.find_withtag("current"))[0]
    colour = get_counter_colour_from_id(canvas, counter_id)
    current_index = backend.find_counter_on_board(counter_id, game_settings['board'])
    
    if game_settings['current_player'] != colour:
        # Player clicked on wrong counter colour
        return None
    if game_settings['die_roll'] == 0:
        # Die has not yet been rolled
        return None
    
    if validate_move(canvas, current_index, game_settings['board'], game_settings['die_roll'], colour, game_settings['total_number_of_counters']):
        # Move is valid
        move_piece(canvas, game_settings['board'],
                   list(canvas.find_withtag("current"))[0], current_index, game_settings)
        game_settings['die_roll'] = 0  # Reset die roll
        if check_win(game_settings['finished_tokens'], game_settings['current_player'], game_settings['num_counters']):
            pop_up_message(title="Winner!",
                           message=f"Congratulations {game_settings['current_player']} player,\nyou've won!!!", button_text="Okay")
        next_player_turn(canvas, player_turn_label, game_settings)


def pop_up_message(title: str, message: str, button_text: str):
    """Function the make a pop-up window with given title, message, and button text."""
    pop_up = Tk()
    pop_up.geometry("260x110")
    pop_up.title(title)
    label = Label(pop_up, text=message)
    label.pack(side="top", padx=10, pady=10)
    okay_button = Button(pop_up, text=button_text, command=pop_up.destroy)
    okay_button.pack(side='bottom')


def validate_move(canvas: Canvas, current_index: int, board: list, die_roll: int, colour: str, total_number_of_counters: int) -> bool:
    """
    Function to validate a given move for a given counter of a given colour on a given square of
    the given board.
    """
    if (current_index == 28) or (get_number_of_colour_on_square(canvas, board[current_index], colour) == 0):
    # Piece licked is off the board or pieces of that colour in the square given
        return False
    
    for place in board[current_index+1:current_index+die_roll]:
        # Checks every place from one ahead of the current to where the die roll would land
        if (place.count(None) < (total_number_of_counters - 1)) and (get_number_of_colour_on_square(canvas, place, colour) != len(place)-place.count(None)):
        # Checks there are 2+ counters in square not all belonging to current player
            return False
        
    if current_index + die_roll > 28:
    # Checks if roll would keep counter within board.
        return False
    return True


def move_piece(canvas: Canvas, board, counter_ID, current_index, game_settings):
    """
    Moves piece with the given counter id from the current index by the game settings' die roll.
    """
    colour = game_settings['current_player']
    remove_from_board(board, current_index, counter_ID)

    if current_index + game_settings['die_roll'] == 28:
        # Die roll takes the piece off the board
        game_settings['finished_tokens'].append(game_settings['current_player'])
        x, y = map(lambda i, j: i + j,
                   board_number_to_position(current_index + game_settings['die_roll']),
                   get_position_in_square(counter_number=len(game_settings['finished_tokens']),
                                          total_number_of_counters=\
                                            game_settings['total_number_of_counters']))
        canvas.moveto(counter_ID, x, y)
        counter_tags = canvas.gettags(counter_ID)
        canvas.itemconfig(counter_ID,
                          tags=f"{counter_tags[0]} {counter_tags[1]} " + \
                            f"{current_index + game_settings['die_roll']}")
    else:
        index_in_square = add_to_board(board,
                                       current_index + game_settings['die_roll'],
                                       counter_ID)
        x, y = map(lambda i, j: i + j, board_number_to_position(current_index + game_settings['die_roll']), get_position_in_square(
            counter_number=index_in_square, total_number_of_counters=game_settings['total_number_of_counters']))
        canvas.moveto(counter_ID, x, y)
        counter_tags = canvas.gettags(counter_ID)
        canvas.itemconfig(counter_ID, tags=f"{counter_tags[0]} {counter_tags[1]} " + \
                          str({current_index + game_settings['die_roll']}))

    # Send back overtaken pieces:
    for i in range(current_index+1, current_index+game_settings['die_roll']):
        if board[i] and i not in (7, 14, 21):
            # If there is a counter in the square and the square is not a safety
            for piece in board[i]:
                # For each piece in the square
                if piece:
                    if list(canvas.gettags(piece))[0] != colour:
                        # If the piece is not the same colour as the current player
                        remove_from_board(board, i, piece)
                        index_in_square = add_to_board(board, 0, piece)
                        x, y = map(lambda i, j: i + j, board_number_to_position(0), get_position_in_square(
                            counter_number=index_in_square, total_number_of_counters=game_settings['total_number_of_counters']))
                        canvas.moveto(piece, x, y)
                        counter_tags = canvas.gettags(piece)
                        canvas.itemconfig(
                            piece, tags=f"{counter_tags[0]} {counter_tags[1]} 0")


def remove_from_board(board, index, counter_ID):
    """Function to remove the counter with given id from given index."""
    for i in range(len(board[index])):
        if board[index][i] == counter_ID:
            board[index][i] = None
            return None


def add_to_board(board, index, counter_ID) -> int:
    """Function to add a piece to the next empty slot in the given square of the board."""
    for i in range(len(board[index])):
        if board[index][i] == None:
            board[index][i] = counter_ID
            return i


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


def check_if_moves_exist(canvas: Canvas, board: list[list[int]], die_roll: int, colour: str, total_number_of_counters: int) -> bool:
    """
    Function to check if there is a move possible for any counter of a given colour on the board.
    """
    for index in range(len(board)):
        if get_number_of_colour_on_square(canvas, board[index], colour) > 0:
            if validate_move(canvas, index, board, die_roll, colour, total_number_of_counters):
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


def draw_board(window: Tk, game_settings: dict):

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

    game_settings['colours'] = game_settings['colours'][::-1]
    game_settings['current_player'] = game_settings['colours'].pop(0)
    game_settings['colours'].append(game_settings['current_player'])

    # Draw player turn label
    player_turn_label_colour = Label(canvas, text=game_settings['current_player'].title(), font=Font(
        family="Times New Roman", size=25), background="black", foreground=game_settings['current_player'], highlightthickness=0)
    player_turn_label_colour.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'] + 100, y=2 *
                            GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)

    count = 0
    game_settings['total_number_of_counters'] = len(
        game_settings['colours'])*game_settings['num_counters']
    
    # Gives each board square 6 'None's as its pieces
    for i in range(1, len(game_settings['board'])):
        game_settings['board'][i] = [None]*game_settings['total_number_of_counters']

    # Loops over each colour
    for i in range(len(game_settings['colours'])):
        # Loops over each counter
        for j in range(game_settings['num_counters']):
            x, y = map(lambda i, j: i + j, board_number_to_position(
                0), get_position_in_square(counter_number=count, total_number_of_counters=game_settings['total_number_of_counters']))
            game_settings['board'][0].append(canvas.create_oval(
                x, y, x+COUNTER_DIAMETER, y+COUNTER_DIAMETER, fill=game_settings['colours'][i].lower(), tags=f"{game_settings['colours'][i]} {j}"))
            canvas.tag_bind(game_settings['board'][0][-1],
                            "<Button-1>", lambda *args: counter_clicked_on(canvas, player_turn_label_colour, game_settings, * args))
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
                             text="Roll Die", command=lambda: roll_die_animation(canvas, 10, game_settings, player_turn_label_colour))
    roll_die_button_window = canvas.create_window(GAP_FROM_EDGE + 2*BOARD_SQUARE['spacer'], 2 *
                                                  GAP_FROM_TOP + 16*BOARD_SQUARE['spacer'] + 8*BOARD_SQUARE['width'], anchor=W, window=roll_die_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    canvas.pack(fill=NONE)


def start_new_game(window: Tk):
    """Function to kill the current game and start a new one."""
    window.destroy()
    backend.main()


def next_player_turn(canvas: Canvas, player_turn_label: Label, game_settings: dict):
    """Function to change the current player turn to the next one in the player list."""
    game_settings['current_player'] = game_settings['colours'].pop(0)
    game_settings['colours'].append(game_settings['current_player'])
    display_player_turn(canvas, player_turn_label,
                        game_settings['current_player'])


def display_player_turn(canvas: Canvas, player_turn_label: Label, player_colour: str):
    """Function to update the current player turn shown on main window."""
    player_turn_label.config(text=player_colour, foreground=player_colour)
    canvas.update()


def roll_die_animation(canvas: Canvas, time_period_ms: int, game_settings: dict, player_turn_label: Label):
    if game_settings['die_roll'] != 0 and time_period_ms == 10:
        return None
    die_number = r.randint(1, 6)
    die_image_raw = Image.open(os.path.join("images", "die_faces", f"die_face_{die_number}.png"))
    resized_die_image = die_image_raw.resize((80, 80))
    die_image = ImageTk.PhotoImage(resized_die_image)
    canvas.die_image = die_image
    die = canvas.create_image(250, 685, image=die_image)
    canvas.update()
    if time_period_ms < 150:
        canvas.after(time_period_ms, lambda: roll_die_animation(
            canvas, int(1.2*time_period_ms), game_settings, player_turn_label))
    else:
        game_settings['die_roll'] = die_number
        if not check_if_moves_exist(canvas, game_settings['board'], game_settings['die_roll'], game_settings['current_player'], game_settings['total_number_of_counters']):
            # No moves exist
            pop_up_message(title="OH DEAR",
                        message="No moves available - sorry", button_text="Okay")
            next_player_turn(canvas, player_turn_label, game_settings)
            game_settings['die_roll'] = 0


def player_turn():
    pass


def print_player_turn():
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