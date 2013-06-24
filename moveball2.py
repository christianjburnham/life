# move_erase_cycle_1.py
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from Tkinter import *
root = Tk()
root.title("move-and-erase")
cw = 230 # canvas width
ch = 130 # canvas height

chart_1 = Canvas(root, width=cw, height=ch, background="white")
chart_1.grid(row=0, column=0)
cycle_period = 50 # time between new positions of the ball
# (milliseconds).

# The parameters determining the dimensions of the ball and its
# position.
posn_x = 1 # x position of box containing the ball (bottom).
posn_y = 1 # y position of box containing the ball (left edge).
shift_x = 1 # amount of x-movement each cycle of the 'for' loop.
shift_y = 1 # amount of y-movement each cycle of the 'for' loop.
ball_width = 12 # size of ball - width (x-dimension).
ball_height = 12
color = "hot pink" # color of the ball

for i in range(1,500): # end the program after 500 position shifts.
    posn_x += shift_x
    posn_y += shift_y
    chart_1.create_oval(posn_x, posn_y, posn_x + ball_width,\
    posn_y + ball_height, fill=color)
    chart_1.update() # This refreshes the drawing on the canvas.
    chart_1.after(cycle_period) # This makes execution pause for 200
    # milliseconds.
    chart_1.delete(ALL) # This erases everything on the canvas.

root.mainloop()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
