import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import os

# =========================================================
# GLOBAL VARIABLES
# =========================================================

photo_path = ""

name_entry = None
course_entry = None
phone_entry = None
id_entry = None
search_entry = None
result_label = None
photo_label = None


# =========================================================
# DATABASE
# =========================================================

def connect_db():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    # STUDENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            phone TEXT,
            photo TEXT
        )
    """)

    # TEACHERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL
        )
    """)

    # BOOKS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    # USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # DEFAULT ADMIN
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (id, username, password, role)
        VALUES
        (1, 'admin', 'admin123', 'admin')
    """)

    # ATTENDANCE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# LOGIN
# =========================================================

def check_login():

    user = username.get().strip()
    pwd = password.get().strip()

    if user == "" or pwd == "":
        status.config(
            text="Please enter username and password",
            fg="red"
        )
        return

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT role
        FROM users
        WHERE username = ? AND password = ?
    """, (user, pwd))

    result = cur.fetchone()

    conn.close()

    if result:

        role = result[0]

        root.destroy()

        if role == "admin":
            dashboard()

        elif role == "teacher":
            teacher_panel()

        elif role == "student":
            student_panel()

        else:
            messagebox.showerror(
                "Error",
                "Invalid user role."
            )

    else:

        status.config(
            text="Invalid Username or Password",
            fg="red"
        )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def dashboard():

    win = tk.Tk()
    win.title("Admin Dashboard")
    win.geometry("450x550")
    win.resizable(False, False)

    tk.Label(
        win,
        text="COLLEGE MANAGEMENT SYSTEM",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        win,
        text="Admin Control Panel",
        font=("Arial", 14)
    ).pack(pady=5)

    tk.Button(
        win,
        text="Student Management",
        width=30,
        command=student_window
    ).pack(pady=7)

    tk.Button(
        win,
        text="Teacher Management",
        width=30,
        command=teacher_window
    ).pack(pady=7)

    tk.Button(
        win,
        text="Library",
        width=30,
        command=library_window
    ).pack(pady=7)

    tk.Button(
        win,
        text="View Students",
        width=30,
        command=show_students
    ).pack(pady=7)

    tk.Button(
        win,
        text="Register User",
        width=30,
        command=register_window
    ).pack(pady=7)

    tk.Button(
        win,
        text="Attendance Graph",
        width=30,
        command=show_graph
    ).pack(pady=7)

    tk.Button(
        win,
        text="Logout",
        width=30,
        command=lambda: logout(win)
    ).pack(pady=15)

    win.mainloop()


# =========================================================
# LOGOUT
# =========================================================

def logout(window):

    window.destroy()
    login_window()


# =========================================================
# LOGIN WINDOW
# =========================================================

def login_window():

    global root
    global username
    global password
    global status

    root = tk.Tk()

    root.title("College Management Login")
    root.geometry("400x330")
    root.resizable(False, False)

    title = tk.Label(
        root,
        text="COLLEGE MANAGEMENT SYSTEM",
        font=("Arial", 16, "bold")
    )

    title.pack(pady=20)

    tk.Label(
        root,
        text="Username",
        font=("Arial", 11)
    ).pack()

    username = tk.Entry(
        root,
        width=30,
        font=("Arial", 11)
    )

    username.pack(pady=5)

    tk.Label(
        root,
        text="Password",
        font=("Arial", 11)
    ).pack()

    password = tk.Entry(
        root,
        show="*",
        width=30,
        font=("Arial", 11)
    )

    password.pack(pady=5)

    tk.Button(
        root,
        text="Login",
        width=20,
        command=check_login
    ).pack(pady=15)

    status = tk.Label(
        root,
        text="",
        font=("Arial", 10)
    )

    status.pack()

    tk.Label(
        root,
        text="Default Admin Login\nUsername: admin\nPassword: admin123",
        font=("Arial", 9)
    ).pack(pady=15)

    root.bind(
        "<Return>",
        lambda event: check_login()
    )

    root.mainloop()


