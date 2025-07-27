import pandas as pd
from faker import Faker
import random
import string

fake = Faker()
num_rows = 950 # Number of fake rows you want
num_rows2 = 50
data = []
Marker = random.choice(["Ellen"])
for i in range(num_rows):
    # Generate a fake student ID (e.g., 8 digits)
    student_id = fake.random_number(digits=8, fix_len=True)
    email = f"{student_id}@stu.mmu.ac.uk"
    row = {
        'Sub ID': fake.random_number(digits=7, fix_len=True),
        'Submission id': fake.bothify(text='X????????', letters=string.ascii_lowercase + string.digits),
        'Surname/Name': f"{fake.last_name()} {fake.first_name()}",
        'Username': email,
        'Submission time': random.choice(["On Time", "Late"]),
        'Grade': fake.random_int(min=0, max=100),
        'Feedback comment': fake.sentence(),
        'Marker': Marker
    }
    data.append(row)

for i in range(num_rows2):
    # Generate a fake student ID (e.g., 8 digits)
    student_id = fake.random_number(digits=8, fix_len=True)
    email = f"{student_id}@stu.mmu.ac.uk"
    row = {
        'Sub ID': "",
        'Submission id': "",
        'Surname/Name': f"{""} {fake.first_name()}",
        'Username': email,
        'Submission time': random.choice(["On Time", "Late"]),
        'Grade': fake.random_int(min=0, max=100),
        'Feedback comment': fake.sentence(),
        'Marker': Marker
    }
    data.append(row)
    
df = pd.DataFrame(data)
df.to_csv('gradesheet3_SubsMissing.csv', index=False)

