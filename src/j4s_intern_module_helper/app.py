import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
import tkinter.ttk as ttk



from .split import SplitMixin
from .merge import MergeMixin
from .feedback import FeedbackMixin
from .utils import resource_path 

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
        filepath = resource_path("data\\generic-feedbacks.xlsx")
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
        print(self.feedbacks)

    def setup_buttons(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        tk.Button(self.frame2, text="Split Grading Sheet", width=40, height=2, command=self.split_grading_sheet_page).pack(pady=20)
        tk.Button(self.frame2, text="Merge Grading Sheets", width=40, height=2, command=self.merge_grading_sheets_page).pack(pady=20)
        tk.Button(self.frame2, text="Generate Feedback", width=40, height=2, command=self.generate_feedback_page).pack(pady=20)
        tk.Button(self.frame2, text="Upload Generic Feedback Sheet", width=40, height=2, command=self.upload_feedback_page).pack(pady=20)
        tk.Button(self.frame2, text="Update Grading Sheet using Submitted Sheet", width=40, height=2, wraplength=600, command=self.update_grading_sheet_using_submitted).pack(pady=20)
        tk.Button(self.frame2, text="Search User by ID", width=40, height=2, wraplength=400, command=self.search_student_page_select_sheet).pack(pady=20)
        tk.Label(self.frame2, text="Created and Maintained by Liam Ford. Contact at liam.ford001@gmail.com", wraplength=600).pack(pady=200)

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
            "   - Utilises moodles list of all students on a course to then create a bran new grading sheet for each marker.\n"
            "   - Merge multiple markers grading sheets into one\n"
            "\n"
            "2. Generic Feedback\n"
            "   - Generate generic feedback for students based on their grades by utilising a pre defined list built into the program or that is uploaded\n"
            "   - Allow user to select feedback from the generic feedback list\n"
            "   - Allow user to write individual feedback for students\n"
            "\n"
            "3. Update Grading Sheet\n"
            "   - Update existing grading sheets with new information from the sheet of submitted students from moodle\n"
            "\n"
            "To get started, please press one of the buttons to the right.\n"
        )
    
    def update_grading_sheet_using_submitted(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Update Grading Sheet using Submitted Sheet", font=("Arial", 16, "bold")).pack(pady=10)

        submitted_path_var = tk.StringVar()
        graded_path_var = tk.StringVar()

        def select_submitted():
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
            submitted_path_var.set(path)

        def select_graded():
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
            graded_path_var.set(path)

        tk.Button(self.frame1, text="Select Submitted Sheet", command=select_submitted).pack(pady=5)
        tk.Label(self.frame1, textvariable=submitted_path_var, wraplength=900).pack(pady=2)
        tk.Button(self.frame1, text="Select Graded Sheet", command=select_graded).pack(pady=5)
        tk.Label(self.frame1, textvariable=graded_path_var, wraplength=900).pack(pady=2)

        def run_update():
            submitted_path = submitted_path_var.get()
            graded_path = graded_path_var.get()
            if not submitted_path or not graded_path:
                self.show_message("Please select both files.")
                return

           
            if submitted_path.endswith('.csv'):
                submitted_df = pd.read_csv(submitted_path, encoding="utf-8")
            else:
                submitted_df = pd.read_excel(submitted_path)
            
            if graded_path.endswith('.csv'):
                graded_df = pd.read_csv(graded_path, encoding="utf-8")
            else:
                graded_df = pd.read_excel(graded_path)

            
            submitted_df.set_index('Username', inplace=True)

            for idx, row in graded_df.iterrows():
                username = row.get('Username')
                if pd.notna(username) and username in submitted_df.index:
                    for col in ['Sub ID', 'Submission id', 'Submission time']:
                        if col in submitted_df.columns and col in graded_df.columns:
                            graded_df.at[idx, col] = submitted_df.at[username, col]

            self.updated_grading_df = graded_df

            tk.Label(self.frame1, text="Update complete! Click below to save the updated graded sheet.").pack(pady=10)
            tk.Button(self.frame1, text="Save Updated Graded Sheet", command=save_updated).pack(pady=10)

        def save_updated():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
            if file_path:
                if file_path.endswith('.csv'):
                    self.updated_grading_df.to_csv(file_path, index=False, encoding="utf-8")
                else:
                    self.updated_grading_df.to_excel(file_path, index=False)
                self.show_message("Updated graded sheet saved.")

        tk.Button(self.frame1, text="Update Graded Sheet", command=run_update).pack(pady=20)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)
        
    def search_student_page_select_sheet(self):
        """Page to select grading sheet before searching for a student."""
        self.clear_frame1()
        tk.Label(self.frame1, text="Select a grading sheet to search for students:", font=("Arial", 16, "bold")).pack(pady=10)
        def select_sheet():
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
            if file_path:
                if file_path.endswith('.csv'):
                    self.grading_Sheet = pd.read_csv(file_path, encoding="utf-8")
                else:
                    self.grading_Sheet = pd.read_excel(file_path)
                self.search_student_page()
        tk.Button(self.frame1, text="Select Grading Sheet", command=select_sheet).pack(pady=20)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)

    def search_student_page(self):
        """Search for a student by ID/email."""
        if self.grading_Sheet is None:
            self.show_message("No grading sheet loaded.")
            return
        self.clear_frame1()
        tk.Label(self.frame1, text="Search for a student by ID/email", font=("Arial", 14, "bold")).pack(pady=10)

        search_var = tk.StringVar()
        search_entry = tk.Entry(self.frame1, textvariable=search_var, width=40)
        search_entry.pack(pady=5)
        tk.Label(self.frame1, text="Search by ID/email").pack()

        listbox = tk.Listbox(self.frame1, width=80, height=20, exportselection=False)
        listbox.pack(pady=10, padx=10, fill='x')

        self._student_display = []
        self._student_indices = []

        def populate_listbox(filter_text=""):
            listbox.delete(0, tk.END)
            self._student_display.clear()
            self._student_indices.clear()
            for index, row in self.grading_Sheet.iterrows():
                username = str(row.get('Username', ''))
                id_part = username.split('@')[0] if '@' in username else username
                display = f"{row.get('Surname/Name', '')} ({username})"
                if filter_text.lower() in username.lower() or filter_text.lower() in id_part.lower() or filter_text == "":
                    listbox.insert(tk.END, display)
                    self._student_display.append(display)
                    self._student_indices.append(index)

        def on_search(*args):
            filter_text = search_var.get()
            populate_listbox(filter_text)

        search_var.trace_add("write", on_search)

        result_text = tk.Text(self.frame1, width=80, height=10, state='disabled')
        result_text.pack(pady=10)

        def on_select(event=None):
            selection = listbox.curselection()
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            if not selection:
                result_text.insert(tk.END, "No student selected.")
            else:
                lb_index = selection[0]
                df_index = self._student_indices[lb_index]
                info = self.grading_Sheet.iloc[df_index].to_dict()
                for k, v in info.items():
                    result_text.insert(tk.END, f"{k}: {v}\n")
            result_text.config(state='disabled')

        listbox.bind('<<ListboxSelect>>', on_select)

        populate_listbox()
        if listbox.size() > 0:
            listbox.selection_set(0)
            on_select()

        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)