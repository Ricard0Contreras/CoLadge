from tkinter import *
import tkinter as tk
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
labelsList = []


#INPUT PAGE DETAILS

#new window
frame=tk.Frame(root, bg='#232A2D')
frame.place(x=25, y=25)
rect = {}
rows = 20
columns = 20
cellwidth = 0
cellheight = 0


def create_canvas():
    global canvas
    canvas = tk.Canvas(root, width=scaleW - 64.8, height=scaleH - 364, borderwidth=0, highlightthickness=0)
    canvas.place(anchor='n', x=scaleW * 0.52, y=scaleH * 0.618)
    
def create_rectangles():
    global cellwidth, cellheight
    cellwidth = (scaleW - 50) // columns
    cellheight = (scaleH - 300) // rows

    for column in range(columns):
        for row in range(rows):
            x1 = column * cellwidth
            y1 = row * cellheight
            x2 = x1 + cellwidth
            y2 = y1 + cellheight
            rect[row, column] = canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")

def update_grid(event=None):
    global rows, columns, cellwidth, cellheight

    #create rectangles for each cell
    for column in range(columns):
        for row in range(rows):
            x1 = column * cellwidth
            y1 = row * cellheight
            x2 = x1 + cellwidth
            y2 = y1 + cellheight
            rect[row, column] = canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")

    #update grid based on scale values
    rows = row_scale.get()
    columns = column_scale.get()

    #create new rectangles with updated grid size
    for column in range(columns):
        for row in range(rows):
            x1 = column * cellwidth
            y1 = row * cellheight
            x2 = x1 + cellwidth
            y2 = y1 + cellheight
            rect[row, column] = canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="rect")

def create_scales():
    global row_scale, column_scale
    row_scale = tk.Scale(root, from_=1, to=rows,activebackground='lightpink', troughcolor='lightcoral', bg='darkseagreen4', command=update_grid)
    row_scale.place(anchor='n', x=scaleW * 0.052, y=scaleH * 0.657, height= scaleH * 0.25, width=scaleW * 0.095)
    column_scale = tk.Scale(root, from_=1, to=columns, orient="horizontal", activebackground='lightpink', troughcolor='lightcoral', bg='darkseagreen4', command=update_grid)
    column_scale.place(anchor='n', x=scaleW * 0.4, y=scaleH * 0.915, width= scaleW * 0.4, height= scaleH * 0.08, relheight=0.001)

def main():
    create_canvas()
    create_rectangles()
    create_scales()
    
#remember X/Y and pass data
def pass_data(imageList):
    x_input = row_scale.get()
    y_input = column_scale.get()
    print(f"Selected rows: {x_input}")
    print(f"Selected columns: {y_input}")

#update button for rows x columns
update_button = tk.Button(root, text="Make CoLadge", command= lambda: pass_data(globalFileList))
update_button.place(in_=frame, anchor='n', x=scaleW * 0.8, y=scaleH * 0.88)

#FILE SELECTOR           
def on_frame_configure(canvas):
    """Reset the scroll region to encompass the inner frame."""
    canvas.configure(scrollregion=canvas.bbox("all"))

def upload_file(fileList):
    f_types = [('JPG Files and PNG Files', '*.jpg and .png*'), ('PNG Files', '*.png')]
    filenames = tk.filedialog.askopenfilenames(multiple=True, filetypes=f_types)

    # Start from row 5 and column 1
    row, col = 5, 1
    row += int(len(globalFileList) / 3)
    col += len(globalFileList) % 3
    
    for files in filenames:
        globalFileList.append(files)
    
    labelsListLen = len(labelsList)

    for i in range(len(filenames)):

        img = Image.open(filenames[i])
        img = img.resize((100, 100))  # Resize the image
        img = ImageTk.PhotoImage(img)
        
        # Create a label to display the image
        label = tk.Label(frame, text="", font=("Arial", 70), image=img, compound="center")
        label.grid(in_=frame, row=row, column=col)
        label.image = img  # Keep a reference!
        label.index = i + labelsListLen
        label.bind("<Button-1>",lambda event, lab = label: delete_file(globalFileList, lab))
        label.bind("<Enter>", lambda event, lab=label: changeImage(lab))
        label.bind("<Leave>", lambda event, lab=label: returnImage(lab))
        labelsList.append(label)
        #Displays the name of all the labels and remove the ones that have been deleted
        print("Number of pictures in Label List: ", len(labelsList))
        print("Upload File: " + str(labelsList))
        print("Number of pictures in file List: ", len(globalFileList))
        print()
        
        # Show the image
        if col == 3:
            # Start a new line after the third column
            row += 1
            col = 1
        else:
            # Within the same row
            col += 1

def delete_file(fileList, label):

    #if label.index < len(fileList):
    
    # Deletes the file name of the image deleted
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
    
    # Start from row 5 and column 1
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
            # Start a new line after the third column
            row += 1
            col = 1
        else:
            # Within the same row
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

        # Bind events to show/hide the tooltip
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

# INSTRUCTION PAGE DETAILS

def instruction_page():
    #create new window
    new_window = tk.Toplevel(root)
    new_window.title("How to use")
    
    #sizing
    width, height = new_window.winfo_screenwidth(), root.winfo_screenheight()
    scaleW = int(width * 0.25)
    scaleH = int(height * 0.49)
    new_window.geometry(f"{scaleW}x{scaleH}+0+0")
    new_window.maxsize(scaleW, scaleH)
    new_window.minsize(scaleW, scaleH)
    
    #text for instructions
    instruction_body = tk.Text(new_window, wrap="word", bg="#232A2D", fg="white", font=('Helvetica', 9), height=30)
    instruction_body.tag_configure("underline", underline=True)
    instruction_body.tag_configure("bold", font=('Helvetica', 9, 'bold'))
#for bold and underline, I have to know the indexes for the words I want bolded and underlined. Haven't done this yet.
    instruction_body.insert(tk.END, """
                                 CoLodge User Manuel

Name
        Color Colloge
                                    
Description
        User friendly program used to create a collage of
        images that are automatically sorted by their colors.
                                    
Using Input Form
        Using Images
               - Add images by clicking the 'Upload Files' button.
                 You will be able to scroll through the images you
                 add by using the scroll bar to the right.
        Deleting Images
               - Hover over an image you wish to remove and
                 click on the red X that appears to delete.
        Selecting Collage Size
               - Use the scrollers on the bottom half of the
                 window to change your rows (x) and columns (y)
                 to customize what final size you would like
                 your collage to be.
        Create Collage
               - After images and size variable criteria has
                 been met, click the 'Make Collage' button to
                 begin compiling your color collage.""")
                 
    instruction_body.config(state=tk.DISABLED)
    instruction_body.pack()



#INNICIATION OF PLACEMENTS

#welcome label
welcome_lab = tk.Label(root, text="COLadge", bg='#232A2D', fg='white',  font=('Helvetica bold', 16, "bold"))
welcome_lab.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.04)

#how to Use button
instruction_page = tk.Button(root, text="?", bd=0.5, bg="steelblue", fg="black", width=1, command=instruction_page)
instruction_page.place(anchor='n', x=scaleW * 0.028, y=scaleH * 0.01)

if __name__ == "__main__":
    tooltip = CustomTooltip(instruction_page, "Instructions on how to use COLadge")
    t = CustomTooltip(b1, "Allows user to upload images")
    tu = CustomTooltip(update_button, "Begin creating collage")
    main()
    root.mainloop()
