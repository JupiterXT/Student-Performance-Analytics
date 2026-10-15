import sqlite3
import csv
import os

print("Current folder:", os.getcwd())

db_file = "student_performance.db"

# Automatically deletes the file before connecting
if os.path.exists(db_file):
    os.remove(db_file)

   
# Creates a brand new empty database file every time
connection = sqlite3.connect(db_file)
cursor = connection.cursor()
# Database cursor: enables traversal over the records in a database

cursor.execute('''CREATE TABLE IF NOT EXISTS Students(
    student_id INTEGER PRIMARY KEY,
    learner_type TEXT,
    grade_level TEXT,
    enrollment_date DATE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Courses(
    course_id INTEGER PRIMARY KEY,
    course_name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Assessments(
    assessment_id INTEGER PRIMARY KEY,
    course_id INTEGER,
    assessment_name TEXT,
    topic TEXT,
    FOREIGN KEY(course_id) REFERENCES Courses(course_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Scores(
    score_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    assessment_id INTEGER,
    score REAL,
    FOREIGN KEY(student_id) REFERENCES Students(student_id),
    FOREIGN KEY(assessment_id) REFERENCES Assessments(assessment_id)
)''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS Attendance(
    attendance_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    date  DATE,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES Students(student_id)
)''')

connection.commit()

# Opens the CSV file and insert data into the Students table
with open("Students.csv", "r") as file:
    #create a CSV reader object
    reader = csv.DictReader(file)

    # Loops through each row in the CSV file and insert data into the Students table
    for row in reader:
        cursor.execute("""
            INSERT INTO Students (
                student_id,
                learner_type,
                grade_level,
                enrollment_date
            )
            VALUES (?, ?, ?, ?)
        """, (
            row["student_id"],
            row["learner_type"],
            row["grade_level"],
            row["enrollment_date"]
        ))

# Commits the changes to the database
connection.commit()

# Progress Check
print("Students imported successfully!")

# Repeat for each tab: Courses, Assessments, Scores, and Attendance tables
with open("Courses.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT INTO Courses (
                course_id,
                course_name
            )
            VALUES (?, ?)
        """, (
            row["course_id"],
            row["course_name"]
        ))

connection.commit()
# Progress Check
print("Courses imported successfully!")

with open("Assessments.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT INTO Assessments (
                assessment_id,
                course_id,
                assessment_name,
                topic
            )
            VALUES (?, ?, ?, ?)
        """, (
            row["assessment_id"],
            row["course_id"],
            row["assessment_name"],
            row["topic"]
        ))

connection.commit()
# Progress Check
print("Assessments imported successfully!")

with open("Scores.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT INTO Scores (
                score_id,
                student_id,
                assessment_id,
                score
            )
            VALUES (?, ?, ?, ?)
        """, (
            row["score_id"],
            row["student_id"],
            row["assessment_id"],
            row["score"]
        ))

connection.commit()
# Progress Check
print("Scores imported successfully!")

with open("Attendance.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT INTO Attendance (
                attendance_id,
                student_id,
                date,
                status
            )
            VALUES (?, ?, ?, ?)
        """, (
            row["attendance_id"],
            row["student_id"],
            row["date "],
            row["status"]
        ))

# Progress Check
print("Attendance imported successfully!\n")
connection.commit()

#cursor.execute("SELECT COUNT(*) FROM Students")
#rows = cursor.fetchone()
#print("Number of students:", rows[0])


tables = ["Students", "Courses", "Assessments", "Scores", "Attendance"]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    result = cursor.fetchone()
    print(f"Number of records in {table}: {result[0]}")


print("\nAVERAGE SCORES PER COURSE")
# 1. What is the average score of each course?
cursor.execute("""
    SELECT
        Courses.course_name,
        AVG(Scores.score) AS avg_score
    FROM Scores
    JOIN Assessments
        ON Scores.assessment_id = Assessments.assessment_id
    JOIN Courses
        ON Assessments.course_id = Courses.course_id
    GROUP BY Courses.course_name
""")

results = cursor.fetchall()

for row in results:
    print(f"{row[0]}: {row[1]:.2f}")


print("\nLOWEST AVERAGE PERFORMANCE BY TOPIC")
# 2. Which topics have the lowest average performance?
cursor.execute("""
    SELECT
        Assessments.topic,
        AVG(Scores.score) AS avg_score
    FROM Scores
    JOIN Assessments
        ON Scores.assessment_id = Assessments.assessment_id
    GROUP BY Assessments.topic
    ORDER BY avg_score ASC
""")

results = cursor.fetchall()

for row in results:
    print(f"{row[0]}: {row[1]:.2f}")

print("\nSTUDENT WITH HIGHEST PERFORMANCE IMPROVEMENT")
# 3. Which student improved the most?

print("\nATTENDANCE AND PERFORMANCE RELATIONSHIP")
# 4. Is attendance related with performance?

print("\nASSESSMENTS WITH HIGHEST/LOWEST AVERAGE SCORES")
# 5. Which assessment have the highest/lowest average scores?


connection.close()

