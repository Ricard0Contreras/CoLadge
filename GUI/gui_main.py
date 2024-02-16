from tkinter import *
import tkinter as tk
from tkinter import font
import os
import sqlite3



root = Tk()

#main window instuctions
root.title('COLadge')
root.config(bg="lightgray")
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width/3,height/1.5))
root.maxsize(width, height)#figure out what size it is currently!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111!!!!!!!!!!!!!!!!!!
frame=tk.Frame(root,bg='lightblue')
frame.place(rely=0.2,relheight=height,relwidth=width)



#other pages defined
def input_page():
    #new window
    frame=tk.Frame(root,bg='lightblue')
    frame.place(relx=0,rely=0.3,relheight=0.7,relwidth=1)
    
    #words to be displayed
    label=tk.Label(frame,text='This will be the input page', bg="lightblue", font=('Helvetica bold', 12))
    label.place(relx=10, rely=10)
    
    #rows/column
    rows_input = Scale(frame, from_=1, to=5 )
    rows_input.place(in_= label, relx=0.3, rely=0.7, anchor = CENTER)
 
    column_input = Scale(frame, from_=1, to=5, orient=HORIZONTAL)
    column_input.place(relx=0.3, rely=0.7)
    
    
    

    
'''  
    #making grid with loops
    empty_01=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    
    for x in range(5):
        for y in range(5):
            print (x,y)
            empty_01.place(relx=0.16, rely=0.45, relheight=0.05, relwidth=0.05)
           
    #empty boxes
    #will make a loop later to save space and make it look better.
    empty_01=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_01.place(relx=0.16,rely=0.45,relheight=0.05,relwidth=0.05)
    
    empty_02=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_02.place(relx=0.22,rely=0.45,relheight=0.05,relwidth=0.05)
    
    empty_03=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_03.place(relx=0.28,rely=0.45,relheight=0.05,relwidth=0.05)
    
    empty_04=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_04.place(relx=0.34,rely=0.45,relheight=0.05,relwidth=0.05)
    
    empty_05=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_05.place(relx=0.4,rely=0.45,relheight=0.05,relwidth=0.05)
    
    empty_06=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_06.place(relx=0.16,rely=0.51,relheight=0.05,relwidth=0.05)
    
    empty_07=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_07.place(relx=0.22,rely=0.51,relheight=0.05,relwidth=0.05)
    
    empty_08=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_08.place(relx=0.28,rely=0.51,relheight=0.05,relwidth=0.05)
    
    empty_09=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_09.place(relx=0.34,rely=0.51,relheight=0.05,relwidth=0.05)
    
    empty_10=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_10.place(relx=0.4,rely=0.51,relheight=0.05,relwidth=0.05)
    
    empty_11=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_11.place(relx=0.16,rely=0.57,relheight=0.05,relwidth=0.05)
    
    empty_12=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_12.place(relx=0.22,rely=0.57,relheight=0.05,relwidth=0.05)
    
    empty_13=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_13.place(relx=0.28,rely=0.57,relheight=0.05,relwidth=0.05)
    
    empty_14=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_14.place(relx=0.34,rely=0.57,relheight=0.05,relwidth=0.05)
    
    empty_15=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_15.place(relx=0.4,rely=0.57,relheight=0.05,relwidth=0.05)
    
    empty_16=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_16.place(relx=0.16,rely=0.63,relheight=0.05,relwidth=0.05)
    
    empty_17=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_17.place(relx=0.22,rely=0.63,relheight=0.05,relwidth=0.05)
    
    empty_18=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_18.place(relx=0.28,rely=0.63,relheight=0.05,relwidth=0.05)
    
    empty_19=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_19.place(relx=0.34,rely=0.63,relheight=0.05,relwidth=0.05)
    
    empty_20=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_20.place(relx=0.4,rely=0.63,relheight=0.05,relwidth=0.05)
    
    empty_21=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_21.place(relx=0.16,rely=0.69,relheight=0.05,relwidth=0.05)
    
    empty_22=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_22.place(relx=0.22,rely=0.69,relheight=0.05,relwidth=0.05)
    
    empty_23=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_23.place(relx=0.28,rely=0.69,relheight=0.05,relwidth=0.05)
    
    empty_24=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_24.place(relx=0.34,rely=0.69,relheight=0.05,relwidth=0.05)
    
    empty_25=tk.Frame(root, bg="steelblue", borderwidth=0.5)
    empty_25.place(relx=0.4,rely=0.69,relheight=0.05,relwidth=0.05)
'''


def cropping_page():
    frame=tk.Frame(root,bg='lightblue')
    frame.place(rely=0.2,relheight=height,relwidth=width)
    label=tk.Label(frame,text='This will be the cropping page', bg="lightblue", font=('Helvetica bold', 12))
    label.place(relx=0.05, rely=0.1)
    '''
    #save/load/exit feature might want to add later
    def save():
        #Code needs to be fixed later
        save_frame=tk.Button(root)
        save.add_command(label= "Save", comand=save)
        save.place(relx=0, rely=0)
        pass
 
    def load():
        #code needs to be fixed later
        load_frame=tk.Button(root)
        load.add_command(label = "Load", command= load)
        load.place(relx=0, rely=0)
        pass   
 
    mainmenu = Menu(frame)
    mainmenu.add_command(label = "Exit", command= root.destroy)
    
    root.config(menu = mainmenu)
    '''
    
    
    
def instruction_page():
    frame=tk.Frame(root,bg='lightblue')
    frame.place(rely=0.2,relheight=height,relwidth=width)
    label=tk.Label(frame,text='This will be the instruction page', bg="lightblue", font=('Helvetica bold', 12))
    label.place(relx=width/1, rely=width/1)

#create font object for boldness
label_font = font.Font(weight="bold")

#creating widget
button_quit = Button(root, text= "Exit Program", command= root.quit, bg="maroon", fg="white")
welcome_lab = Label(root, text= "Welcome to the COLadge", bg="lightgray", font=('Helvetica bold', 16,"bold"))
input_page = Button(root, text="Input Page", font=5, bd=0.5, bg="cadetblue", fg="black", command=input_page)
cropping_page = Button(root, text="Image Cropping", font=9, bd=0.5, bg="cadetblue", fg="black", command=cropping_page)
instruction_page = Button(root, text="How to use", font=9, bd=0.5, bg="cadetblue", fg="black", command=instruction_page)

#to display on screen
button_quit.pack(side = tk.TOP)
welcome_lab.pack(side = tk.TOP, pady=10)

#display buttons for different pages
input_page.pack(side=tk.LEFT, anchor=tk.N, ipadx=.001, ipady=.1, padx=5)
cropping_page.pack(side=tk.LEFT, anchor=tk.N, ipadx=.001, ipady=.1, padx=15)
instruction_page.pack(side=tk.RIGHT, anchor=tk.N, ipadx=.001, ipady=.1, padx=5)


#calling main loop
root.mainloop()

