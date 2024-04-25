import os
import tkinter as tk

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

def instruction_page(root):
    #create new window
    new_window = tk.Toplevel(root)
    new_window.title("How to use")

    icon_path = 'GUI' + os.sep + 'Icon.ico'

    #set window icon
    new_window.iconphoto(False, tk.PhotoImage(file=icon_path))

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
    welcome_screen.after(3000, close_welcome_screen)