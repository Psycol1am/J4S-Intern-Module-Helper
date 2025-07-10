import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
import tkinter.ttk as ttk

from .split import SplitMixin
from .merge import MergeMixin
from .feedback import FeedbackMixin

class J4SInternModuleHelper(SplitMixin, MergeMixin, FeedbackMixin):
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.minsize(1920, 1080)
        self.root.state('zoomed')
        self.root.resizable(True, True)

        self.all_Students = None
        self.grading_Sheet = None
        self.submitted = None
        self.grading_path = None
        self.feedbacks = {}

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame1.grid(row=0, column=0, sticky='nsew')
        self.frame2.grid(row=0, column=1, sticky='nsew')
        self.root.grid_columnconfigure(0, weight=1, uniform="group1")
        self.root.grid_columnconfigure(1, weight=1, uniform="group1")
        self.root.grid_rowconfigure(0, weight=1)

        self.setup_buttons()
        self.show_home()
        self.load_Feedback()

    def load_Feedback(self):
        self.feedbacks = {}
        filepath = "data\\generic-feedbacks.xlsx"
        try:
            feedback = pd.read_excel(filepath, sheet_name=None)
            for _, sheet_df in feedback.items():
                for _, row in sheet_df.iterrows():
                    ranges = str(row['Marks']).split('-')
                    for i in range(int(ranges[0]), int(ranges[1])+1):
                        self.feedbacks[i] = row['Feedback']    
        except Exception as e:
            print(f"Error loading feedbacks: {e}")
        if self.feedbacks == {}:
            print("No feedbacks loaded. Please check the file path and format.")

    def setup_buttons(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        tk.Button(self.frame2, text="Split Grading Sheet", width=30, height=2, command=self.split_grading_sheet_page).pack(pady=20)
        tk.Button(self.frame2, text="Merge Grading Sheets", width=30, height=2, command=self.merge_grading_sheets_page).pack(pady=20)
        tk.Button(self.frame2, text="Generate Feedback", width=30, height=2, command=self.generate_feedback_page).pack(pady=20)
        tk.Button(self.frame2, text="Upload Generic Feedback Sheet", width=30, height=2, command=self.upload_feedback_page).pack(pady=20)

    def show_home(self):
        self.clear_frame1()
        intro = tk.Label(self.frame1, text=self.get_intro_text(), anchor="nw", justify="left", wraplength=900)
        intro.pack(pady=30, padx=30, expand=True, fill='both')

    def show_message(self, message):
        self.clear_frame1()
        tk.Label(self.frame1, text=message).pack(pady=10)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)

    def clear_frame1(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

    def get_intro_text(self):
        return (
            "Welcome to the Moodle Feedback helper tool\n"
            "\n"
            "This tool is designed to help with:\n"
            "\n"
            "1. Grading sheets:\n"
            "   - Split student grading sheets into multiple markers\n"
            "   - Merge multiple markers grading sheets into one\n"
            "\n"
            "2. Generic Feedback\n"
            "   - Generate generic feedback for students based on their grades\n"
            "   - Allow user to select feedback from a predefined list\n"
            "   - Allow user to write individual feedback for students\n"
            "\n"
            "3. Generate new graded sheet that complies with Moodle's requirements\n"
            "\n"
            "To get started, please press one of the buttons to the right.\n"
        )