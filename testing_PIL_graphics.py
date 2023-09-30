from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font

CANVAS = {'height': 800, 'width': 650}
BOARD_SQUARE = {'width': 70, 'spacer': 5}
NUM_SQUARES = 8
GAP_FROM_EDGE = (CANVAS['width'] - NUM_SQUARES *
                 (BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) + BOARD_SQUARE['spacer'])/2

GAP_FROM_TOP = GAP_FROM_EDGE

CURRENT_SQUARE = -1


def piece_selected(*args):
    global CURRENT_SQUARE
    CURRENT_SQUARE += 1
    x, y = board_number_to_position(CURRENT_SQUARE)
    canvas.moveto(canvas.find_withtag("current"), x, y)


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


def draw_board(canvas: Canvas, board: list[list[str]]):



players = ["Red"]
current_player = "Red"

counters = {}
for colour in players:
    counters[colour] = []
num_counters = 1

window = Tk()

window.title('The Roman Stones')
window.geometry("720x800+10+20")
window.configure(bg="black")

canvas = Canvas(window, width=CANVAS['width'],
                height=CANVAS['height'], background="black")

count = 0

place_numbering = ["S", "XII", "XI", "X", "IX", "IIX", "VII", "S", "S", "XIX", "XX", "XXI", "XXII", "XXIII",
                   "XXIV", "S", "S", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "S", "S", "VI", "V", "IV", "III", "II", "I", "S"]
for i in range(2):
    for j in range(2):
        for k in range(8):
            r = 5
            x_1 = (1-i)*k*(BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + i*j * \
                7*(BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + GAP_FROM_EDGE
            y_1 = i*k*(BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + (1-i)*j*7 * \
                (BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + GAP_FROM_TOP
            x_2 = (1-i)*(k+1)*BOARD_SQUARE['width'] + (1-i)*k*BOARD_SQUARE['spacer'] + i * \
                BOARD_SQUARE['width'] + i*j*7*(BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + GAP_FROM_EDGE
            y_2 = GAP_FROM_TOP + (1-i)*BOARD_SQUARE['width'] + (1-i)*j*7*(
                BOARD_SQUARE['width'] + BOARD_SQUARE['spacer']) + i*(k+1)*BOARD_SQUARE['width'] + i*k*BOARD_SQUARE['spacer']
            points = (x_1, y_1, x_2, y_2)
            canvas.create_rectangle(points, fill="white")
            canvas.create_text(
                (x_1+x_2)/2, (y_1+y_2)/2, text=place_numbering[count], font=Font(family="Times New Roman", size=20))
            count += 1


for colour in players:
    for i in range(1, num_counters+1):
        counters[colour].append(canvas.create_oval(
            20, 20, 40, 40, fill="red", tags=colour + str(i)))
        canvas.tag_bind(colour + str(i), "<Button-1>", piece_selected)


board_centre = Image.open(
    "/Users/hughmorris/Documents/Prework/capstone-project/images/bc.png")

resized_image = board_centre.resize(
    (6*(BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) - 2*BOARD_SQUARE['spacer'], 6*(BOARD_SQUARE['width']+BOARD_SQUARE['spacer']) - 2*BOARD_SQUARE['spacer']))
new_image = ImageTk.PhotoImage(resized_image)
canvas.create_image(canvas.winfo_reqwidth()/2,
                    canvas.winfo_reqwidth()/2, anchor=CENTER, image=new_image)


new_game_button = Button(canvas, bg="blue", fg="blue", text="New Game")
new_game_button_window = canvas.create_window(gap_from_edge + 6*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), 2*gap_from_top + 8*(
    BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W, window=new_game_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

quit_button = Button(canvas, bg="blue", fg="red", text="Exit", command=quit)
quit_button_window = canvas.create_window(gap_from_edge + 6*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), 2*gap_from_top + 8*(
    BOARD_SQUARE['spacer']+BOARD_SQUARE['width']) + BOARD_SQUARE['width']/2 + 2*BOARD_SQUARE['spacer'], anchor=W, window=quit_button, width=2 * BOARD_SQUARE['width'] + BOARD_SQUARE['spacer'], height=BOARD_SQUARE['width']/2)

current_player_label = Label(canvas, text="Player:", font=Font(
    family="Cambria", size=20), background="white", foreground="black")
current_player_label.place(relx=2*gap_from_edge, rely=2 *
                           gap_from_top + 8*(BOARD_SQUARE['spacer']+BOARD_SQUARE['width']), anchor=W)
canvas.pack(fill=NONE)

window.mainloop()
