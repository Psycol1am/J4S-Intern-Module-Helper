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
    row = {
        'First name': fake.first_name(),
        'Last name': fake.last_name(),
        'Username': email,
    }
    data.append(row)

for i in range(num_rows2):
    # Generate a fake student ID (e.g., 8 digits)
    student_id = fake.random_number(digits=8, fix_len=True)
    email = f"{student_id}@stu.mmu.ac.uk"
    row = {
        'First name': fake.first_name(),
        'Last name': "",
        'Username': email,
    }
    data.append(row)
    
df = pd.DataFrame(data)
df.to_csv('all_students.csv', index=False)