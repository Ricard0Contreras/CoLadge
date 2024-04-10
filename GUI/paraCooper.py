from PIL import ImageDraw,ImageFont
from tkinter.messagebox import askyesno
from tkinter import Scale
import os, sys
#from tkinter.tix import *
from tkinter.ttk import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from scripts import testing
from tkinter import messagebox
import math


def close_welcome_screen():
    welcome_screen.destroy()

def create_gradient_canvas(parent, width, height, color1, color2):
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    for y in range(height):
        # Calculate the color at this point
        r = int(color1[0] * (height - y) / height + color2[0] * y / height)
        g = int(color1[1] * (height - y) / height + color2[1] * y / height)
        b = int(color1[2] * (height - y) / height + color2[2] * y / height)
        color = f'#{r:02x}{g:02x}{b:02x}'

        canvas.create_line(0, y, width, y, fill=color, tags="gradient")

    return canvas

def show_welcome_screen():
    global welcome_screen
    welcome_screen = tk.Toplevel(root)
    welcome_screen.overrideredirect(True)  # Remove the title bar
    welcome_screen.geometry("300x200")
    canvas = tk.Canvas(welcome_screen, width=300, height=200)
    canvas.pack()

    # Define the base color
    base_color = "#85586f"

    # Create a gradient background
    for i in range(200):
        shade = hex(int(0xff * (1 - i / 200)))[2:]
        color = f"#{shade}{base_color[1:]}"  # Use the same shade for R, G, and B components
        canvas.create_line(0, i, 300, i, fill=color)

    welcome_label = canvas.create_text(150, 100, text="Welcome to COLadge! Enjoy creating your collages!", fill="white", font=("Helvetica", 12))
    okay_button = tk.Button(welcome_screen, text="Okay", command=close_welcome_screen)
    okay_button.pack(pady=10)
    # Schedule closing the welcome screen after 3 seconds (3000 milliseconds)
    welcome_screen.after(10000, close_welcome_screen)

show_welcome_screen()

if __name__ == "__main__":
    root.iconbitmap(icon_path)
    main()
    root.mainloop()