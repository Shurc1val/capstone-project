from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
import math as m
import random as r
from TRS_backend import *


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

    Label(pop_up, text="Please enter the number of players: ", font=(
        'Times'), bg="white", fg="black").place(x=10, y=10)

    num_player_menu = StringVar()
    num_player_menu.set("2")
    num_player_drop = OptionMenu(pop_up, num_player_menu, "1", "2", "3", "4")
    num_player_drop.config(bg="white", fg="black")
    num_player_drop.place(x=200, y=10)

    Label(pop_up, text="Number of tokens for each player:", font=(
        'Times'), bg="white", fg="black").place(x=10, y=40)

    num_counters_menu = StringVar()
    num_counters_menu.set("3")
    num_counters_drop = OptionMenu(pop_up, num_counters_menu, "1", "2", "3")
    num_counters_drop.config(bg="white", fg="black")
    num_counters_drop.place(x=200, y=40)

    """colour_options = 
    colour_menu = Listbox(pop_up, selectmode=MULTIPLE, )"""

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


def check_win(finished_tokens, current_player, number_of_tokens):
    print(finished_tokens, current_player, number_of_tokens)
    if finished_tokens.count(current_player) == number_of_tokens:
        return True
    return False


def new_game_pop_up_colours(window, game_settings: dict, colour_options: list[str]):
    number_words = {1: "one", 2: "two", 3: "three", 4: "four"}

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
    counter_selected = list(canvas.gettags("current"))
    colour = counter_selected[0]
    current_index = int(counter_selected[2])
    if not check_if_moves_exist(canvas, game_settings['board'], game_settings['die_roll'], game_settings['current_player'], game_settings['total_number_of_counters']):
        pop_up_message(canvas, title="OH DEAR",
                       message="No moves available - sorry", button_text="Okay")
        next_player_turn(canvas, player_turn_label, game_settings)
        game_settings['die_roll'] = 0
    if game_settings['current_player'] != colour:
        return None
    if game_settings['die_roll'] == 0:
        return None
    print(canvas.gettags("current"))
    if validate_move(canvas, current_index, game_settings['board'], game_settings['die_roll'], colour, game_settings['total_number_of_counters']):
        print("a")
        move_piece(canvas, game_settings['board'],
                   list(canvas.find_withtag("current"))[0], current_index, game_settings)
        game_settings['die_roll'] = 0
        if check_win(game_settings['finished_tokens'], game_settings['current_player'], game_settings['num_counters']):
            pop_up_message(canvas, title="Winner!",
                           message=f"Congratulations {game_settings['current_player']} player, you've won!!!", button_text="Okay")
        next_player_turn(canvas, player_turn_label, game_settings)
    print("b")

    # canvas.moveto(canvas.find_withtag("current"), x, y)


def pop_up_message(canvas: Canvas, title: str, message: str, button_text: str):
    pop_up = Tk()
    pop_up.geometry("260x110")
    pop_up.title(title)
    label = Label(pop_up, text=message)
    label.pack(side="top", padx=10, pady=10)
    okay_button = Button(pop_up, text=button_text, command=pop_up.destroy)
    okay_button.pack(side='bottom')


def validate_move(canvas: Canvas, current_index, board: list, die_roll, colour, total_number_of_counters):
    if [list(canvas.gettags(counter))[0] for counter in board[current_index] if counter != None].count(colour) == 0:
        print("apple", [list(canvas.gettags(counter))[0]
                        for counter in board[current_index] if counter != None])
        print(board[current_index])
        print([list(canvas.gettags(counter))[0]
              for counter in board[current_index]])
        return False
    for place in board[current_index+1:current_index+die_roll]:
        if place.count(None) < total_number_of_counters-1 and [list(canvas.gettags(counter))[0] for counter in place if counter != None].count(colour) != len(place)-place.count(None):
            print("banana", [list(canvas.gettags(counter))[0]
                  for counter in place if counter != None], place)
            return False
    if current_index + die_roll > 28:
        return False
    return True


