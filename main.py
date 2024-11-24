# ======================================
import tkinter as tk
from tkinter import Canvas
import random
import threading
import time

COLOR_LIST = ["red2", "dodgerblue", "gold"]
SIZE_LIST = [(25, 25, 50, 50), (50, 50, 100, 100), (75, 75, 150, 150)]

BALL_OBJECTS = dict()
CONTINUE_ANIMATION = False
SELECTED_COLOR = None
SELECTED_SIZE = None
# ======================================

# ---------------------------------
# Setters
# ---------------------------------
def set_color(color: str) -> None:
    """
    Sets the selected color for the ball.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> SELECTED_COLOR
    
    Parameters:
        color (str): The color to set.
    
    Returns:
        None
    """
    global SELECTED_COLOR
    SELECTED_COLOR = color  

# ---------------------------------
#  Util
# ---------------------------------
def _move_ball(canvas: Canvas, ovalID: int) -> None:
    """
    Helper function that determines the next coordinates of the ball and moves it.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> BALL_OBJECTS
    
    Parameters:
        canvas (tkinter.Canvas): The canvas on which the ball is moving.
        ovalID (int): ID of the oval to be moved.
    
    Returns:
        None
    """
    global BALL_OBJECTS
    global CONTINUE_ANIMATION
    
    # Loop to keep moving the ball while animation continues and ball exists in BALL_OBJECTS
    while CONTINUE_ANIMATION and ovalID in BALL_OBJECTS:
        
        # Get coordinates of the oval object to determine the next coordinates.
        ovalSpeedX, ovalSpeedY = BALL_OBJECTS[ovalID]
        ovalCoords = canvas.coords(ovalID)
        newCoords = (ovalCoords[0] + ovalSpeedX,
                     ovalCoords[1] + ovalSpeedY,
                     ovalCoords[2] + ovalSpeedX,
                     ovalCoords[3] + ovalSpeedY)
        
        # Update the coordinates of the ball.
        canvas.coords(ovalID, newCoords)
        
        # Reverse the speed if the ball hits one of the window frames.
        if newCoords[2] >= canvas.winfo_width() or newCoords[0] <= 0:
            BALL_OBJECTS[ovalID][0] = -BALL_OBJECTS[ovalID][0]
            
        if newCoords[3] >= canvas.winfo_height() or newCoords[1] <= 0:
            BALL_OBJECTS[ovalID][1] = -BALL_OBJECTS[ovalID][1]
        
        # Wait for a split second before updating again.
        # (canvas.after method causes balls to move randomly.)
        time.sleep(0.01)

def create_ball(canvas: Canvas, ballSize: tuple, ballColor: str) -> None:
    """
    Helper function that creates a ball using entered parameters.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> BALL_OBJECTS

    Parameters:
        canvas (Canvas): The canvas on which the ball is created.
        ballSize (tuple): Size of the ball as a tuple of coordinates (x0, y0, x1, y1).
        ballColor (str): Color of the ball.

    Returns:
        None
    """
    global BALL_OBJECTS
    
    # Get window frame coordinates.
    canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
    
    # Select random coordinates to place the ball.
    x0 = random.randint(0, canvas_width - ballSize[2])
    y0 = random.randint(0, canvas_height - ballSize[3])
    x1 = x0 + (ballSize[2] - ballSize[0])
    y1 = y0 + (ballSize[3] - ballSize[1])
    
    # Create the ball, using entered parameters and random coordinates.
    ovalID = canvas.create_oval(x0, y0, x1, y1, fill=ballColor)
    
    # Select random default speeds (in this case, options are: -1, 1).
    ovalSpeedX = random.choice([-1, 1])
    ovalSpeedY = random.choice([-1, 1])
    
    # Save ovalID to BALL_OBJECTS to keep track of the ball object.
    BALL_OBJECTS[ovalID] = [ovalSpeedX, ovalSpeedY]
    
    # Start moving the ball if animation is active.
    if CONTINUE_ANIMATION:
        threading.Thread(target=_move_ball, args=(canvas, ovalID)).start()

