# app.py
# --- FINAL, COMPLETE version with the server run command restored ---

from flask import Flask, render_template
import sqlite3
import os

# --- This part finds your database file ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')

app = Flask(__name__)

# --- This function connects to the database ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- This handles your main page ---
@app.route('/')
def index():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

# --- This handles your new, structured details page ---
@app.route('/details/<int:job_id>')
def details(job_id):
    conn = get_db_connection()
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    job_spec = conn.execute('SELECT * FROM job_specs WHERE job_id = ?', (job_id,)).fetchone()
    exam_pattern = conn.execute('SELECT * FROM exam_pattern WHERE job_id = ?', (job_id,)).fetchone()
    job_cutoffs = conn.execute('''
        SELECT * FROM job_cutoffs 
        WHERE job_id = ?
        ORDER BY
            CASE category
                WHEN 'UR (General)' THEN 1 WHEN 'OBC' THEN 2 WHEN 'OBC NCL' THEN 3
                WHEN 'SC' THEN 4 WHEN 'ST' THEN 5 ELSE 6
            END
    ''', (job_id,)).fetchall()
    conn.close()
    return render_template('details.html', job=job, job_spec=job_spec, exam_pattern=exam_pattern, cutoffs=job_cutoffs)


# --- THIS IS THE PART THAT WAS MISSING ---
# This code tells Python: "If this is the main file being run,
# then start the web server engine."
if __name__ == '__main__':
    app.run(debug=True)