def move_piece(canvas: Canvas, board, counter_ID, current_index, game_settings):
    print(counter_ID)
    print(current_index, board[current_index])
    colour = game_settings['current_player']
    remove_from_board(board, current_index, counter_ID)
    if current_index + game_settings['die_roll'] == 28:
        game_settings['finished_tokens'].append(
            game_settings['current_player'])
        x, y = map(lambda i, j: i + j, board_number_to_position(current_index + game_settings['die_roll']), get_position_in_square(
            counter_number=len(game_settings['finished_tokens']), total_number_of_counters=game_settings['total_number_of_counters']))
        canvas.moveto(
            counter_ID, x, y)
        counter_tags = canvas.gettags(counter_ID)
        canvas.itemconfig(
            counter_ID, tags=f"{counter_tags[0]} {counter_tags[1]} {current_index + game_settings['die_roll']}")

    else:
        index_in_square = add_to_board(board, current_index +
                                       game_settings['die_roll'], counter_ID)
        x, y = map(lambda i, j: i + j, board_number_to_position(current_index + game_settings['die_roll']), get_position_in_square(
            counter_number=index_in_square, total_number_of_counters=game_settings['total_number_of_counters']))
        canvas.moveto(
            counter_ID, x, y)
        counter_tags = canvas.gettags(counter_ID)
        canvas.itemconfig(
            counter_ID, tags=f"{counter_tags[0]} {counter_tags[1]} {current_index + game_settings['die_roll']}")

    for i in range(current_index+1, current_index+game_settings['die_roll']):
        if board[i] and i not in (7, 14, 21):
            for piece in board[i]:
                if piece != None:
                    if list(canvas.gettags(piece))[0] != colour:
                        remove_from_board(board, i, piece)
                        index_in_square = add_to_board(board, 0, piece)
                        x, y = map(lambda i, j: i + j, board_number_to_position(0), get_position_in_square(
                            counter_number=index_in_square, total_number_of_counters=game_settings['total_number_of_counters']))
                        canvas.moveto(piece, x, y)
                        counter_tags = canvas.gettags(piece)
                        canvas.itemconfig(
                            piece, tags=f"{counter_tags[0]} {counter_tags[1]} 0")


def remove_from_board(board, index, counter_ID):
    for i in range(len(board[index])):
        if board[index][i] == counter_ID:
            board[index][i] = None
            return None


def add_to_board(board, index, counter_ID) -> int:
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


