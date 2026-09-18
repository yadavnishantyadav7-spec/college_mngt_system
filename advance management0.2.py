import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

# ---------------- DATABASE ----------------

def connect_db():

    conn = sqlite3.connect("college_erp.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    phone TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    author TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO users(id,username,password)
    VALUES(1,'admin','admin123')
    """)

    conn.commit()
    conn.close()


# ---------------- LOGIN ----------------

def login():

    user = username.get()
    pwd = password.get()

    conn = sqlite3.connect("college_erp.db")
    cur = conn.cursor()

    cur.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (user,pwd)
    )

    result = cur.fetchone()
    conn.close()

    if result:
        root.destroy()
        dashboard()

    else:
        status.config(text="Invalid Login")


# ---------------- DASHBOARD ----------------

def dashboard():

    win = tk.Tk()
    win.title("College ERP System")
    win.geometry("900x550")

    sidebar = tk.Frame(win,bg="#2c3e50",width=200)
    sidebar.pack(side="left",fill="y")

    main = tk.Frame(win,bg="white")
    main.pack(side="right",expand=True,fill="both")

    tk.Label(sidebar,text="ERP PANEL",
             bg="#2c3e50",
             fg="white",
             font=("Arial",16)).pack(pady=20)

    tk.Button(sidebar,text="Dashboard",
              width=20,
              command=lambda:show_dashboard(main)).pack(pady=5)

    tk.Button(sidebar,text="Students",
              width=20,
              command=lambda:student_window(main)).pack(pady=5)

    tk.Button(sidebar,text="Teachers",
              width=20,
              command=lambda:teacher_window(main)).pack(pady=5)

    tk.Button(sidebar,text="Library",
              width=20,
              command=lambda:library_window(main)).pack(pady=5)

    tk.Button(sidebar,text="Attendance",
              width=20,
              command=attendance_graph).pack(pady=5)

    show_dashboard(main)

    win.mainloop()


# ---------------- DASHBOARD SCREEN ----------------

def show_dashboard(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame,text="College ERP Dashboard",
             font=("Arial",22)).pack(pady=30)

    tk.Label(frame,text="Welcome Admin",
             font=("Arial",16)).pack(pady=10)


# ---------------- STUDENTS ----------------

def student_window(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame,text="Student Management",
             font=("Arial",18)).pack(pady=10)

    name = tk.Entry(frame)
    name.pack(pady=5)
    name.insert(0,"Name")

    course = tk.Entry(frame)
    course.pack(pady=5)
    course.insert(0,"Course")

    phone = tk.Entry(frame)
    phone.pack(pady=5)
    phone.insert(0,"Phone")

    def add_student():

        conn = sqlite3.connect("college_erp.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO students(name,course,phone) VALUES(?,?,?)",
        (name.get(),course.get(),phone.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Student Added")
        load_students()

    tk.Button(frame,text="Add Student",
              command=add_student).pack(pady=10)

    tree = ttk.Treeview(frame)

    tree["columns"]=("ID","Name","Course","Phone")

    tree.column("#0",width=0)

    tree.heading("ID",text="ID")
    tree.heading("Name",text="Name")
    tree.heading("Course",text="Course")
    tree.heading("Phone",text="Phone")

    def load_students():

        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect("college_erp.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

        for r in rows:
            tree.insert("",tk.END,values=r)

        conn.close()

    load_students()

    tree.pack(fill="both",expand=True)


# ---------------- TEACHERS ----------------

def teacher_window(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame,text="Teacher Management",
             font=("Arial",18)).pack(pady=10)

    name = tk.Entry(frame)
    name.pack(pady=5)
    name.insert(0,"Teacher Name")

    subject = tk.Entry(frame)
    subject.pack(pady=5)
    subject.insert(0,"Subject")

    def add_teacher():

        conn = sqlite3.connect("college_erp.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO teachers(name,subject) VALUES(?,?)",
        (name.get(),subject.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Teacher Added")

    tk.Button(frame,text="Add Teacher",
              command=add_teacher).pack(pady=10)


# ---------------- LIBRARY ----------------

def library_window(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame,text="Library Management",
             font=("Arial",18)).pack(pady=10)

    name = tk.Entry(frame)
    name.pack(pady=5)
    name.insert(0,"Book Name")

    author = tk.Entry(frame)
    author.pack(pady=5)
    author.insert(0,"Author")

    def add_book():

        conn = sqlite3.connect("college_erp.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO books(name,author) VALUES(?,?)",
        (name.get(),author.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Book Added")

    tk.Button(frame,text="Add Book",
              command=add_book).pack(pady=10)


# ---------------- GRAPH ----------------

def attendance_graph():

    labels = ["Present","Absent"]
    values = [80,20]

    plt.bar(labels,values)

    plt.title("Attendance Report")
    plt.show()


# ---------------- PDF RECEIPT ----------------

def generate_receipt():

    c = canvas.Canvas("fees_receipt.pdf")

    c.drawString(100,750,"College ERP Fee Receipt")
    c.drawString(100,700,"Student Fees Paid")

    c.save()

    messagebox.showinfo("Success","PDF Generated")


# ---------------- MAIN ----------------

connect_db()

root = tk.Tk()
root.title("College ERP Login")
root.geometry("300x200")

tk.Label(root,text="Username").pack()
username = tk.Entry(root)
username.pack()

tk.Label(root,text="Password").pack()
password = tk.Entry(root,show="*")
password.pack()

tk.Button(root,text="Login",command=login).pack(pady=10)

status = tk.Label(root,text="")
status.pack()

root.mainloop()