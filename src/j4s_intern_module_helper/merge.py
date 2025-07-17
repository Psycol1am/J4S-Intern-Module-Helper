import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class MergeMixin:
    def merge_grading_sheets_page(self):
        self.clear_frame1()
        tk.Label(self.frame1, text="Merge Grading Sheets", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame1, text="Step 1: Select grading sheet files (.csv or .xlsx)").pack()
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
                    if pd.isna(row['Grade']) and pd.isna(row['Submission id']) and pd.isna(row['Sub ID']):
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
                    self.show_message("No valid students found please check that the submission id,Sub ID and grade columns are not empty.")
                    return
                self.grading_Sheet = valid_df
                self.save_gradingsheetfile()
                self.clear_frame1()
                tk.Label(self.frame1, text="Merged Grading Sheet", font=("Arial", 16, "bold")).pack(pady=10)
                text = tk.Text(self.frame1, wrap="none", height=15)
                text.insert(tk.END, valid_df.to_string())
                text.pack(expand=True, fill='both')
                tk.Button(self.frame1, text="Back to Home", command=self.show_home).pack(pady=10)
                if not skipped_df.empty:
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
                    tk.Label(self.frame1, text=f"{len(skipped_df)} students skipped (Missing data in the submission ID, Sub ID, or Grade columns).").pack(pady=10)
                    tk.Button(self.frame1, text="Save Skipped Students List", command=save_skipped).pack(pady=10)
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