def check_if_moves_exist(canvas: Canvas, board: list, die_roll, colour, total_number_of_counters):
    for index in range(len(board)):
        if [list(canvas.gettags(counter))[0] for counter in board[index] if counter != None].count(colour) > 0:
            print("cheesecake")
            print([list(canvas.gettags(counter))[0]
                   for counter in board[index] if counter != None], board[index])
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

    place_numbering = ["S", "XII", "XI", "X", "IX", "IIX", "VII", "S", "S", "XIX", "XX", "XXI", "XXII", "XXIII",
                       "XXIV", "S", "S", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "S", "S", "VI", "V", "IV", "III", "II", "I", "S"]

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

    player_turn_label = Label(canvas, text="Player turn:", font=Font(
        family="Times New Roman", size=20), background="black", foreground="white", highlightthickness=0)
    player_turn_label.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'], y=2 *
                            GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)

    game_settings['colours'] = game_settings['colours'][::-1]
    game_settings['current_player'] = game_settings['colours'].pop(0)
    game_settings['colours'].append(game_settings['current_player'])
    player_turn_label = Label(canvas, text=game_settings['current_player'].title(), font=Font(
        family="Times New Roman", size=25), background="black", foreground=game_settings['current_player'], highlightthickness=0)
    player_turn_label.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'] + 100, y=2 *
                            GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)

    count = 0
    game_settings['total_number_of_counters'] = len(
        game_settings['colours'])*game_settings['num_counters']
    for i in range(1, len(game_settings['board'])):
        game_settings['board'][i] = [None]*6

    for i in range(len(game_settings['colours'])):
        for j in range(game_settings['num_counters']):
            x, y = map(lambda i, j: i + j, board_number_to_position(
                0), get_position_in_square(counter_number=count, total_number_of_counters=game_settings['total_number_of_counters']))
            game_settings['board'][0].append(canvas.create_oval(
                x, y, x+COUNTER_DIAMETER, y+COUNTER_DIAMETER, fill=game_settings['colours'][i].lower(), tags=f"{game_settings['colours'][i]} {j} {0}"))
            canvas.tag_bind(game_settings['board'][0][-1],
                            "<Button-1>", lambda *args: counter_clicked_on(canvas, player_turn_label, game_settings, * args))
            count += 1
    print(game_settings['board'][0])

    roman_mosaic = Image.open(
        "/Users/hughmorris/Documents/Prework/capstone-project/images/bc.png")

    resized_roman_mosaic = roman_mosaic.resize(
        (6*(BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) - 2*BOARD_SQUARE['spacer'], 6*(BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) - 2*BOARD_SQUARE['spacer']))
    board_centre_image = ImageTk.PhotoImage(resized_roman_mosaic)
    window.board_centre_image = board_centre_image
    board_centre = canvas.create_image(canvas.winfo_reqwidth()/2,
                                       canvas.winfo_reqwidth()/2, anchor=CENTER, image=board_centre_image)

    new_game_button = Button(canvas, bg="blue", fg="blue", text="New Game")
    new_game_button_window = canvas.create_window(GAP_FROM_EDGE + 6*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), 2*GAP_FROM_TOP + 8*(
        BOARD_SQUARE['spacer']+BOARD_SQUARE['width']) + BOARD_SQUARE["spacer"], anchor=W, window=new_game_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    quit_button = Button(canvas, bg="blue", fg="red",
                         text="Exit", command=quit)
    quit_button_window = canvas.create_window(GAP_FROM_EDGE + 6*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), 2*GAP_FROM_TOP + 8*(
        BOARD_SQUARE['spacer']+BOARD_SQUARE['width']) + BOARD_SQUARE['width']/2 + 3*BOARD_SQUARE['spacer'], anchor=W, window=quit_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    roll_die_button = Button(canvas, bg="white", fg="black",
                             text="Roll Die", command=lambda: roll_die_animation(canvas, 10, game_settings))
    roll_die_button_window = canvas.create_window(GAP_FROM_EDGE + 2*BOARD_SQUARE['spacer'], 2 *
                                                  GAP_FROM_TOP + 16*BOARD_SQUARE['spacer'] + 8*BOARD_SQUARE['width'], anchor=W, window=roll_die_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    canvas.pack(fill=NONE)


def next_player_turn(canvas: Canvas, player_turn_label: Label, game_settings: dict):
    game_settings['current_player'] = game_settings['colours'].pop(0)
    game_settings['colours'].append(game_settings['current_player'])
    display_player_turn(canvas, player_turn_label,
                        game_settings['current_player'])


def display_player_turn(canvas: Canvas, player_turn_label: Label, player_colour: str):
    player_turn_label.config(text=player_colour, foreground=player_colour)
    canvas.update()


def roll_die_animation(canvas: Canvas, time_period_ms: int, game_settings: dict):
    if game_settings['die_roll'] != 0 and time_period_ms == 10:
        return None
    die_number = r.randint(1, 6)
    die_image_raw = Image.open(
        f"/Users/hughmorris/Documents/Prework/capstone-project/images/die_faces/die_face_{die_number}.png")
    resized_die_image = die_image_raw.resize((80, 80))
    die_image = ImageTk.PhotoImage(resized_die_image)
    canvas.die_image = die_image
    die = canvas.create_image(250, 685, image=die_image)
    canvas.update()
    if time_period_ms < 150:
        canvas.after(time_period_ms, lambda: roll_die_animation(
            canvas, int(1.2*time_period_ms), game_settings))
    else:
        game_settings['die_roll'] = die_number


def player_turn():
    pass


def print_player_turn():
    current_player_turn = Label(canvas, text="Player turn:", font=Font(
        family="Times New Roman", size=20), background="black", foreground="white")
    current_player_turn.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'], y=2 *
                              GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)
