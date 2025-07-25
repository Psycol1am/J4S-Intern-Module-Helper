import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import tkinter.ttk as ttk

class MergeMixin:
    def merge_grading_sheets_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Merge Grading Sheets", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="This allows you to merge multiple grading sheets into one. The output will be a single sheet containing all the students who have been graded and have valid submission ID and sub ID fields. \n "" \n Any students who had missing submissions or weren't graded will be able to be downloaded in another sheet separately.", wraplength=900).pack()
        tk.Label(self.frame1, text="Please select the grading sheets you want to merge:").pack(pady=10)
        tk.Button(self.frame1, text="Select Files", command=self.merge_popup).pack(pady=10)

    def merge_files(self, file_paths):
        dataframes = []
        columns = ['Sub ID', 'Submission id', 'Surname/Name', 'Username', 'Submission time', 'Grade', 'Feedback comment', 'Marker']
        skipped_students = []
        try:
            for file_path in file_paths:
                if file_path.endswith('.csv'):
                    dataframes.append(pd.read_csv(file_path, usecols=columns, encoding="utf-8"))
                elif file_path.endswith('.xlsx'):
                    sheets = pd.read_excel(file_path, sheet_name=None, usecols=columns)
                    for sheet in sheets.values():
                        dataframes.append(sheet)
            if dataframes:
                combined_df = pd.concat(dataframes, ignore_index=True)
                valid_rows = []
                for index, row in combined_df.iterrows():
                    # Check for missing or empty values in Sub ID, Submission id, or Grade
                    subid_missing = pd.isna(row['Sub ID']) or str(row['Sub ID']).strip() == ""
                    subid_missing = subid_missing or str(row['Sub ID']).lower() == "nan"
                    submissionid_missing = pd.isna(row['Submission id']) or str(row['Submission id']).strip() == ""
                    submissionid_missing = submissionid_missing or str(row['Submission id']).lower() == "nan"
                    grade_missing = pd.isna(row['Grade']) or str(row['Grade']).strip() == ""
                    grade_missing = grade_missing or str(row['Grade']).lower() == "nan"
                    if subid_missing or submissionid_missing or grade_missing:
                        skipped_students.append(row)
                    else:
                        feedback = row.get('Feedback comment', '')
                        marker = row.get('Marker', '')
                        if pd.notna(marker) and str(marker).strip():
                            feedback = f"{feedback} - Marked by {marker}"
                        row['Feedback comment'] = feedback
                        valid_rows.append(row)
                valid_df = pd.DataFrame(valid_rows, columns=columns)
                skipped_df = pd.DataFrame(skipped_students, columns=columns)
                if valid_df.empty:
                    self.show_message("No valid students found please check that there is at least one student who has the submission id,subID and grade columns filled in.")
                    return
                self.grading_Sheet = valid_df
                self.clear_frame1()
                tk.Label(self.frame1, text="Merged Grading Sheet", font=("Arial", 16, "bold")).pack(pady=10)

                # Viewer for merged grading sheet (similar style to split.py)
                try:
                    notebook = ttk.Notebook(self.frame1)
                    notebook.pack(expand=True, fill='both', padx=10, pady=10)

                    # Show merged sheet in a tab
                    frame = tk.Frame(notebook)
                    label = tk.Label(frame, text=f"Merged ({len(valid_df)} students)")
                    label.pack()
                    text = tk.Text(frame, wrap="none", height=15)
                    text.insert(tk.END, valid_df.to_string(index=False))
                    text.config(state='disabled')
                    text.pack(expand=True, fill='both')
                    notebook.add(frame, text="Merged Sheet")

                    # If skipped students, show in another tab
                    if not skipped_df.empty:
                        skipped_frame = tk.Frame(notebook)
                        skipped_label = tk.Label(skipped_frame, text=f"Skipped Students ({len(skipped_df)})")
                        skipped_label.pack()
                        skipped_text = tk.Text(skipped_frame, wrap="none", height=8)
                        skipped_text.insert(tk.END, skipped_df.to_string(index=False))
                        skipped_text.config(state='disabled')
                        skipped_text.pack(expand=True, fill='both')
                        notebook.add(skipped_frame, text="Skipped Students")

                    def save_merged():
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".csv",
                            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
                        )
                        if file_path:
                            if file_path.endswith('.csv'):
                                valid_df.to_csv(file_path, index=False, encoding="utf-8")
                            elif file_path.endswith('.xlsx'):
                                valid_df.to_excel(file_path, index=False)
                            self.show_message("Merged grading sheet saved.")

                    def save_skipped():
                        file_path = filedialog.asksaveasfilename(
                            defaultextension=".csv",
                            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
                        )
                        if file_path:
                            if file_path.endswith('.csv'):
                                skipped_df.to_csv(file_path, index=False, encoding="utf-8")
                            elif file_path.endswith('.xlsx'):
                                skipped_df.to_excel(file_path, index=False)
                            self.show_message("Skipped students file saved.")

                    btn_frame = tk.Frame(self.frame1)
                    btn_frame.pack(pady=10)
                    tk.Button(btn_frame, text="Save Merged Grading Sheet", command=save_merged).pack(side='left', padx=10)
                    if not skipped_df.empty:
                        tk.Button(btn_frame, text="Save Skipped Students List", command=save_skipped).pack(side='left', padx=10)
                    tk.Button(btn_frame, text="Back to Home", command=self.show_home).pack(side='left', padx=10)
                except Exception as e:
                    self.show_message(f"Error displaying merged sheet: {e}")
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
            file_path = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv;*.xlsx")], parent=popup)
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