# ---------------------------------
# Main
# ---------------------------------
def start_animation(canvas: Canvas) -> None:
    """
    Function that starts the animation.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> CONTINUE_ANIMATION

    Parameters:
        canvas (tkinter.Canvas): The canvas on which the animation is played.

    Returns:
        None
    """
    global CONTINUE_ANIMATION
    
    # If CONTINUE_ANIMATION is already True, return. If not, set it to True.
    if CONTINUE_ANIMATION:
        return  
    CONTINUE_ANIMATION = True
    
    # For every ball in BALL_OBJECTS, initiate moving sequence by calling _move_ball in a new thread.
    # New thread for each ball.
    for oval in BALL_OBJECTS:
        threading.Thread(target=_move_ball, args=(canvas, oval)).start()
        
def stop_animation() -> None:
    """
    Function that stops the animation.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> CONTINUE_ANIMATION

    Parameters:
        None

    Returns:
        None
    """
    global CONTINUE_ANIMATION
    
    # Set CONTINUE_ANIMATION to False to stop the animation.
    CONTINUE_ANIMATION = False

def reset_animation(canvas: Canvas) -> None:
    """
    Function that clears the tkinter.Canvas object and BALL_OBJECTS dictionary.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> BALL_OBJECTS
    
    Parameters:
        canvas (tkinter.Canvas): The canvas to be reset.
    
    Returns:
        None
    """
    global BALL_OBJECTS
    
    # Call stop_animation function to stop the animation and clear both canvas, and BALL_OBJECTS dictionary.
    stop_animation()
    canvas.delete("all")
    BALL_OBJECTS.clear()

def speed_up_animation() -> None:
    """
    Increases the speed of all balls, keeping their directions the same.
    [AFFECTS GLOBAL SCOPE VARIABLES] -> BALL_OBJECTS
    
    Parameters:
        None
    
    Returns:
        None
    """
    global BALL_OBJECTS
    
    # Double the speed of each ball without changing their directions.
    for ball in BALL_OBJECTS:
        BALL_OBJECTS[ball][0] *= 2
        BALL_OBJECTS[ball][1] *= 2

# ---------------------------------
# GUI
# ---------------------------------
# Create main window.
root = tk.Tk()
root.title("Ball Animation")
root.geometry("1080x720")
root.resizable(False, False)

# Create empty Canvas.
canvas = Canvas(root, bg="lightgrey", width=720, height=720)
canvas.place(x=0, y=0)

# Create keypad frame.
frame = tk.Frame(root, width=360, height=360, bg="darkgrey")
frame.pack(side="right", fill="y")

# Create the buttons.
buttonStart = tk.Button(frame, text="Start", bg="slategray", fg="limegreen", width=10, height=2, command=lambda: start_animation(canvas))
buttonStop = tk.Button(frame, text="Stop", bg="slategray", fg="yellow", width=10, height=2, command=stop_animation)
buttonReset = tk.Button(frame, text="Reset", bg="slategray", fg="red", width=10, height=2, command=lambda: reset_animation(canvas))
buttonSpeedUp = tk.Button(frame, text="Speed Up", bg="mediumpurple1", width=10, height=2, command=speed_up_animation)
buttonRed = tk.Button(frame, text="Red", bg="red2", width=10, height=2, command=lambda: set_color(COLOR_LIST[0]))
buttonBlue = tk.Button(frame, text="Blue", bg="dodgerblue", width=10, height=2, command=lambda: set_color(COLOR_LIST[1]))
buttonYellow = tk.Button(frame, text="Yellow", bg="gold", width=10, height=2, command=lambda: set_color(COLOR_LIST[2]))
buttonSmall = tk.Button(frame, text="Small", bg="gray80", width=10, height=2, command=lambda: create_ball(canvas, SIZE_LIST[0], SELECTED_COLOR))
buttonMedium = tk.Button(frame, text="Medium", bg="gray55", width=10, height=2, command=lambda: create_ball(canvas, SIZE_LIST[1], SELECTED_COLOR))
buttonLarge = tk.Button(frame, text="Large", bg="gray30", width=10, height=2, command=lambda: create_ball(canvas, SIZE_LIST[2], SELECTED_COLOR))

# Placements of the buttons.
buttonStart.place(x=40, y=220)
buttonStop.place(x=40, y=300)
buttonReset.place(x=40, y=380)
buttonRed.place(x=140, y=220)
buttonBlue.place(x=140, y=300)
buttonYellow.place(x=140, y=380)
buttonSmall.place(x=240, y=220)
buttonMedium.place(x=240, y=300)
buttonLarge.place(x=240, y=380)
buttonSpeedUp.place(x=140, y=460)

root.mainloop()