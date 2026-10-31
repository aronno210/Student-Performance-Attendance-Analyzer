import tkinter as tk
from tkinter import ttk, messagebox
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

FILE_NAME = "students.csv"
SUBJECTS = ["Python", "DBMS", "AI", "JavaScript"]
ATTENDANCE_LIMIT = 75


# ------------------------------------------------------------
# STUDENT CLASS
# ------------------------------------------------------------

class Student:
    def __init__(self, roll, name, marks, attendance):

        self.roll = roll
        self.name = name
        self.marks = marks
        self.attendance = attendance

        self.total = sum(marks.values())
        self.average = np.mean(list(marks.values()))
        self.percentage = self.average
        self.grade = self.calculate_grade()

    def calculate_grade(self):

        if self.percentage >= 80:
            return "A"

        elif self.percentage >= 70:
            return "B"

        elif self.percentage >= 60:
            return "C"

        elif self.percentage >= 50:
            return "D"

        else:
            return "F"


# ------------------------------------------------------------
# GLOBAL STUDENT LIST
# ------------------------------------------------------------

students = []
import os
if os.path.exists(FILE_NAME):
    try:
        df = pd.read_csv(FILE_NAME)
        for _, row in df.iterrows():
            m = {"Python": row["Python"], "DBMS": row["DBMS"], "AI": row["AI"], "JavaScript": row["JavaScript"]}
            students.append(Student(int(row["Roll"]), str(row["Name"]), m, float(row["Attendance"])))
    except:
        pass


# ------------------------------------------------------------
# ADD STUDENT
# ------------------------------------------------------------

def add_student():
    try:
        roll = int(roll_entry.get())

        if roll <= 0:
            raise ValueError

        name = name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error","Please enter student name.")
            return

        marks = {}

        for subject, entry in zip(SUBJECTS,mark_entries):
            mark = float(entry.get())

            if mark < 0 or mark > 100:
                raise ValueError

            marks[subject] = mark


        attendance = float(attendance_entry.get())

        if attendance < 0 or attendance > 100:
            raise ValueError


        # Create Student object

        student = Student(roll,name,marks,attendance)
        students.append(student)


        # Show result

        result_text.delete("1.0",tk.END)
        result_text.insert(tk.END,"Student Added Successfully!\n\n")
        result_text.insert(tk.END,f"Roll: {student.roll}\n")
        result_text.insert(tk.END,f"Name: {student.name}\n")
        result_text.insert(tk.END,f"Total: {student.total}\n")
        result_text.insert(tk.END,f"Average: {student.average:.2f}\n")
        result_text.insert(tk.END,f"Percentage: {student.percentage:.2f}%\n")
        result_text.insert(tk.END,f"Grade: {student.grade}\n")
        result_text.insert(tk.END,f"Attendance: {student.attendance}%\n")


        if student.attendance < ATTENDANCE_LIMIT:
            result_text.insert(tk.END,"\nWarning: Low Attendance!")

        clear_entries()


    except ValueError:
        messagebox.showerror("Invalid Input","Please enter valid numbers.\n"
                             "Marks and attendance must be between 0 and 100."
        )


# ------------------------------------------------------------
# CLEAR INPUT FIELDS
# ------------------------------------------------------------

def clear_entries():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    for entry in mark_entries:
        entry.delete(0, tk.END)

    attendance_entry.delete(0, tk.END)


# ------------------------------------------------------------
# VIEW STUDENT RECORDS
# ------------------------------------------------------------

def view_records():
    result_text.delete("1.0",tk.END)

    if len(students) == 0:
        result_text.insert(tk.END,"No student records available.")
        return


    for student in students:

        result_text.insert(
            tk.END,
            f"Roll: {student.roll} | "
            f"Name: {student.name} | "
            f"Percentage: {student.percentage:.2f}% | "
            f"Grade: {student.grade} | "
            f"Attendance: {student.attendance}%\n"
        )


# ------------------------------------------------------------
# PERFORMANCE ANALYSIS
# ------------------------------------------------------------

