import pandas as pd
from faker import Faker
import random
import string

fake = Faker()
num_rows = 950 
num_rows2 = 50
data = []
for i in range(num_rows):
    # Generate a fake student ID (e.g., 8 digits)
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


submitted_data = []
for _, row in df.iterrows():
    submitted_row = {
        'Sub ID' : fake.random_number(digits=7, fix_len=True),
        'Submission id': fake.bothify(text='X????????', letters=string.ascii_lowercase + string.digits),
        'Surname/Name': f"{row['Last name']} {row['First name']}",
        'Username': row['Username'],
        'Submission time': random.choice(["On Time", "Late"]),
        'Grade': "",
        'Feedback comment': "",
        'Marker': "" 
    }
    submitted_data.append(submitted_row)

submitted_df = pd.DataFrame(submitted_data)
submitted_df = submitted_df.drop(submitted_df.sample(n=100, random_state=42).index)
submitted_df.to_csv('submitted.csv', index=False)

