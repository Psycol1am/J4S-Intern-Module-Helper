import tkinter as tk
from tkinter import filedialog
import pandas as pd
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from .utils import resource_path
from tkinter import messagebox

class UpdateMixin:
    def update_grading_sheet_page(self):
        self.clear_frame1()
        self.grading_Sheet = None
        self.submitted = None

        tk.Label(self.frame1, text="Update Grading Sheet", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.frame1, text="Load Grading Sheet", command=self.load_grading_sheet).pack(pady=10)
        tk.Button(self.frame1, text="Load Submitted File", command=self.load_submitted_file).pack(pady=10)
        tk.Button(self.frame1, text="Update Grading Sheet", command=self.update_grading_sheet).pack(pady=10)
    
    
    def update_grading_sheet(self):
        if self.grading_Sheet is None or self.submitted is None:
            self.show_message("Please load both grading sheet and submitted file.")
            return

        if 'Username' not in self.grading_Sheet.columns:
            self.show_message("The grading sheet must contain a 'Username' column.")
            return

        if 'Username' not in self.submitted.columns or 'Submission id' not in self.submitted.columns or 'Sub ID' not in self.submitted.columns:
            self.show_message("The submitted file must contain 'Username', 'Submission id', and 'Sub ID' columns.")
            return

       
        submitted_valid = self.submitted.dropna(subset=['Submission id', 'Sub ID'])
        submitted_map = submitted_valid.set_index('Username')[['Submission id', 'Sub ID']].to_dict('index')

        for index, row in self.grading_Sheet.iterrows():
            username = row.get('Username')
            if pd.isna(username):
                continue
            user_info = submitted_map.get(username)
            if user_info:
                self.grading_Sheet.at[index, 'Submission id'] = user_info['Submission id']
                self.grading_Sheet.at[index, 'Sub ID'] = user_info['Sub ID']

        self.clear_frame1()
        tk.Label(self.frame1, text="Grading Sheet Updated", font=("Arial", 16, "bold")).pack(pady=10)
        text = tk.Text(self.frame1, wrap="none", height=15)
        text.insert(tk.END, self.grading_Sheet.to_string())
        text.pack(expand=True, fill='both')
        tk.Button(self.frame1, text="Save Updated Grading Sheet", command=self.save_gradingsheetfile).pack(pady=10)