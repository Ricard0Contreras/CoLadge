from tkinter import *
import tkinter as tk
from tkinter import font
import os
import sqlite3
from tkinter.filedialog import askopenfile
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
from tkinter import Scale

root = tk.Tk()

root.title('COLadge')
root.config(bg='#232A2D')

#screen dementions 
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
scaleW = int(width * 0.3)
scaleH = int(height * 0.6)
root.geometry(f"{scaleW}x{scaleH}+0+0")
root.maxsize(scaleW, scaleH)
root.minsize(scaleW, scaleH)
globalFileList = []


#INPUT PAGE DETAILS

#new window
frame=tk.Frame(root, bg='#232A2D')
frame.place(anchor='nw', y=scaleH * 0.13 , width= scaleW, height= scaleH * 0.9)
    
#rows/column
rows_input = Scale(frame, from_=1, to=50, activebackground='lightpink', troughcolor='lightcoral', bg='darkseagreen4')
rows_input.place(in_= frame, anchor='n', x=scaleW * 0.09, y=scaleH * 0.502,  height= scaleH * 0.25, width=scaleW * 0.095)
 
column_input = Scale(frame, from_=1, to=50, orient=HORIZONTAL, activebackground='lightpink', troughcolor='lightcoral', bg='darkseagreen4')
column_input.place(in_=frame, anchor='n', x=scaleW * 0.37, y=scaleH * 0.775, width= scaleW * 0.4, height= scaleH * 0.08, relheight=0.001)
    
#define number of rows and columns
labelRows = [[' ' for _ in range(5)] for _ in range(5)]
empty_boxes = []
for row_index, row in enumerate(labelRows):
    row_boxes = []
    for cell_index, cell in enumerate(row):
        box = tk.Label(root, text=cell, width=2, height=1, bg='pink')
        box.place(x=cell_index * (scaleW * 0.055) + 130, y=row_index * (scaleH * 0.043) + 330, anchor='n')
        row_boxes.append(box)
        empty_boxes.append(row_boxes)

#update label for rows x columns
def update_label():
    selected_rows = rows_input.get()
    selected_columns = column_input.get()
    label.config(text=f"{selected_rows} x {selected_columns}")

#label to display rows x columns before you confirm an update
label = tk.Label(root, text="1 x 1", width=8, height=2, bg='#232A2D', fg='white', font=10)
label.place(in_=frame, anchor='n', x=scaleW * 0.72, y=scaleH * 0.77)

#update button for rows x columns
update_button = tk.Button(root, text="Update", command=update_label)
update_button.place(in_=frame, anchor='n', x=scaleW * 0.93, y=scaleH * 0.813)

#file selector            
def on_frame_configure(canvas):
    """Reset the scroll region to encompass the inner frame."""
    canvas.configure(scrollregion=canvas.bbox("all"))

def upload_file(fileList):
    f_types = [('JPG Files and PNG Files', '*.jpg and .png*'), ('PNG Files', '*.png')]
    filenames = tk.filedialog.askopenfilenames(multiple=True, filetypes=f_types)
    
    # Start from row 5 and column 1
    row, col = 5, 1

    for files in filenames:
        fileList.append(files)
        print(fileList)

    for files in fileList:

        img = Image.open(files)
        img = img.resize((100, 100))  # Resize the image
        img = ImageTk.PhotoImage(img)
        
        # Create a label to display the image
        label = tk.Label(frame, image=img)
        label.grid(in_=frame, row=row, column=col)
        label.image = img  # Keep a reference!
        
        # Show the image
        if col == 3:
            # Start a new line after the third column
            row += 1
            col = 1
        else:
            # Within the same row
            col += 1



#create the main frame
myframe = tk.Frame(root, relief=tk.GROOVE, bd=4, bg='#19161D')
myframe.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.2)

#create a canvas inside the main frame
canvas = tk.Canvas(myframe, width=330, height=200, bg='#8A9296')
frame = tk.Frame(canvas)

#create a vertical scrollbar
myscrollbar = tk.Scrollbar(myframe, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

#pack the scrollbar and canvas
myscrollbar.pack(side="right", fill="y")
canvas.pack(side="left")

#attach the scrollable frame to the canvas
canvas.create_window((0, 0), window=frame, anchor='nw')

#bind the function to the frame's configuration event
frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))

#file selector button
b1 = tk.Button(root, text='Upload Files', width=20, command= lambda: upload_file(globalFileList))
b1.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.12)



#INSTRUCTION PAGE DETAILS
        
def instruction_page():
    #create new window
    new_window = tk.Toplevel(root)
    new_window.title("How to use")
    #sizing
    width, height = new_window.winfo_screenwidth(), root.winfo_screenheight()
    scaleW = int(width * 0.25)
    scaleH = int(height * 0.4)
    new_window.geometry(f"{scaleW}x{scaleH}+0+0")
    new_window.maxsize(scaleW, scaleH)
    new_window.minsize(scaleW, scaleH)
    
    #words to be displayed
    label=tk.Label(new_window,text='How to use', font=('Helvetica bold', 16))
    label.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.02)    



#INNICIATION OF PLACEMENTS

#welcome label
welcome_lab = tk.Label(root, text="COLadge", bg='#232A2D', fg='white',  font=('Helvetica bold', 16, "bold"))
welcome_lab.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.04)

#how to Use button
instruction_page = tk.Button(root, text="?", bd=0.5, bg="steelblue", fg="black", width=1, command=instruction_page)
instruction_page.place(anchor='n', x=scaleW * 0.028, y=scaleH * 0.01)


root.mainloop()
