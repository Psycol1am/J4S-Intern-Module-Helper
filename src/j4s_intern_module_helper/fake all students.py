import pandas as pd
from faker import Faker
import random
import string

fake = Faker()
num_rows = 950
num_rows2 = 50
data = []
for i in range(num_rows):
    student_id = fake.random_number(digits=8, fix_len=True)
    email = f"{student_id}@stu.mmu.ac.uk"
    first_name = fake.first_name()
    last_name = fake.last_name()
    row = {
        'First name': first_name,
        'Last name': last_name,
        'Username': email,
    }
    data.append(row)

for i in range(num_rows2):
    student_id = fake.random_number(digits=8, fix_len=True)
    email = f"{student_id}@stu.mmu.ac.uk"
    first_name = fake.first_name()
    row = {
        'First name': first_name,
        'Last name': "",
        'Username': email,
    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv('all_students.csv', index=False)

# --- Create gradesheet.csv using the same random data as above ---
gradesheet_data = []
marker = random.choice(["Ellen", "John", "Mark"])
for _, row in df.iterrows():
    gradesheet_row = {
        'Sub ID': fake.random_number(digits=7, fix_len=True),
        'Submission id': fake.bothify(text='X????????', letters=string.ascii_lowercase + string.digits),
        'Surname/Name': f"{row['Last name']} {row['First name']}",
        'Username': row['Username'],
        'Submission time': random.choice(["On Time", "Late"]),
        'Grade': fake.random_int(min=0, max=100),
        'Feedback comment': fake.sentence(),
        'Marker': marker
    }
    gradesheet_data.append(gradesheet_row)

# Now, replace the last 50 rows with missing values as specified
for i in range(1, 51):
    idx = -i
    gradesheet_data[idx]['Sub ID'] = ""
    gradesheet_data[idx]['Submission id'] = ""
    gradesheet_data[idx]['Submission time'] = ""
    gradesheet_data[idx]['Grade'] = ""
    gradesheet_data[idx]['Feedback comment'] = ""

gradesheet_df = pd.DataFrame(gradesheet_data)
gradesheet_df = gradesheet_df.iloc[:1000]  
gradesheet_df.to_csv('gradesheet.csv', index=False)

# --- Create a copy with all feedback comments blank ---
gradesheet_no_feedback = gradesheet_df.copy()
gradesheet_no_feedback['Feedback comment'] = ""
gradesheet_no_feedback.to_csv('gradesheet_no_feedback.csv', index=False)

markers = ["John", "Ellen", "Mark"]
students_per_marker = len(gradesheet_df) // len(markers)
for i, marker in enumerate(markers):
    start = i * students_per_marker
    # For the last marker, include any remainder students
    end = (i + 1) * students_per_marker if i < len(markers) - 1 else len(gradesheet_df)
    marker_df = gradesheet_df.iloc[start:end].copy()
    marker_df['Marker'] = marker
    marker_df.to_csv(f'gradesheet_{marker.lower()}.csv', index=False)

