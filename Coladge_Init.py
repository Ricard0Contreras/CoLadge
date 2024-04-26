from threading import Thread
import tkinter as tk
from tkinter import ttk
import os, sys, sqlite3, time, queue
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import ImageDraw,ImageFont
import numpy as np
from GUI import manual
from Scripts import miojo


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
    total_images = len(globalFileList)
    
    max_rows = total_images // columns if columns > 0 else 1
    max_columns = total_images // rows if rows > 0 else 1
    
    row_scale.config(to=max_rows)
    column_scale.config(to=max_columns)
    row_scale.bind("<ButtonRelease-1>", update_grid)
    column_scale.bind("<ButtonRelease-1>", update_grid)
    
    rows = max(1, row_scale.get())  # Ensure rows is at least 1
    columns = max(1, column_scale.get())  # Ensure columns is at least 1

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
    total_images = len(globalFileList)
    max_rows = max(1, int(np.sqrt(total_images)))
    max_columns = total_images // max_rows if max_rows > 0 else 0
    while max_rows * max_columns < total_images:
        max_columns += 1

    row_scale = tk.Scale(root, from_=1, to=max_rows, length=200, sliderlength=15, sliderrelief='flat',
                         fg='black', activebackground='#f8ecd1', troughcolor='#85586f', bg='#deb6ab', command=update_grid)
    row_scale.place(anchor='n', x=scaleW * 0.94, y=scaleH * 0.61, height= scaleH * 0.29, width=scaleW * 0.095)
    row_scale.set(1)  # Set initial value to 1

    column_scale = tk.Scale(root, from_=1, to=max_columns, orient="horizontal", length=200, sliderlength=15,
                            sliderrelief='flat', fg='black', activebackground='#f8ecd1', troughcolor='#85586f',
                            bg='#deb6ab', command=update_grid)
    column_scale.set(1)  # Set initial value to 1
    column_scale.place(anchor='n', x=scaleW * 0.687, y=scaleH * 0.9058255, width= scaleW * 0.4, height= scaleH * 0.08, relheight=0.001)

    row_scale.bind("<ButtonRelease-1>", update_grid)
    column_scale.bind("<ButtonRelease-1>", update_grid)

    row_scale.set(max_rows)
    column_scale.set(1)  # Set initial value to 1

#remember X/Y and pass data
def pass_data(imageList):
    x_input = column_scale.get()
    y_input = row_scale.get()
    if len(imageList) > x_input * y_input:
        tk.messagebox.showerror('Error', 'Remove Pictures to fit size')
    elif len(imageList) < x_input * y_input:
        tk.messagebox.showerror('Error', 'Add more pictures to fit size')
    else:
        #print(f"Selected rows: {x_input}") #Debug
        #print(f"Selected columns: {y_input}") #Debug

        global progressbar
        progressbar.start(5)

        #Loading screen when the processing starts
        global loading_screen
        loading_screen = tk.Tk()
        loading_screen.overrideredirect(True)
        loading_screen.title("Loading")
        global loadingLabel
        loadingLabel = tk.Label(loading_screen, text="Processing ...")
        loadingLabel.pack()
        center_window(loading_screen, 150, 75)
        loading_screen.attributes('-topmost', True)
        progressbar.start(5)
        loading_screen.after(200, lambda: config_Coladge(imageList, x_input, y_input))
        loading_screen.mainloop()


def config_Coladge(imgLisg, xValue, yValue):
    q = queue.Queue()
    q2 = queue.Queue()

    global progressbar
    progressbar.start(5)
    coladgeThread = Thread(target=lambda: run_code(imgLisg, xValue, yValue,q, q2))
    #processed_picList, resultPic = run_code(imgLisg, xValue, yValue)
    coladgeThread.start() # Start processing of coladge

    coladgeThread.join() # Must finish the processing before continuing
    loading_screen.destroy()

    proccessed_picList = q.get_nowait() # Result data 
    resultPic = q2.get_nowait()

    save_picture(resultPic, proccessed_picList, str(xValue), str(yValue)) # Saving results as user desires


def run_code(imageList, xVal, yVal,q ,q2):
    time.sleep(1)
    proccessed_picList, resultPic = miojo.makeCollage(imageList, xVal, yVal)
    #return proccessed_picList, resultPic
    q.put_nowait(proccessed_picList)
    q2.put_nowait(resultPic)

