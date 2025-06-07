from tkinter import filedialog
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile

win = tk.Tk()
win.title("Moodle Feedback Helper Tool")
win.geometry("1920x1080")
win.minsize(1000,650)
win.resizable(True, True)

def default():
    global frame1,frame2,label
    frame1 = tk.Frame(win)
    frame2 = tk.Frame(win)
    
    frame1.grid(row=0, column=0, sticky='nsew')
    frame2.grid(row=0, column=1, sticky='nsew')
    
    win.grid_columnconfigure(0, weight=1, uniform="group1")
    win.grid_columnconfigure(1, weight=1, uniform="group1")
    win.grid_rowconfigure(0, weight=1)
    
    
    Intro = (
        "Welcome to the Moodle Feedback helper tool\n"
        "\n"
        "This tool is designed to help with:\n"
        "\n"
        "1.Grading sheets:\n"
        "   -Split student grading sheets into multiple markers \n"
        "   -Merge multiple markers grading sheets into one\n"
        "\n"
        "2.Generic Feedback\n"
        "  -Generate generic feedback for students based on their grades\n"
        "  - Allow user to select feedback from a predefined list\n"
        "  - Allow user to write individual feedback for students\n"
        "\n"
        
        "3. Generate new graded sheet that complies with Moodle's requirements\n"
        "\n"
        "\n"
        
        "To get started, please press one of the buttons to the right.\n"
    )
    
    label = tk.Label(frame1, text=Intro, font=("Arial", 20), justify='left',anchor="nw",wraplength=900)
    label.pack(expand=True, fill='both', padx=40, pady=40)
    
    def update_wraplength(event):
        wrap = max(450, min(int(event.width * 0.8), 1000))
        text =  max(12, min(20, int(event.width /50 )))
        label.config(font=("Arial", text))
        label.config(wraplength=wrap)

    frame1.bind("<Configure>", update_wraplength)



    
    


def  open_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Supported", "*.csv;*.xlsx")])
    if file_path:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            df_view(df)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
            df_view(df)
        else:
            print("Unsupported file format")
            return
        
def df_view(df):
    new = tk.Toplevel(win)
    new.title("DataFrame View")
    text = tk.Text(win)
    text.insert(END, df.to_string())
    text.pack(expand=True, fill='both')
    
    


 
        

default()
win.mainloop()