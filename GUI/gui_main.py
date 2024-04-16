from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
import os
import sqlite3
from tkinter.filedialog import askopenfile
from tkinter import filedialog
from PIL import Image, ImageTk
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

def show_welcome_screen():
    global welcome_screen
    welcome_screen = tk.Toplevel(root)
    welcome_screen.overrideredirect(True)
    welcome_screen_width = 300
    welcome_screen_height = 200
    center_window(welcome_screen, welcome_screen_width, welcome_screen_height)
    welcome_label = tk.Label(welcome_screen, text="Welcome to COLadge! Enjoy creating your collages!", padx=20, pady=20)
    welcome_label.pack()
    okay_button = tk.Button(welcome_screen, text="Okay", command=close_welcome_screen)
    okay_button.pack(pady=10)
    #timed close
    welcome_screen.after(10000, close_welcome_screen)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_canvas():
    global canvas
    canvas_width = scaleW * 0.832
    canvas_height = scaleH * 0.293
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0)
    canvas.place(anchor='n', x=scaleW * 0.472, y=scaleH * 0.608)
    
def create_rectangles():
    global cellwidth, cellheight, rectangles
    cellwidth = (scaleW - 50) // columns
    cellheight = (scaleH - 300) // rows
    rectangles = {}
    for column in range(columns):
        for row in range(rows):
            x1 = column * cellwidth
            y1 = row * cellheight
            x2 = x1 + cellwidth
            y2 = y1 + cellheight
            rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill="#ac7d88", tags="rect")
            rectangles[(row, column)] = rectangle

def update_grid(event=None):
    global rows, columns, cellwidth, cellheight
    #get total images
    total_images = len(globalFileList)
    
    #math for x&y based on total images
    max_rows = int(math.sqrt(total_images))
    max_columns = total_images // max_rows
    while max_rows * max_columns < total_images:
        max_columns += 1
        
    #update max for scales
    row_scale.config(to=max_rows)
    column_scale.config(to=max_columns)
    
    row_scale.bind("<ButtonRelease-1>", update_grid)
    column_scale.bind("<ButtonRelease-1>", update_grid)

    #update grid based on scales
    rows = row_scale.get()
    columns = column_scale.get()

    #delete rectangles
    for rect in rectangles.values():
        canvas.itemconfig(rect, fill="#ac7d88")

    for column in range(columns):
        for row in range(rows):
            x1 = column * cellwidth
            y1 = row * cellheight
            x2 = x1 + cellwidth
            y2 = y1 + cellheight
            rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill="#97335e", tags="rect")
            rectangles[(row, column)] = rectangle

def create_scales():
    global row_scale, column_scale
    row_scale = tk.Scale(root, from_=1, to=rows, length=200, sliderlength=15, sliderrelief='flat',
                         fg='black', activebackground='#f8ecd1', troughcolor='#85586f', bg='#deb6ab', command=update_grid)
    row_scale.place(anchor='n', x=scaleW * 0.94, y=scaleH * 0.63, height= scaleH * 0.25, width=scaleW * 0.095)
    column_scale = tk.Scale(root, from_=1, to=columns, orient="horizontal", length=200, sliderlength=15,
                            sliderrelief='flat', fg='black', activebackground='#f8ecd1', troughcolor='#85586f', 
                            bg='#deb6ab', command=update_grid)
    column_scale.place(anchor='n', x=scaleW * 0.66, y=scaleH * 0.905, width= scaleW * 0.4, height= scaleH * 0.08, relheight=0.001)
    
#remember X/Y and pass data
def pass_data(imageList):
    x_input = row_scale.get()
    y_input = column_scale.get()
    print(f"Selected rows: {x_input}")
    print(f"Selected columns: {y_input}")

#FILE SELECTOR           
def on_frame_configure(canvas):
    """Reset the scroll region to encompass the inner frame."""
    canvas.configure(scrollregion=canvas.bbox("all"))

def upload_file(fileList):
    f_types = [('JPG Files and PNG Files', '*.jpg and .png*'), ('PNG Files', '*.png')]
    filenames = tk.filedialog.askopenfilenames(multiple=True, filetypes=f_types)
    #start from row 5 and column 1
    row, col = 5, 1
    row += int(len(globalFileList) / 3)
    col += len(globalFileList) % 3

    for files in filenames:
        #print(fileList)
        globalFileList.append(files)

    labelsListLen = len(labelsList)

    for i in range(len(filenames[i])):
        img = Image.open(filenames[i])
        img = img.resize((100, 100))  #resize the image
        img = ImageTk.PhotoImage(img)
        label.index = i + labelsListLen
        label.bind("<Button-1>",lambda event, lab = label: delete_file(globalFileList, lab))
        #create a label to display the image
        label = tk.Label(frame, text="", font=("Arial", 70), image=img, compound="center")
        label.grid(in_=frame, row=row, column=col)
        label.image = img  # Keep a reference!
        label.bind("<Enter>", lambda event, lab=label: changeImage(lab))
        label.bind("<Leave>", lambda event, lab=label: returnImage(lab))
        labelsList.append(label)
        #Displays the name of all the labels and remove the ones that have been deleted
        print("Number of pictures in Label List: ", len(labelsList))
        print("Upload File: " + str(labelsList))
        print("Number of pictures in file List: ", len(globalFileList))
        print()
        
        #show the image
        if col == 3:
            #start a new line after the third column
            row += 1
            col = 1
        else:
            #within the same row
            col += 1

