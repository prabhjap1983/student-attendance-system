import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox,filedialog
import matplotlib.pyplot as plt #for manupulation and analysis
import pandas as pd #for visualization
from tkcalendar import DateEntry 
import datetime
import numpy as np
from tkinter import Label, PhotoImage
from tkinter import simpledialog


# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="", 
    database="attendance_system"
)
cursor = conn.cursor()

# Creating the Tkinter GUI
root = tk.Tk()
root.title("Student Attendance System")
root.geometry("1070x2000")

# Setting the background color 
root.configure(bg="Thistle")

# Setting a color scheme
background_color = "#f0f0f0"
button_color = "#800080"
button_text_color = "white"
font_style = ("Arial", 12)

# Function to style buttons
def style_button(widget):
    widget.configure(
        font=font_style,
        bg=button_color,
        fg=button_text_color,
        padx=10,
        pady=5,
    )

# Function to add a new student
def add_student():
    add_student_window = tk.Toplevel(root)
    add_student_window.title("Add Student")
    add_student_window.geometry("500x450")
    add_student_window.configure(bg="#ffffff")

    frame = tk.Frame(add_student_window, bg="thistle")
    frame.pack(pady=50)

    def show_dob_validation(event):
        if dob_entry.get() == "Date of Birth (yyyy/mm/dd)":
            dob_entry.delete(0, tk.END)
            dob_entry.config(fg='black', font=font_style)

    def show_email_validation(event):
        if email_entry.get() == "Email (user@example.com)":
            email_entry.delete(0, tk.END)
            email_entry.config(fg='black', font=font_style)

    def show_phone_validation(event):
        if phone_entry.get() == "Phone Number (+91XXXXXXXXXX)":
            phone_entry.delete(0, tk.END)
            phone_entry.config(fg='black', font=font_style)

    name_label = tk.Label(frame, text="Name:", font=font_style, bg="#efccff")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(frame, font=font_style)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    dob_label = tk.Label(frame, text="Date of Birth:", font=font_style, bg="#efccff")
    dob_label.grid(row=1, column=0, padx=10, pady=5)
    dob_entry = tk.Entry(frame, font=font_style, fg='grey')
    dob_entry.insert(0, "Date of Birth (yyyy/mm/dd)")
    dob_entry.bind("<FocusIn>", show_dob_validation)
    dob_entry.grid(row=1, column=1, padx=10, pady=5)

    email_label = tk.Label(frame, text="Email:", font=font_style, bg="#efccff")
    email_label.grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(frame, font=font_style, fg='grey')
    email_entry.insert(0, "Email (user@example.com)")
    email_entry.bind("<FocusIn>", show_email_validation)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    phone_label = tk.Label(frame, text="Phone Number:", font=font_style, bg="#efccff")
    phone_label.grid(row=3, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(frame, font=font_style, fg='grey')
    phone_entry.insert(0, "Phone Number (+91XXXXXXXXXX)")
    phone_entry.bind("<FocusIn>", show_phone_validation)
    phone_entry.grid(row=3, column=1, padx=10, pady=5)

    address_label = tk.Label(frame, text="Address:", font=font_style, bg="#efccff")
    address_label.grid(row=4, column=0, padx=10, pady=5)
    address_entry = tk.Entry(frame, font=font_style)
    address_entry.grid(row=4, column=1, padx=10, pady=5)

    def upload_photo(url_label):
        # Prompt the user to enter the student ID
        student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")

        if student_id is not None:
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
            if file_path:
                try:
                    with conn.cursor() as cursor:
                        # Inserting the file path into the database for the specific student
                        cursor.execute("UPDATE students SET photo_path = %s WHERE student_id = %s", (file_path, student_id))
                        conn.commit()

                    # Displaying the image URL as a clickable hyperlink
                    url_label.config(text="Image URL:", font=font_style, bg="#efccff")
                    link_label = tk.Label(url_label, text=file_path, font=font_style, fg="blue", cursor="hand2")
                    link_label.grid(row=7, column=1, padx=10, pady=10)
                    link_label.bind("<Button-1>", lambda event: open_url(file_path))

                    # To Display a success message
                    messagebox.showinfo("Success", "Photo uploaded successfully!")

                except mysql.connector.Error as err:
                    conn.rollback()
                    messagebox.showerror("Error", f"Error uploading photo: {str(err)}")

    def open_url(url):
        # Open the file path or URL in the default system application
        import webbrowser
        webbrowser.open(url)

    # Example usage
    url_label = tk.Label(frame, text="", font=font_style, bg="#efccff")
    url_label.grid(row=7, columnspan=2, pady=10)

    upload_photo_button = tk.Button(frame, text="Upload Photo", command=lambda: upload_photo(url_label))
    style_button(upload_photo_button)
    upload_photo_button.grid(row=6, columnspan=2, pady=10)



    def save_student():
        name = name_entry.get()
        date_of_birth = dob_entry.get()
        email = email_entry.get()
        phone_number = phone_entry.get()
        address = address_entry.get()

        if date_of_birth == "Date of Birth (yyyy/mm/dd)" or email == "Email (user@example.com)" or phone_number == "Phone Number (+91XXXXXXXXXX)":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        sql = """
            INSERT INTO students (name, date_of_birth, email, phone_number, address)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, date_of_birth, email, phone_number, address)

        try:
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Success", "Student registered successfully!")
            # To Clear the input fields
            name_entry.delete(0, tk.END)
            dob_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)
            
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Error", f"Error: {err}")

    save_button = tk.Button(frame, text="Save Student", command=save_student)
    style_button(save_button)
    save_button.grid(row=5, columnspan=2, pady=10)

def mark_attendance():
    mark_attendance_window = tk.Toplevel(root)
    mark_attendance_window.title("Mark Attendance")
    mark_attendance_window.geometry("650x350")
    mark_attendance_window.configure(bg="#ffffff")

    frame = tk.Frame(mark_attendance_window, bg="thistle")
    frame.pack(pady=50)

    def show_date_validation(event):
        if date_entry.get() == "Date (YYYY-MM-DD)":
            date_entry.delete(0, tk.END)
            date_entry.config(fg='black', font=font_style)

    student_label = tk.Label(frame, text="Select Student:", font=font_style, bg="#efccff")
    student_label.grid(row=0, column=0, padx=10, pady=5)

    # list of students from the database
    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()
    student_names = [student[1] for student in students]

    student_name_var = tk.StringVar()
    student_name_var.set("Select Student")
    student_dropdown = ttk.Combobox(frame, textvariable=student_name_var, values=student_names)
    student_dropdown.grid(row=0, column=1, padx=10, pady=5)

    selected_student_id = None  # Initializing the global variable

    def update_student_id(event):
        nonlocal selected_student_id
        # Get the student ID based on the selected student name
        selected_student_name = student_name_var.get()
        selected_student_index = student_names.index(selected_student_name)
        selected_student_id = students[selected_student_index][0]

    student_dropdown.bind("<<ComboboxSelected>>", update_student_id)

    date_label = tk.Label(frame, text="Date:", font=font_style, bg="#efccff")
    date_label.grid(row=1, column=0, padx=10, pady=5)
    date_entry = tk.Entry(frame, font=font_style, fg='grey')
    date_entry.insert(0, "Date (YYYY-MM-DD)")
    date_entry.bind("<FocusIn>", show_date_validation)
    date_entry.grid(row=1, column=1, padx=10, pady=5)

    def load_current_date():
        # For Fetching the current date 
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        date_entry.delete(0, tk.END)
        date_entry.insert(0, current_date)

    load_date_button = tk.Button(frame, text="Load Current Date", command=load_current_date)
    style_button(load_date_button)
    load_date_button.grid(row=1, column=2, padx=10)

    subject_label = tk.Label(frame, text="Select Subject:", font=font_style, bg="#efccff")
    subject_label.grid(row=2, column=0, padx=10, pady=5)

    # Create a list of subjects. 
    subjects = ["basics_of_management", "web_development_using_php", "mobile_technology", "computer_peripheral","microprocessor","Project"]  # Replace with your subject list

    subject_var = tk.StringVar()
    subject_var.set("Select Subject")
    subject_dropdown = ttk.Combobox(frame, textvariable=subject_var, values=subjects)
    subject_dropdown.grid(row=2, column=1, padx=10, pady=5)

    subject = None  # Initializing the subject variable

    def update_subject(event):
        nonlocal subject
        subject = subject_var.get()

    subject_dropdown.bind("<<ComboboxSelected>>", update_subject)

    present_label = tk.Label(frame, text="Present:", font=font_style, bg="#efccff")
    present_label.grid(row=3, column=0, padx=10, pady=5)
    present_checkbox_var = tk.StringVar(value="Y")
    present_checkbox = tk.Checkbutton(frame, text="Present", variable=present_checkbox_var, onvalue="Y", offvalue="N")
    present_checkbox.grid(row=3, column=1, padx=10, pady=5)
    present_checkbox.configure(bg='white')

    def mark_attendance_to_db():
        date = date_entry.get()
        present = present_checkbox_var.get()

        if date == "Date (YYYY-MM-DD)":
            messagebox.showerror("Error", "Please enter a valid date (YYYY-MM-DD).")
            return

        if selected_student_id is not None and subject:
            try:
                cursor.execute("INSERT INTO attendance (student_id, date, present, subject) VALUES (%s, %s, %s, %s)",
                               (selected_student_id, date, present, subject))
                conn.commit()
                messagebox.showinfo("Success", "Attendance marked successfully.")
                mark_attendance_window.destroy()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a student and a subject.")

    mark_button = tk.Button(frame, text="Mark Attendance", command=mark_attendance_to_db)
    mark_button.grid(row=4, columnspan=2, pady=20)
    style_button(mark_button) 


# creating view_attendance window
def view_attendance():
    view_attendance_window = tk.Toplevel(root)
    view_attendance_window.title("View Attendance")
    view_attendance_window.geometry("550x250")
    view_attendance_window.configure(bg="#ffffff")

    frame = tk.Frame(view_attendance_window, bg="thistle")
    frame.pack(pady=50)

    student_id_label = tk.Label(frame, text="Student ID or Name:", font=font_style, bg="#efccff")
    student_id_label.grid(row=0, column=0, padx=10, pady=5)
    student_id_entry = tk.Entry(frame, font=font_style)
    student_id_entry.grid(row=0, column=1, padx=10, pady=5)

    option_var = tk.StringVar()
    option_var.set("ID")  

    id_option = tk.Radiobutton(frame, text="ID", variable=option_var, value="ID",bg="#ffffff")
    id_option.grid(row=1, column=0, padx=10, pady=5)

    name_option = tk.Radiobutton(frame, text="Name", variable=option_var, value="Name",bg="#ffffff")
    name_option.grid(row=1, column=1, padx=10, pady=5)

    def view():
        selection_option = option_var.get()
        value = student_id_entry.get()

        if selection_option == "ID":
            try:
                student_id = int(value)
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID")
                return
            # Query the database by ID
            sql = "SELECT date, subject, present FROM attendance WHERE student_id = %s"
            values = (student_id,)
            cursor.execute(sql, values)
            attendance_records = cursor.fetchall()
        elif selection_option == "Name":
            # Query the database by Name
            sql = "SELECT date, subject, present FROM attendance INNER JOIN students ON attendance.student_id = students.student_id WHERE students.name LIKE %s"
            values = ("%" + value + "%",)
            cursor.execute(sql, values)
            attendance_records = cursor.fetchall()
        else:
            messagebox.showerror("Error", "Invalid selection")
            return

        if attendance_records:
            # Display the attendance records, date, subjects, and present status
            attendance_result_window = tk.Toplevel(root)
            attendance_result_window.title(f"Attendance for {selection_option}: {value}")
            attendance_result_window.geometry("800x400")
            attendance_result_window.configure(bg="thistle")

            tree = ttk.Treeview(attendance_result_window, columns=("Date", "Subject", "Present"))
            tree.heading("#1", text="Date")
            tree.heading("#2", text="Subject")
            tree.heading("#3", text="Present")
            tree.pack()

            for record in attendance_records:
                tree.insert("", "end", values=(record[0], record[1], record[2]))
        else:
            messagebox.showinfo("Info", f"No attendance records found for this {selection_option}.")


    view_button = tk.Button(frame, text="View Attendance", command=view)
    style_button(view_button)
    view_button.grid(row=2, columnspan=2, pady=10)

# Function to generate an attendance report
def generate_report():
    generate_report_window = tk.Toplevel(root)
    generate_report_window.title("Generate Report")
    generate_report_window.geometry("600x300")
    generate_report_window.configure(bg="#ffffff")

    frame = tk.Frame(generate_report_window, bg="thistle")
    frame.pack(pady=50)

    from_date_label = tk.Label(frame, text="From Date:", font=font_style, bg="#efccff")
    from_date_label.grid(row=0, column=0, padx=10, pady=5)
    from_date_cal = DateEntry(frame, font=font_style)  
    from_date_cal.grid(row=0, column=1, padx=10, pady=5)

    to_date_label = tk.Label(frame, text="To Date:", font=font_style, bg="#efccff")
    to_date_label.grid(row=1, column=0, padx=10, pady=5)
    to_date_cal = DateEntry(frame, font=font_style)  
    to_date_cal.grid(row=1, column=1, padx=10, pady=5)

    def generate():
        from_date = from_date_cal.get_date()  # Get selected  from DateEntry
        to_date = to_date_cal.get_date()  # Get selected date from DateEntry

        sql = """
        SELECT students.student_id, students.name, COUNT(attendance.attendance_id) as attendance_count
        FROM students
        LEFT JOIN attendance ON students.student_id = attendance.student_id
        WHERE attendance.date BETWEEN %s AND %s
        GROUP BY students.student_id, students.name
    """

        cursor.execute(sql, (from_date, to_date))
        attendance_report = cursor.fetchall()

        report_result_window = tk.Toplevel(root)
        report_result_window.title("Attendance Report")
        report_result_window.geometry("800x400")
        report_result_window.configure(bg="thistle")

        tree = ttk.Treeview(report_result_window, columns=("Student ID", "Name", "Attendance Count"))
        tree.heading("#1", text="Student ID")
        tree.heading("#2", text="Name")
        tree.heading("#3", text="Attendance Count")
        tree.pack()

        for record in attendance_report:
            tree.insert("", "end", values=(record[0], record[1], record[2]))

    generate_button = tk.Button(frame, text="Generate", command=generate)
    style_button(generate_button)
    generate_button.grid(row=2, columnspan=2, pady=10)


# Function to delete a student by name or ID
def delete_student():
    delete_student_window = tk.Toplevel(root)
    delete_student_window.title("Delete Student")
    delete_student_window.geometry("600x250")
    delete_student_window.configure(bg="#ffffff")

    frame = tk.Frame(delete_student_window, bg="thistle")
    frame.pack(pady=50)

    delete_label = tk.Label(frame, text="Delete by Student Name or ID:", font=font_style, bg="#efccff")
    delete_label.grid(row=0, column=0, padx=10, pady=5)
    delete_entry = tk.Entry(frame, font=font_style)
    delete_entry.grid(row=0, column=1, padx=10, pady=5)

    option_var = tk.StringVar()
    option_var.set("Name")  
    name_option = tk.Radiobutton(frame, text="Name", variable=option_var, value="Name",bg="#ffffff")
    name_option.grid(row=1, column=0, padx=10, pady=5)

    id_option = tk.Radiobutton(frame, text="ID", variable=option_var, value="ID",bg="#ffffff")
    id_option.grid(row=1, column=1, padx=10, pady=5)

    def delete():
        selection_option = option_var.get()
        value = delete_entry.get()

        if selection_option == "Name":
            # Delete from the database by Name
            sql = "DELETE FROM students WHERE name LIKE %s"
            values = ("%" + value + "%",)
            cursor.execute(sql, values)
        elif selection_option == "ID":
            try:
                student_id = int(value)
                # Delete from the database by ID
                sql = "DELETE FROM students WHERE student_id = %s"
                values = (student_id,)
                cursor.execute(sql, values)
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID")
                return
        else:
            messagebox.showerror("Error", "Invalid selection")
            return

        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
        else:
            conn.rollback()
            messagebox.showinfo("Info", "No students found matching the delete criteria.")

    delete_button = tk.Button(frame, text="Delete", command=delete)
    style_button(delete_button)
    delete_button.grid(row=2, columnspan=2, pady=10)

# Function to search for students by name or ID
def search_students():
    search_students_window = tk.Toplevel(root)
    search_students_window.title("Search Students")
    search_students_window.geometry("600x250")
    search_students_window.configure(bg="#ffffff")

    frame = tk.Frame(search_students_window, bg="thistle")
    frame.pack(pady=50)

    search_label = tk.Label(frame, text="Search by Student Name or ID:", font=font_style, bg="#efccff")
    search_label.grid(row=0, column=0, padx=10, pady=5)
    search_entry = tk.Entry(frame, font=font_style)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    option_var = tk.StringVar()
    option_var.set("Name")  # Default option

    name_option = tk.Radiobutton(frame, text="Name", variable=option_var, value="Name",bg="#ffffff")
    name_option.grid(row=1, column=0, padx=10, pady=5)

    id_option = tk.Radiobutton(frame, text="ID", variable=option_var, value="ID",bg="#ffffff")
    id_option.grid(row=1, column=1, padx=10, pady=5)

    def search():
        selection_option = option_var.get()
        value = search_entry.get()

        if selection_option == "Name":
            # Query the database by Name
            sql = "SELECT * FROM students WHERE name LIKE %s"
            values = ("%" + value + "%",)
            cursor.execute(sql, values)
            search_results = cursor.fetchall()
        elif selection_option == "ID":
            try:
                student_id = int(value)
                # Query the database by ID
                sql = "SELECT * FROM students WHERE student_id = %s"
                values = (student_id,)
                cursor.execute(sql, values)
                search_results = cursor.fetchall()
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID")
                return
        else:
            messagebox.showerror("Error", "Invalid selection")
            return

        if search_results:
            search_result_window = tk.Toplevel(root)
            search_result_window.title("Search Results")
            search_result_window.geometry("800x400")
            search_result_window.configure(bg="thistle")

            tree = ttk.Treeview(search_result_window, columns=("Student ID", "Name", "Date of Birth", "Email", "Phone Number", "Address"))
            tree.heading("#1", text="Student ID")
            tree.heading("#2", text="Name")
            tree.heading("#3", text="Date of Birth")
            tree.heading("#4", text="Email")
            tree.heading("#5", text="Phone Number")
            tree.heading("#6", text="Address")
            tree.pack()

            for record in search_results:
                tree.insert("", "end", values=record)
        else:
            messagebox.showinfo("Info", f"No students found matching the search criteria.")

    search_button = tk.Button(frame, text="Search", command=search)
    style_button(search_button)
    search_button.grid(row=2, columnspan=2, pady=10)


# Function to update student information
def update_student():
    update_student_window = tk.Toplevel(root)
    update_student_window.title("Update Student Information")
    update_student_window.geometry("500x450")
    update_student_window.configure(bg="#ffffff")

    frame = tk.Frame(update_student_window, bg="thistle")
    frame.pack(pady=20)

    student_id_label = tk.Label(frame, text="Student ID:", font=font_style, bg="#efccff")
    student_id_label.grid(row=0, column=0, padx=10, pady=5)
    student_id_entry = tk.Entry(frame, font=font_style)
    student_id_entry.grid(row=0, column=1, padx=10, pady=5)

    name_label = tk.Label(frame, text="Name:", font=font_style, bg="#efccff")
    name_label.grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(frame, font=font_style)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    dob_label = tk.Label(frame, text="Date of Birth:", font=font_style, bg="#efccff")
    dob_label.grid(row=2, column=0, padx=10, pady=5)
    dob_entry = tk.Entry(frame, font=font_style)
    dob_entry.grid(row=2, column=1, padx=10, pady=5)

    email_label = tk.Label(frame, text="Email:", font=font_style, bg="#efccff")
    email_label.grid(row=3, column=0, padx=10, pady=5)
    email_entry = tk.Entry(frame, font=font_style)
    email_entry.grid(row=3, column=1, padx=10, pady=5)

    phone_label = tk.Label(frame, text="Phone Number:", font=font_style, bg="#efccff")
    phone_label.grid(row=4, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(frame, font=font_style)
    phone_entry.grid(row=4, column=1, padx=10, pady=5)

    address_label = tk.Label(frame, text="Address:", font=font_style, bg="#efccff")
    address_label.grid(row=5, column=0, padx=10, pady=5)
    address_entry = tk.Entry(frame, font=font_style)
    address_entry.grid(row=5, column=1, padx=10, pady=5)

    def load_student_data():
        student_id = int(student_id_entry.get())

        sql = "SELECT * FROM students WHERE student_id = %s"
        values = (student_id,)
        cursor.execute(sql, values)
        student_data = cursor.fetchone()

        if student_data:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, student_data[1])
            dob_entry.delete(0, tk.END)
            dob_entry.insert(0, student_data[2])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, student_data[3])
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, student_data[4])
            address_entry.delete(0, tk.END)
            address_entry.insert(0, student_data[5])
        else:
            messagebox.showinfo("Info", "No student found with this ID.")

    def update():
        student_id = int(student_id_entry.get())
        name = name_entry.get()
        date_of_birth = dob_entry.get()
        email = email_entry.get()
        phone_number = phone_entry.get()
        address = address_entry.get()

        sql = """
            UPDATE students
            SET name = %s, date_of_birth = %s, email = %s, phone_number = %s, address = %s
            WHERE student_id = %s
        """
        values = (name, date_of_birth, email, phone_number, address, student_id)

        try:
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Success", "Student information updated successfully!")
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Error", f"Error: {err}")

    load_button = tk.Button(frame, text="Load Student Data", command=load_student_data)
    style_button(load_button)
    load_button.grid(row=6, columnspan=2, pady=10)

    update_button = tk.Button(frame, text="Update Student", command=update)
    style_button(update_button)
    update_button.grid(row=7, columnspan=2, pady=10)

# Function to calculate and display attendance summary
def attendance_summary():
    # Fetching the total number of students from the database
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Fetching the total number of attendance days from the database
    cursor.execute("SELECT COUNT(DISTINCT date) FROM attendance")
    total_attendance_days = cursor.fetchone()[0]

    # Calculate the average attendance percentage
    if total_students > 0:
        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_attendance = cursor.fetchone()[0]
        average_attendance = (total_attendance / (total_students * total_attendance_days)) * 100
        average_attendance = round(average_attendance, 2)
    else:
        average_attendance = 0.0

    # Creating a messagebox to display the summary
    summary_text = f"""
    Attendance Summary:

    Total Students: {total_students}
    Total Attendance Days: {total_attendance_days}
    Average Attendance: {average_attendance}%
    """
    messagebox.showinfo("Attendance Summary", summary_text)
def analyze_attendance():
    # Fetch attendance data from the database grouped by subject
    cursor.execute("SELECT subject, COUNT(*) as count FROM attendance WHERE present='Y' GROUP BY subject")
    data = cursor.fetchall()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=["Subject", "Count"])

    # Calculate the total number of students
    cursor.execute("SELECT COUNT(DISTINCT student_id) FROM attendance")
    total_students = cursor.fetchone()[0]

    # Calculate attendance percentages
    df["Percentage"] = (df["Count"] / total_students) * 100

    # Sort the DataFrame by attendance percentage in descending order
    df = df.sort_values(by="Percentage", ascending=False)

    # Create labels and sizes for the pie chart
    labels = df["Subject"]
    sizes = df["Percentage"]

    # Define a color palette for the pie chart
    colors = plt.cm.Paired(range(len(labels)))

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, shadow=True)
    plt.axis('equal')  

    plt.title("Student Attendance Percentage by Subject")
    plt.legend(labels, loc="best")  

    # Display the pie chart
    plt.show()

def generate_bar_chart():
    # Fetching attendance data from the database
    cursor.execute("SELECT date, COUNT(*) as attendance_count FROM attendance GROUP BY date")
    data = cursor.fetchall()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=["Date", "Attendance Count"])

    # Extract dates and attendance counts
    dates = df["Date"]
    attendance_counts = df["Attendance Count"]

    # Create a figure and axis with subplots
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars with a color gradient
    cmap = plt.get_cmap("viridis")
    colors = cmap(np.arange(len(dates)) / len(dates))
    bars = ax.bar(dates, attendance_counts, color=colors)

    # Add labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Attendance Count")
    ax.set_title("Daily Attendance")

    # Rotate x-axis labels 
    plt.xticks(rotation=45, ha="right")

    # Add data labels above each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)

    # Add grid lines
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the bar chart
    plt.tight_layout()
    plt.show()

def generate_line_chart():
    # Fetch attendance data from the database
    cursor.execute("SELECT date, COUNT(*) as attendance_count FROM attendance GROUP BY date")
    data = cursor.fetchall()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=["Date", "Attendance Count"])

    # Extract dates and attendance counts
    dates = df["Date"]
    attendance_counts = df["Attendance Count"]

    # Create a figure and axis with subplots
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a more visually appealing line chart
    ax.plot(dates, attendance_counts, marker='o', linestyle='-', color='RebeccaPurple', label='Attendance Count')
    ax.set_xlabel("Date")
    ax.set_ylabel("Attendance Count")
    ax.set_title("Attendance Trends")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add a legend for clarity
    ax.legend(loc="best")

    # Adding data labels to each point on the line
    for date, count in zip(dates, attendance_counts):
        ax.annotate(str(count), xy=(date, count), xytext=(5, -10), textcoords='offset points', fontsize=8, ha='center')

    # To Customize the appearance of the chart
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the line chart
    plt.tight_layout()
    plt.show()

# Create and layout widgets
title_label = tk.Label(root, text="Student Attendance System", font=("Helvetica", 24), bg="#efccff", fg="black")  # Update header color
title_label.pack(pady=20)

image1 = tk.PhotoImage(file="STICKMAN.png")
image1 = image1.subsample(2, 2)
image_label1 = tk.Label(root, image=image1)
image_label1.pack(pady=5)

# Create a frame for the buttons to make them grid-like
button_frame = tk.Frame(root, bg="#ffffff")
button_frame.pack(pady=10)

# Define button functions and labels
button_functions = [add_student, mark_attendance, view_attendance, generate_report,
                    delete_student, search_students, update_student,attendance_summary]

button_labels = ["Add Student", "Mark Attendance", "View Attendance", "Generate Report",
                 "Delete Student", "Search Students", "Update Student Info","attendance_summary"]

# Create and pack buttons in a grid layout
for i, (func, label) in enumerate(zip(button_functions, button_labels)):
    button = tk.Button(button_frame, text=label, command=func)
    style_button(button)
    button.grid(row=i // 2, column=i % 2, padx=20, pady=10, sticky="nsew")

# Update the grid geometry to adjust button sizes and spacing
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(1, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# Function to add buttons for data analysis charts
def add_data_analysis_buttons():
    analyze_button = tk.Button(root, text="Analyze Attendance (Pie Chart)", command=analyze_attendance)
    style_button(analyze_button)
    analyze_button.configure(bg="#ad34cb", fg="white")  
    analyze_button.pack(fill=tk.X, padx=50, pady=10)
    analyze_button.config(width=30)  

    bar_chart_button = tk.Button(root, text="Generate Bar Chart", command=generate_bar_chart)
    style_button(bar_chart_button)
    bar_chart_button.configure(bg="#ad34cb", fg="white")  
    bar_chart_button.pack(fill=tk.X, padx=50, pady=10)
    bar_chart_button.config(width=30)  

    line_chart_button = tk.Button(root, text="Generate Line Chart", command=generate_line_chart)
    style_button(line_chart_button)
    line_chart_button.configure(bg="#ad34cb", fg="white")  
    line_chart_button.pack(fill=tk.X, padx=50, pady=10)
    line_chart_button.config(width=30)  

add_data_analysis_buttons()  

# Function to display a user manual
def user_manual():
    
    user_manual_text = """
    Student Attendance System User Manual:

    1. Add Student: Click the 'Add Student' button to add a new student to the system.
    2. Mark Attendance: Click the 'Mark Attendance' button to mark attendance for a student.
    3. View Attendance: Click the 'View Attendance' button to view a student's attendance.
    4. Generate Report: Click the 'Generate Report' button to generate an attendance report.
    5. Delete Student: Click the 'Delete Student' button to delete a student from the system.
    6. Search Students: Click the 'Search Students' button to search for students by name.
    7. Update Student Info: Click the 'Update Student Info' button to update student information.
    8. Analyze Attendance: Click the 'Analyze Attendance (Pie Chart)' button to analyze attendance using a pie chart.
    9. Generate Bar Chart: Click the 'Generate Bar Chart' button to generate a bar chart of attendance.
    10. Generate Line Chart: Click the 'Generate Line Chart' button to generate a line chart of attendance trends.
    11. Exit: Click the 'Exit' button to close the application.

    For more information and assistance, contact the administrator.
    """

    messagebox.showinfo("User Manual", user_manual_text)

# Create and style the User Manual button
user_manual_button = tk.Button(root, text="User Manual", command=user_manual)
user_manual_button.configure(bg="#5A4FCF", fg="white", font=("Arial", 12))
user_manual_button.pack(fill=tk.X, padx=50, pady=10)
user_manual_button.config(width=30)

exit_button = tk.Button(root, text="Exit", command=root.quit)
style_button(exit_button)
exit_button.configure(bg="#ad34cb", fg="white")  
exit_button.pack(fill=tk.X, padx=50, pady=10)  
exit_button.config(width=10, height=1)

# Run the Tkinter main loop
root.mainloop()

# Close the database connection when the application exits
conn.close()