'''
miojo.saveTemplate() REMEMBER TO USE IT
'''
def save_picture(pic, picList, x, y):
    def run_code():
        savePath = tk.filedialog.asksaveasfilename(title='Enter Save location', filetypes=[('PNG Files', '*.png')])
        if '.png' in savePath:
            pic.save(savePath)
            tk.messagebox.showinfo('Save Complete', 'Image saved successfully!')
        else:
            pic.save(savePath+'.png')
            tk.messagebox.showinfo('Save Complete', 'Image saved successfully!')

    save_window = tk.Toplevel(root)
    save_window.title("Save Window")
    save_window.config(bg='#36393e')

    # Toggle full screen
    def toggle_fullscreen():
        save_window.attributes("-fullscreen", not save_window.attributes("-fullscreen"))

    # Bind the full screen toggle to the Escape key
    save_window.bind("<Escape>", lambda event: toggle_fullscreen())

    title_bar = tk.Frame(save_window, bg='#ae8a8c', relief=tk.RAISED, bd=1)
    title_bar.pack(side=tk.TOP, fill=tk.X)

    title_label = tk.Label(title_bar, text="Save Window", bg='#ae8a8c', fg='black', font=('Helvetica bold', 10))
    title_label.pack(side=tk.LEFT, padx=10)

    full_screen_button = tk.Button(title_bar, text="Full Screen", bg='#f8ecd1', fg='black', command=toggle_fullscreen)
    full_screen_button.pack(side=tk.RIGHT, padx=20)

    saveTemp_button = tk.Button(title_bar, text="Save Template", bg='#f8ecd1', fg='black', command=lambda: miojo.save_template(picList, x, y))
    saveTemp_button.pack(side=tk.RIGHT, padx=10)

    save_button = tk.Button(title_bar, text="Save Picture as ...", bg='#f8ecd1', fg='black', command=lambda: run_code())
    save_button.pack(side=tk.RIGHT, padx=10)

    # Get the user's screen resolution
    screen_width = save_window.winfo_screenwidth()
    screen_height = save_window.winfo_screenheight()

    # Calculate the maximum size the image can be displayed without going off-screen
    max_width = screen_width - 100  # 100 pixels margin on each side
    max_height = screen_height - 200  # 100 pixels margin on top and bottom
    max_aspect_ratio = max_width / max_height

    # Calculate the aspect ratio of the image
    image_aspect_ratio = pic.width / pic.height

    # Determine the optimal size for the image
    if max_aspect_ratio > image_aspect_ratio:
        # Height is the limiting factor
        image_height = min(pic.height, max_height)
        image_width = int(image_height * image_aspect_ratio)
    else:
        # Width is the limiting factor
        image_width = min(pic.width, max_width)
        image_height = int(image_width / image_aspect_ratio)

    # Resize the image to fit within the calculated maximum size
    resized_pic = pic.resize((image_width, image_height))

    # Convert the resized image to ImageTk format
    image_to_display = ImageTk.PhotoImage(resized_pic)

    # Create a canvas to display the image
    canvas = tk.Canvas(save_window, width=screen_width, height=screen_height, bg='#36393e')
    canvas.pack()

    # Place the resized image on the canvas
    canvas.create_image((screen_width - image_width) // 2, (screen_height - image_height) // 2, anchor=tk.NW, image=image_to_display)

    save_window.mainloop()




#FILE SELECTOR           
def on_frame_configure(canvas):
    """Reset the scroll region to encompass the inner frame."""
    canvas.configure(scrollregion=canvas.bbox("all"))

def upload_file(fileList):
    f_types = [('JPG Files and PNG Files', '*.jpg and .png*'), ('PNG Files', '*.png')]
    filenames = tk.filedialog.askopenfilenames(multiple=True, filetypes=f_types)
    if len(filenames) == 0:
        return
    #start from row 5 and column 1
    progressbar.start(5)
    make_previews(fileList, filenames)

def load_template(fileList):
    f_types = [('Template Files', '*.npy*')]
    dirTemplates = 'Database' + os.sep + 'Templates' + os.sep
    templatePath = tk.filedialog.askopenfilename(initialdir=dirTemplates, title='Select Template', filetypes=f_types)
    if templatePath == '':
        return None
    templateData = np.load(templatePath)
    filenames = templateData
    progressbar.start(5)
    make_previews(fileList, filenames)

def make_previews(fileList, filenames):
    global globalFileList, labelsList
    row, col = 5, 1
    row += int(len(globalFileList) / 3)
    col += len(globalFileList) % 3

    # Calculate the total width of all images
    total_width = len(filenames) * 100  # Assuming each image is 100x100

    # Calculate the starting position to center the images
    start_x = (frame.winfo_width() - total_width) // 2

    for files in filenames:
        globalFileList.append(files)

    labelsListLen = len(labelsList)

    for i in range(len(filenames)):
        img = Image.open(filenames[i])
        img = img.resize((100, 100))  # Resize the image to 100x100
        img = ImageTk.PhotoImage(img)

        # Create a label to display the image
        label = tk.Label(frame, text="", font=("Arial", 70), image=img, compound="center", bg="#deb6ab")
        label.index = i + labelsListLen
        label.bind("<Button-1>", lambda event, lab=label: delete_file(globalFileList, lab))
        label.grid(in_=frame, row=row, column=col, padx=1, pady=1)  # Add padding for centering
        label.image = img  # Keep a reference!
        label.bind("<Enter>", lambda event, lab=label: changeImage(lab))
        label.bind("<Leave>", lambda event, lab=label: returnImage(lab))
        labelsList.append(label)

        # Show the image
        if col == 3:
            # Start a new line after the third column
            row += 1
            col = 1
        else:
            # Within the same row
            col += 1

    frame.update_idletasks()
    # Center the images horizontally
    for label in labelsList:
        frame.grid_rowconfigure(row, weight=1)
        frame.grid_columnconfigure(col, weight=1)
        label.grid_configure(padx=(start_x, 1))  # Set the same padding for all images in the row

    # Set consistent spacing between images
    padding_x = (frame.winfo_width() - total_width) // (len(filenames) + 1)
    for label in labelsList:
        label.grid_configure(padx=(padding_x, 1))



def delete_file(fileList, label):
    #if label.index < len(fileList):
    #deletes the file name of the image deleted
    index = label.index
    label.destroy()

    for i in range(index, len(labelsList)):
        labelsList[i].index -= 1
    del fileList[index]
    del labelsList[index]

    # print("Delete File: " + str(labelsList)) #Debug
    # print() #Degug
    update_labels()

def update_labels():
    global labelsList

    # Start from row 5 and column 1
    row, col = 5, 1

    tempLabelsList = []
    tempIndex = 0

    #print("Update Labels: " + str(labelsList)) # Debug
    #print() #Debug
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
icon_path = 'GUI' + os.sep + 'Icon.ico'

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

#welcome label
welcome_lab = tk.Label(root, text="COLadge", bg='#36393e', fg='#ae8a8c',  font=('Helvetica bold', 16, "bold"))
welcome_lab.place(anchor='n', x=scaleW * 0.5, y=scaleH * 0.04)

#Help button
instruction_page = tk.Button(root, text="?", bd=0.5, bg="#f8ecd1", fg="black", activebackground='#97335e', width=1, command=lambda: manual.instruction_page(root))
instruction_page.place(anchor='n', x=scaleW * 0.028, y=scaleH * 0.01)

# upload file button
fileSel_button = tk.Button(root, text='Upload Images', width=20, bg='#f8ecd1', activebackground="#97335e", command=lambda: upload_file(globalFileList))
fileSel_button.place(anchor='n', x=scaleW * 0.35, y=scaleH * 0.12)

#Template Button
template_button = tk.Button(root, text="Load Template", bg='#f8ecd1', fg='black', activebackground="#97335e", command= lambda: load_template(globalFileList))
template_button.place(anchor='n', x=scaleW * 0.65, y=scaleH * 0.12)

#Make Coladge Button
update_button = tk.Button(root, text="Make CoLadge", bg='#f8ecd1', fg='black', activebackground="#97335e", command= lambda: pass_data(globalFileList))
update_button.place(in_=frame, anchor='n', x=scaleW * 0.108, y=scaleH * 0.88)

# Progress bar
progressbar = ttk.Progressbar()
progressbar.step(100)
progressbar.place(anchor= 'n', x=scaleW * 0.07, y=scaleH * 0.97, width=scaleW * 0.4)

#Hover Tips
tooltip = CustomTooltip(instruction_page, "Instructions on how to use COLadge")
t = CustomTooltip(fileSel_button, "Allows user to upload images")
tu = CustomTooltip(update_button, "Begin creating collage")
#show_welcome_screen()

if __name__ == "__main__":
    #root.iconphoto(False, tk.PhotoImage(file=icon_path))
    main()
    root.mainloop()
