# database_setup.py
# FINAL version with a more structured database for the new details page.

import sqlite3
import os

# --- Boilerplate to find and connect to the database ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Drop all tables to ensure a clean start ---
cursor.execute('DROP TABLE IF EXISTS job_details') # We are removing this old table
cursor.execute('DROP TABLE IF EXISTS job_cutoffs')
cursor.execute('DROP TABLE IF EXISTS job_specs')   # This is a NEW table
cursor.execute('DROP TABLE IF EXISTS exam_pattern') # This is a NEW table
cursor.execute('DROP TABLE IF EXISTS jobs')

# --- Recreate all the necessary tables ---
# Main 'jobs' table (with date columns for Gemini later)
cursor.execute('''
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY, post_name TEXT, exam_name TEXT, conducting_body TEXT, "group" TEXT, 
    gazetted_status TEXT, pay_level INTEGER, salary TEXT, eligibility TEXT, 
    age_limit TEXT, pet_status TEXT,
    application_start TEXT, application_end TEXT, exam_date TEXT
);
''')
# NEW table for the large left-side card
cursor.execute('''
CREATE TABLE job_specs (
    id INTEGER PRIMARY KEY, job_id INTEGER, nationality TEXT, age_limits TEXT, 
    age_relax TEXT, edu_qual TEXT, attempts TEXT, physical_std TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);
''')
# NEW table for the middle card
cursor.execute('''
CREATE TABLE exam_pattern (
    id INTEGER PRIMARY KEY, job_id INTEGER, stages TEXT, num_papers TEXT, 
    q_type TEXT, duration TEXT, marking_scheme TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);
''')
# Cutoffs table (unchanged structure)
cursor.execute('''CREATE TABLE job_cutoffs (id INTEGER PRIMARY KEY, job_id INTEGER, category TEXT, cutoff_score TEXT, year INTEGER, FOREIGN KEY (job_id) REFERENCES jobs (id));''')


# --- All 12 Job Posts (from your CSV or previous data) ---
jobs_data = [('IAS Officer', 'UPSC CSE', 'UPSC', 'A', 'Gazetted', 10, '₹56,100+', 'Any Graduation', '21-32', 'No PET'), ('IPS Officer', 'UPSC CSE', 'UPSC', 'A', 'Gazetted', 10, '₹56,100+', 'Any Graduation', '21-32', 'PET Required'), ('IFS Officer', 'UPSC CSE', 'UPSC', 'A', 'Gazetted', 10, '₹60,000+', 'Any Graduation', '21-32', 'No PET'), ('RBI Grade B', 'RBI Grade B Exam', 'RBI', 'A', 'Gazetted', 10, '₹70,000+', 'Graduation (50%+)', '21-30', 'No PET'), ('SBI PO', 'SBI PO Exam', 'SBI', 'A', 'Gazetted', 7, '₹40,000+', 'Any Graduation', '21-30', 'No PET'), ('IBPS PO', 'IBPS PO Exam', 'IBPS', 'A', 'Gazetted', 7, '₹35,000+', 'Any Graduation', '20-30', 'No PET'), ('SSC CGL (AAO)', 'SSC CGL', 'SSC', 'B', 'Non-Gazetted', 8, '₹45,000+', 'Any Graduation', '18-32', 'No PET'), ('NDA Officer', 'NDA Exam', 'UPSC', 'A', 'Gazetted', 10, '₹56,100+', '10+2 (PCM)', '16.5-19.5', 'PET Required'), ('ISRO Scientist', 'ISRO ICRB', 'ISRO', 'A', 'Gazetted', 10, '₹60,000+', 'B.Tech/B.E (60%+)', '21-35', 'No PET'), ('DRDO Scientist', 'DRDO Entry Test', 'DRDO', 'A', 'Gazetted', 10, '₹60,000+', 'B.Tech/B.E (First Class)', '21-28', 'No PET'), ('Railway Group A', 'UPSC ESE', 'UPSC', 'A', 'Gazetted', 10, '₹56,100+', 'B.Tech/B.E', '21-30', 'No PET'), ('LIC AAO', 'LIC AAO Exam', 'LIC', 'B', 'Non-Gazetted', 8, '₹40,000+', 'Any Graduation', '21-30', 'No PET')]
for job in jobs_data:
    cursor.execute('INSERT INTO jobs VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)', job)

# --- Sample Data for the NEW tables (for Job ID 1: UPSC CSE) ---
cursor.execute("INSERT INTO job_specs VALUES (NULL, 1, 'Citizen of India', '21-32 years', 'SC/ST: 5 years, OBC: 3 years', 'Bachelors Degree from any recognized university. Final-year students can apply.', '6 (General), 9 (OBC)', 'Not applicable for most services.')")
cursor.execute("INSERT INTO exam_pattern VALUES (NULL, 1, '3 (Prelims, Mains, Interview)', '2 (Prelims), 9 (Mains)', 'Objective (Prelims), Descriptive (Mains)', '2 hours per paper', 'Prelims: -0.66 negative marking.')")

# --- Sample Cutoffs (for Job ID 1) ---
cutoffs_data = [(1, 'UR (General)', '92.51', 2023), (1, 'OBC', '89.12', 2023), (1, 'SC', '75.41', 2023), (1, 'ST', '70.71', 2023)]
cursor.executemany('INSERT INTO job_cutoffs VALUES (NULL, ?, ?, ?, ?)', cutoffs_data)


# --- Save the data and close ---
conn.commit()
conn.close()
print("✅ Database 'jobs.db' has been successfully built with the new, structured tables! 🚀")
