from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
import math as m
import random as r
import time as t


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


def counter_clicked_on(canvas: Canvas, *args):
    return canvas.find_withtag("current")
    canvas.moveto(canvas.find_withtag("current"), x, y)


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

    else:
        place_index -= 21
        x_coord = GAP_FROM_EDGE + place_index * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])
        y_coord = GAP_FROM_TOP + 7 * \
            (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'])

    return x_coord, y_coord


def draw_board(window: Tk, players: list[str], num_counters: int):

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

    counters = {}
    for colour in players:
        counters[colour] = []

    count = 0
    for i in range(len(players)):
        for j in range(num_counters):
            x, y = map(lambda i, j: i + j, board_number_to_position(
                0), get_position_in_square(counter_number=count, total_number_of_counters=len(players)*num_counters))
            counters[colour].append(canvas.create_oval(
                x, y, x+COUNTER_DIAMETER, y+COUNTER_DIAMETER, fill=players[i].lower(), tags=f"{players[i]} {j}"))
            canvas.tag_bind(f"{players[i]} {j}",
                            "<Button-1>", counter_clicked_on(canvas))
            count += 1

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

    player_turn_label = Label(canvas, text="Player turn:", font=Font(
        family="Times New Roman", size=20), background="black", foreground="white", highlightthickness=0)
    player_turn_label.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'], y=2 *
                            GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)

    roll_die_button = Button(canvas, bg="white", fg="black",
                             text="Roll Die", command=lambda: roll_die(canvas))
    roll_die_button_window = canvas.create_window(2*GAP_FROM_EDGE, 2 *
                                                  GAP_FROM_TOP + 16*BOARD_SQUARE['spacer'] + 8*BOARD_SQUARE['width'], anchor=W, window=roll_die_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

    canvas.pack(fill=NONE)


def roll_die(canvas: Canvas):
    time_period = 0.1
    while time_period < 1:
        die_number = r.randint(1, 6)
        die_image_raw = Image.open(
            f"/Users/hughmorris/Documents/Prework/capstone-project/images/die_faces/die_face_{die_number}.png")
        resized_die_image = die_image_raw.resize((80, 80))
        die_image = ImageTk.PhotoImage(resized_die_image)
        canvas.die_image = die_image
        die = canvas.create_image(280, 685, image=die_image)
        t.sleep(time_period)
        time_period *= 1.1


def player_turn():
    pass


def print_player_turn():
    current_player_turn = Label(canvas, text="Player turn:", font=Font(
        family="Times New Roman", size=20), background="black", foreground="white")
    current_player_turn.place(x=GAP_FROM_EDGE + BOARD_SQUARE['spacer'], y=2 *
                              GAP_FROM_TOP + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)
