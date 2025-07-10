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