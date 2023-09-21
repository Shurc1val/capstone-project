from graphics import *
import tkinter as tk

def main():
    win = GraphWin("Game Board", 800, 800)
    win.setBackground("black")
    gap_from_top = 100
    gap_from_edge = 100
    place_width = 50
    place_spacer = 2
    for i in range(2):
        for j in range(2):
            for k in range(8):
                rectangle = Rectangle(Point((1-i)*k*(place_width + place_spacer) + i*j*7*(place_width + place_spacer) + gap_from_edge, i*k*(place_width + place_spacer) + (1-i)*j*7*(place_width + place_spacer)+ gap_from_top), Point((1-i)*(k+1)*(place_width) + (1-i)*k*place_spacer + i*(place_width) + i*j*7*(place_width + place_spacer) + gap_from_edge, gap_from_top + (1-i)*(place_width) + (1-i)*j*7*(place_width + place_spacer) + i*(k+1)*(place_width) + i*k*place_spacer))
                rectangle.setFill("white")
                rectangle.draw(win)
    
    board_centre_image = Image(Point(5,5), "bc.jpg")

    board_centre_image.draw(win)
    
    win.getMouse() # pause for click in window
    win.close()
    
main()