def delete_file(fileList, label):
    #if label.index < len(fileList):
    #deletes the file name of the image deleted
    index = label.index
    label.destroy()

    for i in range(index, len(labelsList)):
        labelsList[i].index -= 1
    del fileList[index]
    del labelsList[index]

    print("Delete File: " + str(labelsList))
    print()
    update_labels()

def update_labels():
    global labelsList
    #start from row 5 and column 1
    row, col = 5, 1
    tempLabelsList = []
    tempIndex = 0

    print("Update Labels: " + str(labelsList))
    print()
    for label in labelsList:
        image = label.image
        newLabel = tk.Label(frame, text="", font=("Arial", 70), image=image, compound="center")
        newLabel.grid(in_=frame, row=row, column=col)
        newLabel.image = image  # Keep a reference!

        newLabel.index = tempIndex
        newLabel.bind("<Button-1>",lambda event, lab = newLabel: delete_file(globalFileList, lab))
        newLabel.bind("<Enter>", lambda event, lab=newLabel: changeImage(lab))
        newLabel.bind("<Leave>", lambda event, lab=newLabel: returnImage(lab))
        tempLabelsList.append(newLabel)
            
        if col == 3:
            #start a new line after the third column
            row += 1
            col = 1
        else:
            #within the same row
            col += 1
            tempIndex += 1


        for i in range(len(labelsList) - 1, -1, -1):
            label = labelsList[i]
            label.destroy()
            del labelsList[i]
            
        for lab in tempLabelsList:
            labelsList.append(lab)

def changeImage(label):
    label.config(text="X", foreground="red")

def returnImage(label):
    label.config(text="")
    
class CustomTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_visible = False

        #bind events to show/hide the tooltip
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if not self.tooltip_visible:
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            self.tooltip_label = tk.Label(text=self.text, background="lightyellow", relief="solid", borderwidth=1)
            self.tooltip_label.place(x=x, y=y)
            self.tooltip_visible = True

    def hide_tooltip(self, event):
        if self.tooltip_visible:
            self.tooltip_label.place_forget()
            self.tooltip_visible = False

def create_main_frame():
    global myframe, frame, myscrollbar
    frame_width = scaleW * 0.9
    frame_height = scaleH * 0.626
    canvas_width = frame_width * 0.9
    canvas_height = frame_height * 0.626
    # create the main frame
    myframe = tk.Frame(root, relief=tk.GROOVE, bd=4, bg='#deb6ab', width=frame_width, height=frame_height,
                       highlightbackground="#85586f", highlightcolor="#85586f")
    myframe.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.18)
    # create a canvas inside the main frame
    canvas = tk.Canvas(myframe, width=canvas_width, height=canvas_height, bg='#deb6ab', highlightbackground="#85586f", highlightcolor="#85586f")
    canvas.pack(side="left")
    # create a custom style for the vertical scrollbar
    style = ttk.Style()
    style.configure("Vertical.TScrollbar", troughcolor='#685dce', background='#685dce',
                    gripcount=0, arrowsize=15, gripcolor='#ac6cda', troughrelief='flat', gripborderwidth=0)
    # create the vertical scrollbar
    myscrollbar = ttk.Scrollbar(myframe, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right", fill="y")
    # attach the scrollable frame to the canvas
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')
    # bind the function to the frame's configuration event
    frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))

def find_word(text_widget, word):
    #start from beginning
    start_index = "1.0"
    while True:
        #search for the word from the start index
        pos = text_widget.search(word, start_index, stopindex=tk.END)
        if not pos:
            break
        #return position of word
        yield pos
        #update start index to continue searching
        start_index = f"{pos}+{len(word)}c"

