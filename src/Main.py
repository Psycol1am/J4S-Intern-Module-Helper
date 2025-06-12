from tkinter import filedialog
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import simpledialog

win = tk.Tk()
win.title("Moodle Feedback Helper Tool")
win.geometry("1920x1080")
win.minsize(1000,650)
win.resizable(True, True)

def default():
    global frame1,frame2,label,button
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
    
    label = tk.Label(frame1, text=Intro, font=("Arial", 20), justify="left",anchor="nw",wraplength=900)
    label.pack(expand=True, fill='both', padx=40, pady=40)
    
    def update_wraplength(event):
        wrap = max(450, min(int(event.width * 0.8), 1000))
        text =  max(12, min(20, int(event.width /50 )))
        label.config(font=("Arial", text))
        label.config(wraplength=wrap)

    frame1.bind("<Configure>", update_wraplength)
    button = tk.Button(frame2, text="Split Grading Sheet", command=split_grading_sheet)
    button.pack(pady=10, padx=10, fill='x')







def split_grading_sheet():
    global df, label
    label.config(text="Please select a grading sheet to split using the choose file button to the right.(The program only accepts both .csv and .xlsx (Excel files)) \n"
                "\n"
                "After selecting the file, use the text box to the right to enter the amount of students per marker."
                )
    button.config(text="Choose File", command=lambda: open_file('split'))
    

    
    


def  open_file(type):
    global df,button
    file_path = filedialog.askopenfilename(filetypes=[("Supported", "*.csv;*.xlsx")])
    if file_path:
        if file_path.endswith('.csv') and type == 'split':
            df = pd.read_csv(file_path)
            label.config(text="Please enter the number of students per marker in the text box below.")
            entry = tk.Entry(frame2)
            entry.pack(pady=10, padx=10, fill='x')
            button.config(text="submit", command=lambda: submit(entry.get(), df))
            button.pack(pady=10, padx=10, fill='x')
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
    text = tk.Text(new)
    text.insert(END, df.to_string())
    text.pack(expand=True, fill='both')
    
def submit(splitAmount, df):
    try:
        splitAmount = int(splitAmount)
        if splitAmount <= 0:
            raise ValueError("Number of students per marker must be a positive integer.")
        elif splitAmount%len(df) != 0:
            raise ValueError("There isnt a even split of students per marker, please a number that is divisible by the number of students in the grading sheet. Such as in a grading sheet of 100 students, you could use 10, 20, 25, 50 or 100 as the number of students per marker.")
    except ValueError as e:
        label.config(text=f"Invalid input: {e}")
        return
    
    chunks = [df[i:i + splitAmount] for i in range(0, len(df), splitAmount)]
    
    if len(chunks) == 0:
        label.config(text="No data to split. Please check your grading sheet has rows and isnt empty.")
        return
    elif len(chunks) == 1:
        label.config(text="Grading sheet does not need to be split, the number to split by would result in one file only.")
        return
    
    else:
        for i, chunk in enumerate(chunks):
            chunk.to_csv(f'split_grading_sheet_{i+1}.csv', index=False)
        label.config(text=f"Grading sheet split into {len(chunks)} files successfully!")
        button.config(text="Done", command=default)
    
    


 
        

default()
win.mainloop()