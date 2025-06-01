import pandas as pd
import tkinter as tk
from tkinter import *

df = pd.DataFrame(pd.read_csv('allstudents.csv'))

split_size = 100
split = [df.iloc[i:i + split_size] for i in range(0, len(df), split_size)]

for i  in range(len(split)):
    split[i].to_csv(f'allstudents{i+1}.csv')





root = tk.Tk()
root.state('zoomed')

frame = Frame(root)
frame.pack(expand=True, fill='both')


text = Text(frame, wrap='none')


yscroll = Scrollbar(frame, orient='vertical', command=text.yview)
yscroll.pack(side='right', fill='y')

text.configure(yscrollcommand=yscroll.set)
text.insert(END, df.to_string())
text.pack(expand=True, fill='both')

xscroll = Scrollbar(root, orient='horizontal', command=text.xview)
xscroll.pack(side='bottom', fill='x')
text.configure(xscrollcommand=xscroll.set)


root.mainloop()