# =========================================================
# PHOTO UPLOAD
# =========================================================

def upload_photo():

    global photo_path

    selected_file = filedialog.askopenfilename(
        title="Select Student Photo",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.gif"),
            ("All Files", "*.*")
        ]
    )

    if not selected_file:
        return

    try:

        img = Image.open(selected_file)
        img = img.resize((120, 120))

        img = ImageTk.PhotoImage(img)

        photo_label.config(image=img)
        photo_label.image = img

        photo_path = selected_file

    except Exception as e:

        messagebox.showerror(
            "Photo Error",
            f"Unable to load photo.\n\n{e}"
        )


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    name = name_entry.get().strip()
    course = course_entry.get().strip()
    phone = phone_entry.get().strip()

    if name == "" or course == "":

        messagebox.showwarning(
            "Warning",
            "Please enter student name and course."
        )

        return

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students
        (name, course, phone, photo)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        course,
        phone,
        photo_path
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Student Added Successfully!"
    )

    clear_student_fields()


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student():

    student_id = id_entry.get().strip()

    if student_id == "":

        messagebox.showwarning(
            "Warning",
            "Please enter Student ID."
        )

        return

    name = name_entry.get().strip()
    course = course_entry.get().strip()
    phone = phone_entry.get().strip()

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM students WHERE id = ?
    """, (student_id,))

    if cur.fetchone() is None:

        conn.close()

        messagebox.showerror(
            "Error",
            "Student ID not found."
        )

        return

    cur.execute("""
        UPDATE students
        SET name = ?,
            course = ?,
            phone = ?,
            photo = ?
        WHERE id = ?
    """, (
        name,
        course,
        phone,
        photo_path,
        student_id
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Student Updated Successfully!"
    )


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():

    student_id = id_entry.get().strip()

    if student_id == "":

        messagebox.showwarning(
            "Warning",
            "Please enter Student ID."
        )

        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if not confirm:
        return

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()

    deleted = cur.rowcount

    conn.close()

    if deleted > 0:

        messagebox.showinfo(
            "Success",
            "Student Deleted Successfully!"
        )

        clear_student_fields()

    else:

        messagebox.showerror(
            "Error",
            "Student ID not found."
        )


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    student_id = search_entry.get().strip()

    if student_id == "":

        messagebox.showwarning(
            "Warning",
            "Enter Student ID."
        )

        return

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, course, phone, photo
        FROM students
        WHERE id = ?
    """, (student_id,))

    data = cur.fetchone()

    conn.close()

    if data:

        result_label.config(
            text=
            f"ID: {data[0]}\n"
            f"Name: {data[1]}\n"
            f"Course: {data[2]}\n"
            f"Phone: {data[3]}"
        )

        id_entry.delete(0, tk.END)
        id_entry.insert(0, data[0])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, data[1])

        course_entry.delete(0, tk.END)
        course_entry.insert(0, data[2])

        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, data[3])

        # Display photo
        if data[4] and os.path.exists(data[4]):

            try:

                img = Image.open(data[4])
                img = img.resize((120, 120))

                img = ImageTk.PhotoImage(img)

                photo_label.config(image=img)
                photo_label.image = img

            except:
                pass

    else:

        result_label.config(
            text="Student Not Found"
        )


# =========================================================
# CLEAR STUDENT FIELDS
# =========================================================

def clear_student_fields():

    global photo_path

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

    search_entry.delete(0, tk.END)

    result_label.config(text="")

    photo_label.config(image="")

    photo_label.image = None

    photo_path = ""


# =========================================================
# SHOW STUDENTS
# =========================================================

