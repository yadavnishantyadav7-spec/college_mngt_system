import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

photo_path = ""

# ---------------- DATABASE ----------------

def connect_db():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    phone TEXT,
    photo TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    author TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO users(id,username,password,role)
    VALUES(1,'admin','admin123','admin')
    """)

    conn.commit()
    conn.close()

# ---------------- LOGIN ----------------

def check_login():

    user = username.get()
    pwd = password.get()

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=Nishant1 AND password=123",
        (user,pwd)
    )

    result = cur.fetchone()

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
        status.config(text="Invalid Login")

# ---------------- DASHBOARD ----------------

def dashboard():

    win = tk.Tk()
    win.title("Admin Dashboard")
    win.geometry("400x500")

    tk.Label(win,text="Admin Control Panel",
             font=("Arial",16)).pack(pady=20)

    tk.Button(win,text="Student Management",
              command=student_window).pack(pady=5)

    tk.Button(win,text="Teacher Management",
              command=teacher_window).pack(pady=5)

    tk.Button(win,text="Library",
              command=library_window).pack(pady=5)

    tk.Button(win,text="View Students",
              command=show_students).pack(pady=5)

    tk.Button(win,text="Register User",
              command=register_window).pack(pady=5)

    tk.Button(win,text="Attendance Graph",
              command=show_graph).pack(pady=5)

    win.mainloop()

# ---------------- PHOTO ----------------

def upload_photo():

    global photo_path

    photo_path = filedialog.askopenfilename()

    img = Image.open(photo_path)
    img = img.resize((100,100))
    img = ImageTk.PhotoImage(img)

    photo_label.config(image=img)
    photo_label.image = img

# ---------------- STUDENT ----------------

def add_student():

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute(
    "INSERT INTO students(name,course,phone,photo) VALUES(?,?,?,?)",
    (name_entry.get(),course_entry.get(),phone_entry.get(),photo_path)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success","Student Added")

def update_student():

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute(
    "UPDATE students SET name=?,course=?,phone=? WHERE id=?",
    (name_entry.get(),course_entry.get(),phone_entry.get(),id_entry.get())
    )

    conn.commit()
    conn.close()

def delete_student():

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?",(id_entry.get(),))

    conn.commit()
    conn.close()

def search_student():

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id=?",(search_entry.get(),))

    data = cur.fetchone()

    result_label.config(text=str(data))

    conn.close()

# ---------------- STUDENT LIST TABLE ----------------

def show_students():

    win = tk.Tk()
    win.title("Student List")

    tree = ttk.Treeview(win)

    tree["columns"]=("ID","Name","Course","Phone")

    tree.column("#0",width=0)
    tree.column("ID",width=50)
    tree.column("Name",width=150)
    tree.column("Course",width=120)
    tree.column("Phone",width=120)

    tree.heading("ID",text="ID")
    tree.heading("Name",text="Name")
    tree.heading("Course",text="Course")
    tree.heading("Phone",text="Phone")

    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()

    for row in rows:
        tree.insert("",tk.END,values=(row[0],row[1],row[2],row[3]))

    conn.close()

    tree.pack(fill="both",expand=True)

    win.mainloop()

# ---------------- STUDENT WINDOW ----------------

def student_window():

    global name_entry,course_entry,phone_entry,id_entry
    global search_entry,result_label,photo_label

    win = tk.Tk()
    win.title("Student Management")

    tk.Label(win,text="ID").pack()
    id_entry = tk.Entry(win)
    id_entry.pack()

    tk.Label(win,text="Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win,text="Course").pack()
    course_entry = tk.Entry(win)
    course_entry.pack()

    tk.Label(win,text="Phone").pack()
    phone_entry = tk.Entry(win)
    phone_entry.pack()

    photo_label = tk.Label(win)
    photo_label.pack()

    tk.Button(win,text="Upload Photo",
              command=upload_photo).pack()

    tk.Button(win,text="Add Student",
              command=add_student).pack()

    tk.Button(win,text="Update Student",
              command=update_student).pack()

    tk.Button(win,text="Delete Student",
              command=delete_student).pack()

    tk.Label(win,text="Search ID").pack()

    search_entry = tk.Entry(win)
    search_entry.pack()

    tk.Button(win,text="Search",
              command=search_student).pack()

    result_label = tk.Label(win,text="")
    result_label.pack()

    tk.Button(win,text="Show Students",
              command=show_students).pack()

    win.mainloop()

# ---------------- TEACHER ----------------

def teacher_panel():

    win = tk.Tk()
    win.title("Teacher Panel")

    tk.Label(win,text="Teacher Dashboard",
             font=("Arial",16)).pack()

    tk.Button(win,text="View Students",
              command=show_students).pack()

    tk.Button(win,text="Attendance Graph",
              command=show_graph).pack()

    win.mainloop()


def student_panel():

    win = tk.Tk()
    win.title("Student Panel")
    win.geometry("300x300")

    tk.Label(win, text="Student Panel", font=("Arial", 16)).pack(pady=20)

    tk.Button(win, text="View Graph", command=show_graph).pack(pady=5)

    win.mainloop()

def teacher_window():

    win = tk.Tk()
    win.title("Teacher Management")

    tk.Label(win,text="Name").pack()
    tname = tk.Entry(win)
    tname.pack()

    tk.Label(win,text="Subject").pack()
    subject = tk.Entry(win)
    subject.pack()

    def add_teacher():
        conn = sqlite3.connect("college.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO teachers(name,subject) VALUES(?,?)",
        (tname.get(),subject.get())
        )

        conn.commit()
        conn.close()

    tk.Button(win,text="Add Teacher",
              command=add_teacher).pack()

    win.mainloop()

# ---------------- LIBRARY ----------------

def library_window():

    win = tk.Tk()
    win.title("Library")

    tk.Label(win,text="Book Name").pack()
    bname = tk.Entry(win)
    bname.pack()

    tk.Label(win,text="Author").pack()
    author = tk.Entry(win)
    author.pack()

    def add_book():

        conn = sqlite3.connect("college.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO books(name,author) VALUES(?,?)",
        (bname.get(),author.get())
        )

        conn.commit()
        conn.close()

    tk.Button(win,text="Add Book",
              command=add_book).pack()

    win.mainloop()

# ---------------- GRAPH ----------------

def show_graph():

    labels = ["Present","Absent"]
    values = [20,5]

    plt.bar(labels,values)
    plt.title("Attendance Graph")
    plt.show()

# ---------------- REGISTER USER ----------------

def register_window():

    win = tk.Tk()
    win.title("Register User")

    tk.Label(win,text="Username").pack()
    u = tk.Entry(win)
    u.pack()

    tk.Label(win,text="Password").pack()
    p = tk.Entry(win)
    p.pack()

    tk.Label(win,text="Role (admin/teacher/student)").pack()
    r = tk.Entry(win)
    r.pack()

    def register():

        conn = sqlite3.connect("college.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO users(username,password,role) VALUES(?,?,?)",
        (u.get(),p.get(),r.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","User Created")

    tk.Button(win,text="Create User",
              command=register).pack()

    win.mainloop()

# ---------------- LOGIN WINDOW ----------------

connect_db()

root = tk.Tk()
root.title("College Login")
root.geometry("300x200")

tk.Label(root,text="Username").pack()
username = tk.Entry(root)
username.pack()

tk.Label(root,text="Password").pack()
password = tk.Entry(root,show="*")
password.pack()

tk.Button(root,text="Login",
          command=check_login).pack(pady=10)

status = tk.Label(root,text="")
status.pack()

root.mainloop()