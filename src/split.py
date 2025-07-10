import tkinter as tk
from tkinter import filedialog
import pandas as pd
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class SplitMixin:
    def split_grading_sheet_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Split Grading Sheet", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Please upload the file of all students that can be downloaded from moodle (Image Below). This will be used to create numerous grading sheets split by a number of students the user specifies.").pack()
        tk.Button(self.frame1, text="Select File", command=self.select_split_file).pack(pady=10)
        tk.Label(self.frame1, text="Example of all students sheet:").pack(pady=10)
        img = Image.open("data/Example All students.png")
        img = img.resize((900, 700))
        tk_img = ImageTk.PhotoImage(img)
        img_label = tk.Label(self.frame1, image=tk_img)
        img_label.image = tk_img
        img_label.pack(pady=10)

    def select_split_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")])
        if not file_path:
            return
        if file_path.endswith('.csv'):
            self.all_Students = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.all_Students = pd.read_excel(file_path)
        else:
            self.show_message("Unsupported file format.")
            return
        self.show_split_entry_page()

    def show_split_entry_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Please type the marker and then the amount of students you want them to have. You can add more markers by clk").pack(pady=10)
        marker_frame = tk.Frame(self.frame1)
        marker_frame.pack(pady=10)
        marker_entries = []
        students_left = tk.StringVar()
        students_left_label = tk.Label(self.frame1, textvariable=students_left, font=("Arial", 12, "bold"))
        students_left_label.pack(pady=5)

        def update_students_left():
            total = 0
            for _, count_entry in marker_entries:
                count_str = count_entry.get().strip()
                if count_str.isdigit():
                    total += int(count_str)
            if self.all_Students is not None:
                amount_left = len(self.all_Students) - total
                students_left.set(f"Students left to assign: {amount_left}")
            else:
                students_left.set("Students left to assign: N/A")

        def add_marker_row():
            row_frame = tk.Frame(marker_frame)
            row_frame.pack(pady=2)
            name_entry = tk.Entry(row_frame, width=20)
            name_entry.pack(side='left', padx=5)
            count_entry = tk.Entry(row_frame, width=8)
            count_entry.pack(side='left', padx=5)
            marker_entries.append((name_entry, count_entry))
            count_entry.bind("<KeyRelease>", lambda _: update_students_left())
            name_entry.bind("<KeyRelease>", lambda _: update_students_left())
            update_students_left()

        def submit_markers():
            assignments = []
            total = 0
            for name_entry, count_entry in marker_entries:
                name = name_entry.get().strip()
                count_str = count_entry.get().strip()
                if not name and not count_str:
                    continue
                if not name or not count_str.isdigit():
                    continue
                count = int(count_str)
                assignments.append((name, count))
                total += count
            if not assignments:
                self.show_message("Please enter at least one valid marker and number.")
                return
            if total > len(self.all_Students):
                self.show_message(f"Total assigned students ({total}) exceeds number of students ({len(self.all_Students)}).")
                return
            self.perform_marker_split(assignments)

        for _ in range(5):
            add_marker_row()

        tk.Button(self.frame1, text="Submit", command=submit_markers).pack(pady=10)
        tk.Button(self.frame1, text="Add Marker", command=add_marker_row).pack(pady=5)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)

    def perform_marker_split(self, assignments):
        if self.all_Students is None:
            self.show_message("No all students file loaded.")
            return
        if 'First name' not in self.all_Students.columns or 'Last name' not in self.all_Students.columns or 'Username' not in self.all_Students.columns:
            self.show_message("The grading sheet must contain 'Username','First name' and 'Last name' columns.")
            return
        if pd.isna(self.all_Students[['First name', 'Last name', 'Username']]).any().any():
            self.show_message("The grading sheet contains missing values in 'First name', 'Last name', or 'Username' columns.")
            return

        self.all_Students['Surname/Name'] = self.all_Students['Last name'] + ' ' + self.all_Students['First name'].astype(str).str.strip()
        desired_columns = ['Sub ID', 'Submission id', 'Surname/Name', 'Username', 'Submission time', 'Grade', 'Feedback comment']

        splits = []
        start = 0
        for marker, count in assignments:
            end = start + count
            split = self.all_Students.iloc[start:end].copy()
            split = split.reindex(columns=desired_columns, fill_value="-")
            splits.append((marker, split))
            start = end

        self.clear_frame1()
        tk.Label(self.frame1, text="Split Results", font=("Arial", 16, "bold")).pack(pady=10)
        try:
            notebook = ttk.Notebook(self.frame1)
            notebook.pack(expand=True, fill='both')

            for marker, split in splits:
                frame = tk.Frame(notebook)
                split_label = tk.Label(frame, text=f"Marker: {marker} ({len(split)} students)")
                split_label.pack()
                text = tk.Text(frame, wrap="none", height=8)
                text.insert(tk.END, split.to_string())
                text.config(state='disabled')
                text.pack(expand=True, fill='both')
                notebook.add(frame, text=str(marker))

            tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)
            tk.Button(self.frame1, text="Save Split Files", command=lambda: self.save_split_files(splits)).pack(pady=10)
        except Exception as e:
            self.show_message(f"Error splitting: {e}")

    def save_split_files(self, splits):
        try:
            folder = filedialog.askdirectory(title="Select Folder to Save Split Files")
            if not folder:
                return
            for marker, chunk in splits:
                marker_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in str(marker))
                file_path = f"{folder}/grading_sheet_{marker_name}.csv"
                chunk.to_csv(file_path, index=False)
            self.show_message("All split files have been saved.")
        except Exception as e:
            self.show_message(f"Error saving files: {e}")