def show_students():

    win = tk.Toplevel()
    win.title("Student List")
    win.geometry("700x400")

    tk.Label(
        win,
        text="STUDENT LIST",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(
        frame,
        columns=("ID", "Name", "Course", "Phone"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Course", text="Course")
    tree.heading("Phone", text="Phone")

    tree.column("ID", width=60)
    tree.column("Name", width=180)
    tree.column("Course", width=150)
    tree.column("Phone", width=150)

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, course, phone
        FROM students
        ORDER BY id
    """)

    rows = cur.fetchall()

    conn.close()

    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )


# =========================================================
# STUDENT MANAGEMENT WINDOW
# =========================================================

def student_window():

    global name_entry
    global course_entry
    global phone_entry
    global id_entry
    global search_entry
    global result_label
    global photo_label

    win = tk.Toplevel()
    win.title("Student Management")
    win.geometry("500x700")
    win.resizable(False, False)

    tk.Label(
        win,
        text="STUDENT MANAGEMENT",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(win, text="Student ID").pack()

    id_entry = tk.Entry(
        win,
        width=35
    )

    id_entry.pack(pady=5)

    tk.Label(win, text="Student Name").pack()

    name_entry = tk.Entry(
        win,
        width=35
    )

    name_entry.pack(pady=5)

    tk.Label(win, text="Course").pack()

    course_entry = tk.Entry(
        win,
        width=35
    )

    course_entry.pack(pady=5)

    tk.Label(win, text="Phone").pack()

    phone_entry = tk.Entry(
        win,
        width=35
    )

    phone_entry.pack(pady=5)

    photo_label = tk.Label(
        win,
        text="No Photo"
    )

    photo_label.pack(pady=10)

    tk.Button(
        win,
        text="Upload Photo",
        command=upload_photo
    ).pack(pady=5)

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Student",
        width=15,
        command=add_student
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Update Student",
        width=15,
        command=update_student
    ).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Delete Student",
        width=15,
        command=delete_student
    ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_student_fields
    ).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(
        win,
        text="Search Student By ID",
        font=("Arial", 11, "bold")
    ).pack(pady=10)

    search_entry = tk.Entry(
        win,
        width=35
    )

    search_entry.pack()

    tk.Button(
        win,
        text="Search Student",
        width=20,
        command=search_student
    ).pack(pady=8)

    result_label = tk.Label(
        win,
        text="",
        font=("Arial", 10)
    )

    result_label.pack(pady=10)

    tk.Button(
        win,
        text="Show All Students",
        width=20,
        command=show_students
    ).pack(pady=10)


# =========================================================
# TEACHER PANEL
# =========================================================

def teacher_panel():

    win = tk.Tk()

    win.title("Teacher Panel")
    win.geometry("400x350")

    tk.Label(
        win,
        text="TEACHER DASHBOARD",
        font=("Arial", 18, "bold")
    ).pack(pady=25)

    tk.Button(
        win,
        text="View Students",
        width=25,
        command=show_students
    ).pack(pady=10)

    tk.Button(
        win,
        text="Attendance Graph",
        width=25,
        command=show_graph
    ).pack(pady=10)

    tk.Button(
        win,
        text="Logout",
        width=25,
        command=lambda: logout(win)
    ).pack(pady=10)

    win.mainloop()


# =========================================================
# TEACHER MANAGEMENT
# =========================================================

def teacher_window():

    win = tk.Toplevel()

    win.title("Teacher Management")
    win.geometry("400x350")

    tk.Label(
        win,
        text="TEACHER MANAGEMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        win,
        text="Teacher Name"
    ).pack()

    tname = tk.Entry(
        win,
        width=30
    )

    tname.pack(pady=5)

    tk.Label(
        win,
        text="Subject"
    ).pack()

    subject = tk.Entry(
        win,
        width=30
    )

    subject.pack(pady=5)

    def add_teacher():

        name = tname.get().strip()
        sub = subject.get().strip()

        if name == "" or sub == "":

            messagebox.showwarning(
                "Warning",
                "Please enter teacher name and subject."
            )

            return

        conn = sqlite3.connect("college.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO teachers(name, subject)
            VALUES (?, ?)
        """, (name, sub))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Teacher Added Successfully!"
        )

        tname.delete(0, tk.END)
        subject.delete(0, tk.END)

    tk.Button(
        win,
        text="Add Teacher",
        width=20,
        command=add_teacher
    ).pack(pady=20)


# =========================================================
# LIBRARY
# =========================================================

def library_window():

    win = tk.Toplevel()

    win.title("Library")
    win.geometry("400x350")

    tk.Label(
        win,
        text="LIBRARY MANAGEMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        win,
        text="Book Name"
    ).pack()

    bname = tk.Entry(
        win,
        width=30
    )

    bname.pack(pady=5)

    tk.Label(
        win,
        text="Author"
    ).pack()

    author = tk.Entry(
        win,
        width=30
    )

    author.pack(pady=5)

    def add_book():

        book = bname.get().strip()
        auth = author.get().strip()

        if book == "" or auth == "":

            messagebox.showwarning(
                "Warning",
                "Please enter book name and author."
            )

            return

        conn = sqlite3.connect("college.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO books(name, author)
            VALUES (?, ?)
        """, (book, auth))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Book Added Successfully!"
        )

        bname.delete(0, tk.END)
        author.delete(0, tk.END)

    tk.Button(
        win,
        text="Add Book",
        width=20,
        command=add_book
    ).pack(pady=20)


# =========================================================
# ATTENDANCE GRAPH
# =========================================================

def show_graph():

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Present'
    """)

    present = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Absent'
    """)

    absent = cur.fetchone()[0]

    conn.close()

    # If no attendance data exists
    if present == 0 and absent == 0:

        present = 20
        absent = 5

    labels = [
        "Present",
        "Absent"
    ]

    values = [
        present,
        absent
    ]

    plt.figure(figsize=(7, 5))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Attendance Graph"
    )

    plt.xlabel(
        "Attendance Status"
    )

    plt.ylabel(
        "Number of Records"
    )

    plt.tight_layout()

    plt.show()


# =========================================================
# STUDENT PANEL
# =========================================================

def student_panel():

    win = tk.Tk()

    win.title("Student Panel")
    win.geometry("400x350")

    tk.Label(
        win,
        text="STUDENT PANEL",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Button(
        win,
        text="View Students",
        width=25,
        command=show_students
    ).pack(pady=10)

    tk.Button(
        win,
        text="View Attendance Graph",
        width=25,
        command=show_graph
    ).pack(pady=10)

    tk.Button(
        win,
        text="Logout",
        width=25,
        command=lambda: logout(win)
    ).pack(pady=10)

    win.mainloop()


# =========================================================
# REGISTER USER
# =========================================================

def register_window():

    win = tk.Toplevel()

    win.title("Register User")
    win.geometry("400x450")

    tk.Label(
        win,
        text="REGISTER NEW USER",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        win,
        text="Username"
    ).pack()

    u = tk.Entry(
        win,
        width=30
    )

    u.pack(pady=5)

    tk.Label(
        win,
        text="Password"
    ).pack()

    p = tk.Entry(
        win,
        width=30,
        show="*"
    )

    p.pack(pady=5)

    tk.Label(
        win,
        text="Role"
    ).pack()

    role = ttk.Combobox(
        win,
        values=[
            "admin",
            "teacher",
            "student"
        ],
        state="readonly",
        width=27
    )

    role.pack(pady=5)

    role.set("student")

    def register():

        username_value = u.get().strip()
        password_value = p.get().strip()
        role_value = role.get().strip()

        if (
            username_value == "" or
            password_value == "" or
            role_value == ""
        ):

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return

        conn = sqlite3.connect("college.db")
        cur = conn.cursor()

        try:

            cur.execute("""
                INSERT INTO users
                (username, password, role)
                VALUES (?, ?, ?)
            """, (
                username_value,
                password_value,
                role_value
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "User Created Successfully!"
            )

            u.delete(0, tk.END)
            p.delete(0, tk.END)

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Username already exists."
            )

        finally:

            conn.close()

    tk.Button(
        win,
        text="Create User",
        width=20,
        command=register
    ).pack(pady=25)


# =========================================================
# START APPLICATION
# =========================================================

connect_db()

login_window()