def analyze_performance():
    result_text.delete("1.0",tk.END)

    if len(students) == 0:
        result_text.insert(tk.END,"No student records available.")

        return


    # Sorting students according to percentage

    sorted_students = sorted(
        students,
        key=lambda student: student.percentage,
        reverse=True
    )


    result_text.insert(
        tk.END,
        "========== PERFORMANCE RANKING ==========\n\n"
    )


    for rank, student in enumerate(sorted_students,start=1):

        result_text.insert(tk.END,f"{rank}. {student.name} - "
                           f"{student.percentage:.2f}% - "
                           f"Grade {student.grade}\n"
        )


    # NumPy analysis

    percentages = np.array(
        [
            student.percentage
            for student in students
        ]
    )


    result_text.insert(tk.END,"\n========== ANALYSIS ==========\n")
    result_text.insert(tk.END,f"Average: {np.mean(percentages):.2f}%\n")
    result_text.insert(tk.END,f"Highest: {np.max(percentages):.2f}%\n")
    result_text.insert(tk.END,f"Lowest: {np.min(percentages):.2f}%\n")


# ------------------------------------------------------------
# LOW ATTENDANCE
# ------------------------------------------------------------

def check_attendance():
    result_text.delete("1.0",tk.END)

    if len(students) == 0:
        result_text.insert(tk.END,"No student records available.")

        return

    result_text.insert(tk.END,"========== LOW ATTENDANCE ==========\n\n")


    found = False


    for student in students:

        if student.attendance < ATTENDANCE_LIMIT:
            result_text.insert(tk.END,f"{student.name} - "f"{student.attendance}%\n")
            found = True


    if not found:
        result_text.insert(tk.END,"No student has attendance below "f"{ATTENDANCE_LIMIT}%.")


# ------------------------------------------------------------
# SAVE DATA TO CSV
# ------------------------------------------------------------

def save_data():
    if len(students) == 0:
        messagebox.showwarning("Warning","No student data to save.")

        return


    with open(FILE_NAME,"w",newline="")as file:
        writer = csv.writer(file)


        writer.writerow([
            "Roll",
            "Name",
            "Python",
            "DBMS",
            "AI",
            "JavaScript",
            "Total",
            "Average",
            "Percentage",
            "Grade",
            "Attendance"
        ])


        for student in students:
            writer.writerow([
                student.roll,
                student.name,
                student.marks["Python"],
                student.marks["DBMS"],
                student.marks["AI"],
                student.marks["JavaScript"],
                student.total,
                round(student.average, 2),
                round(student.percentage, 2),
                student.grade,
                student.attendance
            ])


    messagebox.showinfo(
        "Success",
        "Student data saved successfully."
    )


# ------------------------------------------------------------
# READ DATA USING PANDAS
# ------------------------------------------------------------

def read_data():

    global students

    try:
        data = pd.read_csv(FILE_NAME)

        # Clear current list and populate from CSV
        students.clear()

        for index, row in data.iterrows():
            marks = {
                "Python": row["Python"],
                "DBMS": row["DBMS"],
                "AI": row["AI"],
                "JavaScript": row["JavaScript"]
            }
            student = Student(int(row["Roll"]), str(row["Name"]), marks, float(row["Attendance"]))
            students.append(student)

        result_text.delete("1.0",tk.END)
        result_text.insert(tk.END,"========== CSV DATA ==========\n\n")
        result_text.insert(tk.END,data.to_string(index=False))
        result_text.insert(tk.END,f"\n\nTotal Students: {len(data)}")

        result_text.insert(tk.END,f"\nAverage Percentage: "f"{data['Percentage'].mean():.2f}%")


    except FileNotFoundError:
        messagebox.showerror("Error","students.csv not found.\n""Please save data first.")


# ------------------------------------------------------------
# GENERATE GRAPHS
# ------------------------------------------------------------

