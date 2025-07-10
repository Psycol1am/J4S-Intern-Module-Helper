import tkinter as tk
from tkinter import filedialog
import pandas as pd
import shutil

class FeedbackMixin:
    def generate_feedback_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Generate Feedback", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Please select a grading sheet to add feedback to:\nThis program supports both generating automated generic feedback based on the students score and also allows the user to write individual feedback for each student.").pack(pady=20)
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

        
        dest_path = "data\\generic-feedbacks.xlsx"

        try:
            
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            if not {'Marks', 'Feedback'}.issubset(df.columns):
                self.show_message("The file must contain 'Marks' and 'Feedback' columns.")
                return

           
            if file_path.endswith('.csv'):
                
                df.to_excel(dest_path, index=False)
            else:
                shutil.copy(file_path, dest_path)

            self.show_message("Feedback sheet uploaded successfully. Reloading feedbacks...")
            self.load_Feedback()
        except Exception as e:
            self.show_message(f"Error uploading feedback sheet: {e}")