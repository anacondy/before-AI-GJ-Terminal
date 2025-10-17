# data_scout.py
# This script is your automated research assistant.

import sqlite3
import google.generativeai as genai
import os
import json
import time

# --- Configuration ---
# PASTE YOUR API KEY HERE
API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# --- Find the database ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')

# --- The prompt for Gemini ---
prompt_template = """
Act as an expert government exam information researcher.
Find the latest dates for the "{exam_name}" exam for the most recent or upcoming cycle.
Provide your answer ONLY in this exact JSON format:
{{
  "application_start": "YYYY-MM-DD or Not Announced",
  "application_end": "YYYY-MM-DD or Not Announced",
  "exam_date": "YYYY-MM-DD or Not Announced"
}}
Do not add any other text.
"""


def fetch_and_update_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, exam_name FROM jobs")
    jobs_to_check = cursor.fetchall()
    print("Starting the data scout to find exam updates... 🚀")

    for job in jobs_to_check:
        job_id, exam_name = job
        print(f"-> Researching: {exam_name}...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = prompt_template.format(exam_name=exam_name)
            response = model.generate_content(prompt)
            json_response = json.loads(response.text.strip().replace('`', '').replace('json', ''))

            app_start = json_response.get("application_start", "Not Announced")
            app_end = json_response.get("application_end", "Not Announced")
            exam_date = json_response.get("exam_date", "Not Announced")

            cursor.execute("""
                UPDATE jobs SET application_start = ?, application_end = ?, exam_date = ? WHERE id = ?
            """, (app_start, app_end, exam_date, job_id))
            print(f"   ...Success! Found dates for {exam_name}.")
            time.sleep(1)  # Be respectful to the API and wait a second
        except Exception as e:
            print(f"   ...Could not process data for {exam_name}. Error: {e}")

    conn.commit()
    conn.close()
    print("\nData scout has finished its mission. Database is updated! ✅")


if __name__ == '__main__':
    fetch_and_update_data()
