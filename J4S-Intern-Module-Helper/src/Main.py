from tkinter import filedialog
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile

win = tk.Tk()

win.state('zoomed')

frame = Frame(win)
frame.pack(fill=tk.BOTH, expand=True)

text = tk.Text(frame, wrap="none")


def  open_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Supported", "*.csv;*.xlsx")])
    if file_path:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            text.configure(yscrollcommand=yscroll.set)
            text.insert(END, df.to_string())
            text.pack(expand=True, fill='both')
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
            text.configure(yscrollcommand=yscroll.set)
            text.insert(END, df.to_string())
            text.pack(expand=True, fill='both')
        else:
            print("Unsupported file format")
            return
        
    
    
        
yscroll = Scrollbar(frame, orient='vertical', command=text.yview)
yscroll.pack(side='right', fill='y')


xscroll = Scrollbar(win, orient='horizontal', command=text.xview)
xscroll.pack(side='bottom', fill='x')
text.configure(xscrollcommand=xscroll.set)
        

label = tk.Label(win, text="Select a file to open:")
label.pack(pady=10)

tk.Button(win, text="Open File", command=open_file).pack(pady=20)

win.mainloop()