def generate_graphs():
    if len(students) == 0:
        messagebox.showwarning("Warning","No student data available.")

        return


    names = [
        student.name
        for student in students
    ]

    percentages = [
        student.percentage
        for student in students
    ]


    # ---------------- BAR CHART ----------------

    plt.figure(figsize=(8, 5))
    plt.bar(names,percentages)
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.title("Student Performance - Bar Chart")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("bar_chart.png")

    plt.show()


    # ---------------- LINE GRAPH ----------------

    plt.figure(figsize=(8, 5))
    plt.plot(names,percentages,marker="o")
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.title("Student Performance - Line Graph")
    plt.xticks(rotation=30)
    plt.grid()
    plt.tight_layout()
    plt.savefig("line_graph.png")

    plt.show()


    # ---------------- HISTOGRAM ----------------

    from matplotlib.ticker import MaxNLocator

    plt.figure(figsize=(8, 5))
    bins = [0, 20, 40, 60, 80, 100]
    plt.hist(percentages, bins=bins, edgecolor="black", color="#4CAF50", rwidth=0.85)
    plt.xlabel("Percentage Range (%)")
    plt.ylabel("Number of Students")
    plt.title("Student Percentage Distribution (Histogram)")
    plt.xticks(bins)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("histogram.png")

    plt.show()

    messagebox.showinfo("Success","All three graphs generated successfully.")


# ============================================================
# GUI WINDOW
# ============================================================

root = tk.Tk()
root.title("Student Performance & Attendance Analyzer")
root.geometry("850x650")


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

title_label = tk.Label(root,text="Student Performance & Attendance Analyzer",font=("Arial", 20, "bold"))
title_label.pack(pady=15)


# ------------------------------------------------------------
# INPUT FRAME
# ------------------------------------------------------------

input_frame = tk.Frame(root)
input_frame.pack(pady=5)


# Roll

tk.Label(input_frame,text="Roll Number:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

roll_entry = tk.Entry(input_frame,width=20)
roll_entry.grid(row=0,column=1)


# Name

tk.Label(input_frame,text="Student Name:"
).grid(row=1,column=0,padx=5,pady=5)

name_entry = tk.Entry(input_frame,width=20)
name_entry.grid(row=1,column=1)


# Marks

mark_entries = []

for i, subject in enumerate(SUBJECTS,start=2):

    tk.Label(input_frame,text=f"{subject} Marks:"
    ).grid(row=i,column=0,padx=5,pady=5)

    entry = tk.Entry(input_frame,width=20)
    entry.grid(row=i,column=1)

    mark_entries.append(entry)


# Attendance

tk.Label(input_frame,text="Attendance %:"
).grid(row=6,column=0,padx=5,pady=5)

attendance_entry = tk.Entry(input_frame,width=20)
attendance_entry.grid(row=6,column=1)


# ------------------------------------------------------------
# BUTTON FRAME
# ------------------------------------------------------------

button_frame = tk.Frame(root)
button_frame.pack(pady=15)


tk.Button(button_frame,text="Add Student",width=16,command=add_student
).grid(row=0,column=0,padx=5,pady=5)

tk.Button(button_frame,text="View Records",width=16,command=view_records
).grid(row=0,column=1,padx=5,pady=5)

tk.Button(button_frame,text="Performance",width=16,command=analyze_performance
).grid(row=0,column=2,padx=5,pady=5)

tk.Button(button_frame,text="Attendance",width=16,command=check_attendance
).grid(row=1,column=0,padx=5,pady=5)

tk.Button(button_frame,text="Save CSV",width=16,command=save_data
).grid(row=1,column=1,padx=5,pady=5)

tk.Button(button_frame,text="Read CSV",width=16,command=read_data
).grid(row=1,column=2,padx=5,pady=5)

tk.Button(button_frame,text="Generate Graphs",width=16,command=generate_graphs
).grid(row=2,column=1,padx=5,pady=5)


# ------------------------------------------------------------
# RESULT AREA
# ------------------------------------------------------------

result_text = tk.Text(root,width=95,height=14)
result_text.pack(padx=15,pady=10)


# ------------------------------------------------------------
# START GUI
# ------------------------------------------------------------

root.mainloop()