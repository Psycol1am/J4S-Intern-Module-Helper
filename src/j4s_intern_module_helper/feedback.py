import tkinter as tk
from tkinter import filedialog
import unicodedata
import pandas as pd
import shutil
import tkinter.ttk as ttk
from .utils import resource_path
import unicodedata


class FeedbackMixin:
    def generate_feedback_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Generate Feedback", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Please select a grading sheet to add feedback to:\nThis program supports both generating automated generic feedback based on the students score and also allows the user to write individual feedback for each student.", wraplength=900).pack(pady=20)
        tk.Button(self.frame1, text="Select Grading Sheet", command=self.select_feedback_file).pack(pady=10)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)

    def select_feedback_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")])
        if not file_path:
            return
        if file_path.endswith('.csv'):
            self.grading_Sheet = pd.read_csv(file_path, encoding="utf-8")
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
        tk.Label(self.frame1, text="This is a feedback generation tool. Select individual feedback if you are wanting to provide personalized comments for a specific student. Otherwise, select generic feedback if you would like to provide general comments for all students based on an uploaded list of generic feedbacks.", wraplength=900).pack(pady=10)
        tk.Button(self.frame1, text="Generate Generic Feedback: Automatically selects generic feedback based on the marks that students have", command=self.generate_generic_feedback).pack(pady=10)
        tk.Button(self.frame1, text="Write Individual Feedback: Allows you to write custom feedback by clicking on and searching for students", command=self.individual_feedback_page).pack(pady=10)

    def generate_generic_feedback(self):
        if self.grading_Sheet is None:
            self.show_message("No grading sheet loaded.")
            return
        
        # Create a copy of the grading sheet for preview
        preview_sheet = self.grading_Sheet.copy()
        
        try:
            for index, row in preview_sheet.iterrows():
                if 'Grade' in row and pd.notna(row['Grade']):
                    grade = int(row['Grade'])
                    feedback = self.feedbacks.get(grade, "No feedback available for this grade.")
                    preview_sheet.at[index, 'Feedback comment'] = feedback
            
            # Show the feedback preview page
            self.show_feedback_preview(preview_sheet)
            
        except Exception as e:
            self.show_message(f"Error generating feedback: {e}")
            return

    def show_feedback_preview(self, preview_sheet):
        self.clear_frame1()
        tk.Label(self.frame1, text="Generic Feedback Preview", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Review the generated feedback below.", wraplength=900).pack(pady=5)
        
        try:
            notebook = ttk.Notebook(self.frame1)
            notebook.pack(expand=True, fill='both')

            # Tab 1: Changed feedback only - formatted view
            changed_frame = tk.Frame(notebook)
            
            # Create text widget with scrollbars for changed feedback
            changed_text_frame = tk.Frame(changed_frame)
            changed_text_frame.pack(expand=True, fill='both')
            
            changed_text = tk.Text(changed_text_frame, wrap="none", height=15, font=("Courier", 10))
            changed_v_scrollbar = tk.Scrollbar(changed_text_frame, orient='vertical', command=changed_text.yview)
            changed_h_scrollbar = tk.Scrollbar(changed_text_frame, orient='horizontal', command=changed_text.xview)
            changed_text.configure(yscrollcommand=changed_v_scrollbar.set, xscrollcommand=changed_h_scrollbar.set)
            
            # Filter to show only rows with feedback
            changed_data = preview_sheet[preview_sheet['Feedback comment'].notna() & (preview_sheet['Feedback comment'] != '')]
            if len(changed_data) > 0:
                # Create a custom formatted display with full feedback
                display_text = f"{'Student Name':<25} {'Username':<15} {'Grade':<6} {'Feedback'}\n"
                display_text += "-" * 80 + "\n"
                
                for index, row in changed_data.iterrows():
                    name = str(row.get('Surname/Name', 'Unknown'))[:24]
                    username = str(row.get('Username', 'Unknown'))[:14]
                    grade = str(row.get('Grade', 'N/A'))[:5]
                    feedback = str(row.get('Feedback comment', 'No feedback'))
                    feedback = unicodedata.normalize("NFKC", feedback)
                    
                    display_text += f"{name:<25} {username:<15} {grade:<6} {feedback}\n"
                
                changed_text.insert(tk.END, display_text)
            else:
                changed_text.insert(tk.END, "No feedback was generated.")
            changed_text.config(state='disabled')
            
            # Pack scrollbars and text widget for changed feedback
            changed_text.grid(row=0, column=0, sticky='nsew')
            changed_v_scrollbar.grid(row=0, column=1, sticky='ns')
            changed_h_scrollbar.grid(row=1, column=0, sticky='ew')
            
            changed_text_frame.grid_rowconfigure(0, weight=1)
            changed_text_frame.grid_columnconfigure(0, weight=1)
            
            notebook.add(changed_frame, text=f"Generated Feedback ({len(changed_data)} students)")

            # Tab 2: Complete sheet
            complete_frame = tk.Frame(notebook)
            
            # Create text widget with scrollbars for complete sheet
            complete_text_frame = tk.Frame(complete_frame)
            complete_text_frame.pack(expand=True, fill='both')
            
            complete_text = tk.Text(complete_text_frame, wrap="none", height=15)
            complete_v_scrollbar = tk.Scrollbar(complete_text_frame, orient='vertical', command=complete_text.yview)
            complete_h_scrollbar = tk.Scrollbar(complete_text_frame, orient='horizontal', command=complete_text.xview)
            complete_text.configure(yscrollcommand=complete_v_scrollbar.set, xscrollcommand=complete_h_scrollbar.set)
            
            complete_text.insert(tk.END, preview_sheet.to_string())
            complete_text.config(state='disabled')
            
            # Pack scrollbars and text widget for complete sheet
            complete_text.grid(row=0, column=0, sticky='nsew')
            complete_v_scrollbar.grid(row=0, column=1, sticky='ns')
            complete_h_scrollbar.grid(row=1, column=0, sticky='ew')
            
            complete_text_frame.grid_rowconfigure(0, weight=1)
            complete_text_frame.grid_columnconfigure(0, weight=1)
            
            notebook.add(complete_frame, text="Complete Sheet")

            # Apply the feedback to the actual grading sheet
            self.grading_Sheet = preview_sheet.copy()
            
            tk.Button(self.frame1, text="Save Feedback", command=self.save_gradingsheetfile).pack(pady=10)
            tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)
            
        except Exception as e:
            self.show_message(f"Error showing feedback preview: {e}")

    def save_gradingsheetfile(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"),])
        if file_path:
            if file_path.endswith('.csv'):
                self.grading_Sheet.to_csv(file_path, index=False, encoding="utf-8")
            elif file_path.endswith('.xlsx'):
                self.grading_Sheet.to_excel(file_path, index=False)

    def individual_feedback_page(self):
        if self.grading_Sheet is None:
            self.show_message("No grading sheet loaded.")
            return
        self.clear_frame1()
        tk.Label(self.frame1, text="Select a student to edit feedback (only students with a grade):", font=("Arial", 14, "bold")).pack(pady=10)

        search_var = tk.StringVar()
        search_entry = tk.Entry(self.frame1, textvariable=search_var, width=40)
        search_entry.pack(pady=5)
        tk.Label(self.frame1, text="Search by ID").pack()

        listbox = tk.Listbox(self.frame1, width=80, height=20, exportselection=False)
        listbox.pack(pady=10, padx=10, fill='x')

        self._student_display = []
        self._student_indices = []

        def populate_listbox(filter_text=""):
            listbox.delete(0, tk.END)
            self._student_display.clear()
            self._student_indices.clear()
            for index, row in self.grading_Sheet.iterrows():
                
                grade = row.get('Grade', '')
                if pd.isna(grade) or str(grade).strip() == "":
                    continue
                feedback_val = row.get('Feedback comment', '')
                if pd.isna(feedback_val) or not str(feedback_val).strip():
                    feedback_val = "Blank"
                username = str(row.get('Username', ''))
                display = f"{row.get('Surname/Name', '')} ({username}) Feedback: {feedback_val}"
                # Filter by username or ID
                if filter_text.lower() in username.lower():
                    listbox.insert(tk.END, display)
                    self._student_display.append(display)
                    self._student_indices.append(index)
                elif filter_text == "":
                    listbox.insert(tk.END, display)
                    self._student_display.append(display)
                    self._student_indices.append(index)

        def on_search(*args):
            filter_text = search_var.get()
            populate_listbox(filter_text)

        search_var.trace_add("write", on_search)

        feedback_label = tk.Label(self.frame1, text="Feedback:")
        feedback_label.pack(pady=(20, 0))
        feedback_text = tk.Text(self.frame1, width=80, height=5)
        feedback_text.pack(pady=5)

        def on_select(event=None):
            selection = listbox.curselection()
            if not selection:
                return
            lb_index = selection[0]
            df_index = self._student_indices[lb_index]
            feedback = self.grading_Sheet.iloc[df_index].get('Feedback comment', '')
            if pd.isna(feedback) or not str(feedback).strip():
                feedback = ""
            feedback_text.delete("1.0", tk.END)
            feedback_text.insert(tk.END, feedback)

        def update_and_autosave(event=None):
            selection = listbox.curselection()
            if not selection:
                return
            lb_index = selection[0]
            df_index = self._student_indices[lb_index]
            feedback = feedback_text.get("1.0", tk.END).strip()
            self.grading_Sheet.at[df_index, 'Feedback comment'] = feedback
            display_feedback = feedback if feedback else "Blank"
            row = self.grading_Sheet.iloc[df_index]
            display = f"{row.get('Surname/Name', '')} ({row.get('Username', '')}) Feedback: {display_feedback}"
            listbox.delete(lb_index)
            listbox.insert(lb_index, display)
            listbox.selection_set(lb_index)

        def save_feedback():
            self.save_gradingsheetfile()
            self.show_message("Feedback saved to file.")

        listbox.bind('<<ListboxSelect>>', on_select)
        feedback_text.bind("<KeyRelease>", update_and_autosave)

        tk.Button(self.frame1, text="Save Feedback", command=save_feedback).pack(pady=10)
        tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)

        populate_listbox()
        if listbox.size() > 0:
            listbox.selection_set(0)
        
    def upload_feedback_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Upload Generic Feedback Sheet \n This should be a excel sheet with the columns Marks and Feedback. Marks should contain a mark range such as 35-40 and then the feedback column should contain that mark brackets generic feedback such as Good job!", font=("Arial", 16),wraplength=900).pack(pady=10)
        tk.Label(self.frame1, text="Please select a feedback sheet file to upload:").pack(pady=20)
        tk.Button(self.frame1, text="Select Feedback Sheet", command=self.upload_feedback_sheet).pack(pady=10)
    
    def upload_feedback_sheet(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel or CSV files", "*.xlsx;*.csv")]
        )
        if not file_path:
            return

        dest_path = resource_path("data\\generic-feedbacks.csv")

        try:
            if file_path.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path, encoding="utf-8")
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding="latin1")
            else:
                df = pd.read_excel(file_path)
            if not {'Marks', 'Feedback'}.issubset(df.columns):
                self.show_message("The file must contain 'Marks' and 'Feedback' columns.")
                return

            df.to_csv(dest_path, index=False, encoding="utf-8")

            self.show_message("Feedback sheet uploaded successfully. Reloading feedbacks...")
            self.load_Feedback()
        except Exception as e:
            self.show_message(f"Error uploading feedback sheet: {e}")
