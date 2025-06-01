import pandas as pd
import tkinter as tk
from tkinter import *

df = pd.DataFrame(pd.read_csv('allstudents.csv'))


root = tk.Tk()
root.state('zoomed')

frame = Frame(root)
frame.pack(expand=True, fill='both')


text = Text(frame, wrap='none')


yscrollbar = Scrollbar(frame, orient='vertical', command=text.yview)
yscrollbar.pack(side='right', fill='y')

text.configure(yscrollcommand=yscrollbar.set)
text.insert(END, df.to_string())
text.pack(expand=True, fill='both')

xscroll = Scrollbar(root, orient='horizontal', command=text.xview)
xscroll.pack(side='bottom', fill='x')
text.configure(xscrollcommand=xscroll.set)


root.mainloop()
