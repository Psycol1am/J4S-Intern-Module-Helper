import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import J4SInternModuleHelper
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = J4SInternModuleHelper(root)
    root.mainloop()