def instruction_page():
    #create new window
    new_window = tk.Toplevel(root)
    new_window.title("How to use")
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "COLadge_Icon.ico")

    #set window icon
    new_window.iconbitmap(icon_path)

    #sizing
    width, height = new_window.winfo_screenwidth(), root.winfo_screenheight()
    scaleW = int(width * 0.25)
    scaleH = int(height * 0.51)
    new_window.geometry(f"{scaleW}x{scaleH}+0+0")
    new_window.maxsize(scaleW, scaleH)
    new_window.minsize(scaleW, scaleH)

    #text for instructions
    instruction_body = tk.Text(new_window, wrap="word", bg="#36393e", fg="white", font=('Helvetica', 9), height=30)
    instruction_body.tag_configure("bold", font=('Helvetica', 9, 'bold'))
    instruction_body.tag_configure("big_bold", font=('Helvetica', 12, 'bold'))
    instruction_body.tag_configure("darker_color", foreground="#ae8a8c")
    instruction_body.tag_configure("mid_color", foreground="#deb6ab")
    instruction_body.tag_configure("lighter_color", foreground="#f8ecd1")
    #insert text
    instruction_body.insert(tk.END, """
                      CoLodge User Manuel

    Name:
            Color Collage
                                        
    Description:
            User-friendly program used to create a collage of
            images that are automatically sorted by their colors.
                                        
    Using Input Form:
            Using Images
                    - Add images by clicking the 'Upload Files'
                    button. You will be able to scroll through
                    the images you add by using the scroll bar
                    to the right.
            Deleting Images
                    - Hover over an image you wish to remove and
                    click on the red X that appears to delete.
            Selecting Collage Size
                    - Use the scrollers on the bottom half of the
                    window to change your rows (x) and columns
                    (y) to customize what final size you would
                    like your collage to be.
            Create Collage
                    - After images and size variable criteria have
                    been met, click the 'Make Collage' button to
                    begin compiling your color collage.""")

     #apply tags to specific words
    for word in ["CoLodge User Manuel", "Name:", "Description:", "Using Input Form:", "Using Images", "Deleting Images", "Selecting Collage Size", "Create Collage"]:
        for pos in find_word(instruction_body, word):
            end = f"{pos}+{len(word)}c"
            if word == "Name:":
                instruction_body.tag_add("bold", pos, end)
                instruction_body.tag_add("mid_color", pos, end)
            elif word in ["Description:", "Using Input Form:"]:
                instruction_body.tag_add("bold", pos, end)
                instruction_body.tag_add("bold", pos, end)
                instruction_body.tag_add("mid_color", pos, end)
            elif word in ["CoLodge User Manuel"]:
                instruction_body.tag_add("big_bold", pos, end)
                instruction_body.tag_add("darker_color", pos, end)
                
            elif word in ["Using Images", "Deleting Images", "Selecting Collage Size", "Create Collage"]:
                instruction_body.tag_add("bold", pos, end)
                instruction_body.tag_add("lighter_color", pos, end)

    instruction_body.config(state=tk.DISABLED)
    instruction_body.pack()

def main():
    create_canvas()
    create_rectangles()
    create_scales()
    create_main_frame()
    
#INNICIATION OF PLACEMENTS
root = tk.Tk()
root.title('COLadge')
root.config(bg='#36393e')
#icon path
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "COLadge_Icon.ico")

#program dimensions
scaleW = int(root.winfo_screenwidth() * 0.3)
scaleH = int(root.winfo_screenheight() * 0.6)
root.maxsize(scaleW, scaleH)
root.minsize(scaleW, scaleH)
globalFileList = []
labelsList = []
#center the window
center_window(root, scaleW, scaleH)

#INPUT PAGE DETAILS
#new window
frame=tk.Frame(root, bg='#36393e')
frame.place(x=25, y=25)
rect = {}
rows = 20
columns = 20
cellwidth = 0
cellheight = 0

#update button for X&Y
update_button = tk.Button(root, text="Make CoLadge", bg='#f8ecd1', fg='black', activebackground="#97335e", command= lambda: pass_data(globalFileList))
update_button.place(in_=frame, anchor='n', x=scaleW * 0.07, y=scaleH * 0.88)

#welcome label
welcome_lab = tk.Label(root, text="COLadge", bg='#36393e', fg='#ae8a8c',  font=('Helvetica bold', 16, "bold"))
welcome_lab.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.04)

#how to Use button
instruction_page = tk.Button(root, text="?", bd=0.5, bg="#f8ecd1", fg="black", activebackground='#97335e', width=1, command=instruction_page)
instruction_page.place(anchor='n', x=scaleW * 0.028, y=scaleH * 0.01)

show_welcome_screen()

if __name__ == "__main__":
    root.iconbitmap(icon_path)
    # file selector button
    b1 = tk.Button(root, text='Upload Files', width=20, bg='#f8ecd1', activebackground="#97335e", command=lambda: upload_file(globalFileList))
    b1.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.12)
    tooltip = CustomTooltip(instruction_page, "Instructions on how to use COLadge")
    t = CustomTooltip(b1, "Allows user to upload images")
    tu = CustomTooltip(update_button, "Begin creating collage")
    main()
    root.mainloop()