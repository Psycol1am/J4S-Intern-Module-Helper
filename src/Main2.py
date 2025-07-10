import tkinter as tk
from tkinter import filedialog
import pandas as pd
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox


class J4SInternModuleHelper:
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
        tk.Button(self.frame2, text="Split Grading Sheet", width=20, height=2, command=self.split_grading_sheet_page).pack(pady=20)
        tk.Button(self.frame2, text="Merge Grading Sheets", width=20, height=2, command=self.merge_grading_sheets_page).pack(pady=20)
        tk.Button(self.frame2, text="Generate Feedback", width=20, height=2, command=self.generate_feedback_page).pack(pady=20)
        tk.Button(self.frame2, text="Update Grading Sheet using Submitted", width=21, height=2, wraplength=200, command=self.update_page).pack(pady=20)

    def show_home(self):
        self.clear_frame1()
        intro = tk.Label(self.frame1, text=self.get_intro_text(), anchor="nw", justify="left", wraplength=900)
        intro.pack(pady=30, padx=30, expand=True, fill='both')

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

    def merge_grading_sheets_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Merge Grading Sheets", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Step 1: Select grading sheet files (.csv or .xlsx)").pack()
        tk.Button(self.frame1, text="Select Files", command=self.merge_popup).pack(pady=10)

    def merge_files(self,file_paths):
        dataframes = []
        columns =  ['Sub ID', 'Submission id', 'Surname/Name', 'Username', 'Submission time', 'Grade', 'Feedback comment']
        try:
            for file_path in file_paths:
                if file_path.endswith('.csv'):
                    dataframes.append(pd.read_csv(file_path, usecols=columns))
                elif file_path.endswith('.xlsx'):
                    sheets = pd.read_excel(file_path, sheet_name=None, usecols=columns)
                    for sheet in sheets.values():
                        dataframes.append(sheet)
            if dataframes:
                combined_df = pd.concat(dataframes, ignore_index=True)
                for index, row in combined_df.iterrows():
                    if (
                        pd.isna(row['Sub ID']) or
                        pd.isna(row['Submission id']) or
                        pd.isna(row['Surname/Name']) or
                        pd.isna(row['Username']) or
                        pd.isna(row['Submission time']) or
                        pd.isna(row['Grade'])
                    ):
                        raise Exception("One or more required columns contain NaN (Null/Invalid) values. Please make sure the subID, Submission id, Surname/Name, Username, Submission time and Grade columns are present and contain valid data.")
                
                self.grading_Sheet = combined_df
                self.save_gradingsheetfile()
                self.clear_frame1()
                tk.Label(self.frame1, text="Merged Grading Sheet", font=("Arial", 16, "bold")).pack(pady=10)
                text = tk.Text(self.frame1, wrap="none", height=15)
                text.insert(tk.END, combined_df.to_string())
                text.pack(expand=True, fill='both')
                tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)
            else:
                self.show_message("No valid files selected.")
        except Exception as e:
            self.show_message(f"Error merging files: {e}")


    def merge_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Select Files to Merge")
        popup.geometry("500x400")
        file_list = []
        
        listbox = tk.Listbox(popup, width=60)
        listbox.pack(pady=10)
        
        def add_file():
            file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")],parent=popup)
            if file_path and file_path not in file_list:
                file_list.append(file_path)
                listbox.insert(tk.END, file_path)
                
        def remove_file():
            selected_file = listbox.curselection()
            if selected_file:
                for index in reversed(selected_file):
                    listbox.delete(index)
                    del file_list[index]
                
        def start_merge():
            if not file_list:
                messagebox.showwarning("No Files", "Please add at least one file to merge.")
                return
            popup.destroy()
            self.merge_files(file_list)
            
        tk.Button(popup, text="Add File", command=add_file).pack(pady=5)
        tk.Button(popup, text="Merge Files", command=start_merge).pack(pady=5)
        tk.Button(popup, text="Remove Selected", command=remove_file).pack(pady=5)
        tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5)
    
    
    def generate_feedback_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Generate Feedback", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Please select a grading sheet to add feedback to:" 
                 "\n"
                 "This program supports both generating automated generic feedback based on the students score and also allows the user to write individual feedback for each student.""").pack(pady=20)
        tk.Button(self.frame1, text="Select Grading Sheet", command=self.select_feedback_file).pack(pady=10)
        
    def select_feedback_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")])
        if not file_path:
            return
        if file_path.endswith('.csv'):
            self.grading_Sheet = pd.read_csv(file_path)
            self.grading_path = file_path
        elif file_path.endswith('.xlsx'):
            self.grading_Sheet = pd.read_excel(file_path)
            self.grading_path = file_path
        else:
            self.show_message("Unsupported file format.")
            return
        self.feedback_page_part2()
        
    def feedback_page_part2(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Step 2: Select feedback type").pack(pady=10)
        tk.Button(self.frame1, text="Generate Generic Feedback", command=self.generate_generic_feedback).pack(pady=10)
        tk.Button(self.frame1, text="Write Individual Feedback", command=self.individual_feedback_page).pack(pady=10)
    
    def generate_generic_feedback(self):
        if self.grading_Sheet is None:
            self.show_message("No grading sheet loaded.")
            return
        self.clear_frame1()
        tk.Label(self.frame1, text="Generic Feedback", font=("Arial", 16, "bold")).pack(pady=10)
        try:
            for index, row in self.grading_Sheet.iterrows():
                if 'Grade' in row and pd.notna(row['Grade']):
                    grade = int(row['Grade'])
                    feedback = self.feedbacks.get(grade, "No feedback available for this grade.")
                    self.grading_Sheet.at[index, 'Feedback comment'] = feedback
            popup = tk.Toplevel(self.root)
            popup.title("Feedback Generated")
            popup.geometry("300x200")
            tk.Label(popup, text="Generic feedback has been generated for all students.").pack(pady=10)
            tk.Button(popup, text="Save Feedback", command=self.save_gradingsheetfile).pack(pady=10)
        except Exception as e:
            self.show_message(f"Error generating feedback: {e}")
            return
    
    def save_gradingsheetfile(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
            if file_path:
                if file_path.endswith('.csv'):
                    self.grading_Sheet.to_csv(file_path, index=False)
                elif file_path.endswith('.xlsx'):
                    self.grading_Sheet.to_excel(file_path, index=False)
  
    def individual_feedback_page(self):
        if self.grading_Sheet is None:
            self.show_message("No grading sheet loaded.")
            return
        self.clear_frame1()
        tk.Label(self.frame1, text="Select a student to edit feedback:", font=("Arial", 14, "bold")).pack(pady=10)

        
        listbox = tk.Listbox(self.frame1, width=80, height=20)
        listbox.pack(pady=10, padx=10, fill='x')

        try:
            for index, row in self.grading_Sheet.iterrows():
                display = f"{row.get('Surname/Name', '')} ({row.get('Username', '')}) Feedback: {row.get('Feedback comment', 'N/A')}"
                listbox.insert(tk.END, display)
        except Exception as e:
            self.show_message(f"Error loading grading sheet: {e}")

        feedback_label = tk.Label(self.frame1, text="Feedback:")
        feedback_label.pack(pady=(20, 0))
        feedback_text = tk.Text(self.frame1, width=80, height=5)
        feedback_text.pack(pady=5)

        def on_select(event):
            selection = listbox.curselection()
            if not selection:
                return
            index = selection[0]
            
            feedback = self.grading_Sheet.iloc[index].get('Feedback comment', '')
            feedback_text.delete("1.0", tk.END)
            feedback_text.insert(tk.END, feedback)

        def save_feedback():
            selection = listbox.curselection()
            if not selection:
                self.show_message("Please select a student.")
                return
            index = selection[0]
            feedback = feedback_text.get("1.0", tk.END).strip()
            self.grading_Sheet.at[index, 'Feedback comment'] = feedback
            self.show_message("Feedback saved.")

        listbox.bind('<<ListboxSelect>>', on_select)
        tk.Button(self.frame1, text="Save Feedback", command=save_feedback).pack(pady=10)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)
        

    def update_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Update Existing grading sheet", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="This will allow you to update an existing grading sheet by uploading the grading sheet and also the sheet where people have submitted doing so will dynamically update the grading sheet by inputting the submission id and sub ID fields for you ").pack(pady=10)
        tk.Label(self.frame1, text="Please select the grading sheet you want to update:").pack(pady=10)
        tk.Button(self.frame1, text="Select Grading Sheet", command=self.select_grading_sheet).pack(pady=10)
            
    def select_grading_sheet(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")])
        if not file_path:
            return
        if file_path.endswith('.csv'):
            self.grading_Sheet = pd.read_csv(file_path)
            self.grading_path = file_path
        elif file_path.endswith('.xlsx'):
            self.grading_Sheet = pd.read_excel(file_path)
            self.grading_path = file_path
        else:
            self.show_message("Unsupported file format.")
            return
        self.update_page2()
            
    def update_page2(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Step 2: Select submitted file").pack(pady=10)
        tk.Button(self.frame1, text="Select Submitted File", command=lambda: self.select_submitted_file).pack(pady=10)
    
    def select_submitted_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")])
        if not file_path:
            return
        if file_path.endswith('.csv'):
            self.submitted = pd.read_csv(file_path)
            self.update_grading_sheet()
        elif file_path.endswith('.xlsx'):
            self.submitted = pd.read_excel(file_path)
            self.update_grading_sheet()
        else:
            self.show_message("Unsupported file format.")
            return    
        
    def update_grading_sheet(self):
        if self.grading_Sheet is None or self.submitted is None:
            self.show_message("Please load both grading sheet and submitted file.")
            return
        
        if 'Submission id' not in self.submitted.columns or 'Sub ID' not in self.submitted.columns:
            self.show_message("The submitted file must contain 'Submission id' and 'Sub ID' columns.")
            return
        
        if 'Submission id' not in self.grading_Sheet.columns or 'Sub ID' not in self.grading_Sheet.columns:
            self.show_message("The grading sheet must contain 'Submission id' and 'Sub ID' columns.")
            return
        
        for index, row in self.grading_Sheet.iterrows():
            sub_id = row.get('Sub ID')
            submission_id = row.get('Submission id')
            if pd.isna(sub_id) or pd.isna(submission_id):
                continue
            match = self.submitted[self.submitted['Submission id'] == submission_id]
            if not match.empty:
                self.grading_Sheet.at[index, 'Sub ID'] = match.iloc[0]['Sub ID']
        
        self.clear_frame1()
        tk.Label(self.frame1, text="Grading Sheet Updated", font=("Arial", 16, "bold")).pack(pady=10)
        text = tk.Text(self.frame1, wrap="none", height=15)
        text.insert(tk.END, self.grading_Sheet.to_string())
        text.pack(expand=True, fill='both')
        tk.Button(self.frame1, text="Save Updated Grading Sheet", command=self.save_gradingsheetfile).pack(pady=10)
        
        
            
        
    
    
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
        
  
                
if __name__ == "__main__":
    root = tk.Tk()
    app = J4SInternModuleHelper(root)
    root.mainloop()