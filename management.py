import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

photo_path=""

# ---------------- DATABASE ----------------

def connect_db():

    conn = sqlite3.connect("ai_college_erp.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    phone TEXT,
    photo TEXT
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

    user=username.get()
    pwd=password.get()

    conn=sqlite3.connect("ai_college_erp.db")
    cur=conn.cursor()

    cur.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (user,pwd)
    )

    result=cur.fetchone()

    conn.close()

    if result:

        root.destroy()
        dashboard()

    else:
        status.config(text="Invalid Login")

# ---------------- DASHBOARD ----------------

def dashboard():

    win=tk.Tk()
    win.title("AI Smart College ERP")
    win.geometry("900x550")

    sidebar=tk.Frame(win,bg="#2c3e50",width=200)
    sidebar.pack(side="left",fill="y")

    main=tk.Frame(win,bg="white")
    main.pack(side="right",expand=True,fill="both")

    tk.Label(sidebar,text="ERP PANEL",
             bg="#2c3e50",
             fg="white",
             font=("Arial",16)).pack(pady=20)

    tk.Button(sidebar,text="Students",
              width=20,
              command=lambda:student_window(main)).pack(pady=5)

    tk.Button(sidebar,text="Teachers",
              width=20,
              command=lambda:teacher_window(main)).pack(pady=5)

    tk.Button(sidebar,text="Library",
              width=20,
              command=lambda:library_window(main)).pack(pady=5)

    tk.Button(sidebar,text="Attendance Graph",
              width=20,
              command=attendance_graph).pack(pady=5)

    tk.Button(sidebar,text="AI Assistant",
              width=20,
              command=ai_chatbot).pack(pady=5)

    tk.Label(main,text="Welcome to AI College ERP",
             font=("Arial",22)).pack(pady=50)

    win.mainloop()

# ---------------- PHOTO UPLOAD ----------------

def upload_photo():

    global photo_path

    photo_path=filedialog.askopenfilename(
    filetypes=[("Image Files","*.png *.jpg *.jpeg")]
    )

    img=Image.open(photo_path)
    img=img.resize((100,100))

    img=ImageTk.PhotoImage(img)

    photo_label.config(image=img)
    photo_label.image=img

# ---------------- STUDENT ----------------

def student_window(frame):

    global photo_label

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame,text="Student Management",
             font=("Arial",18)).pack(pady=10)

    name=tk.Entry(frame)
    name.pack()

    course=tk.Entry(frame)
    course.pack()

    phone=tk.Entry(frame)
    phone.pack()

    photo_label=tk.Label(frame)
    photo_label.pack()

    tk.Button(frame,text="Upload Photo",
              command=upload_photo).pack(pady=5)

    def add_student():

        conn=sqlite3.connect("ai_college_erp.db")
        cur=conn.cursor()

        cur.execute(
        "INSERT INTO students(name,course,phone,photo) VALUES(?,?,?,?)",
        (name.get(),course.get(),phone.get(),photo_path)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Student Added")

    tk.Button(frame,text="Add Student",
              command=add_student).pack(pady=10)

    tree=ttk.Treeview(frame)

    tree["columns"]=("ID","Name","Course","Phone")

    tree.heading("ID",text="ID")
    tree.heading("Name",text="Name")
    tree.heading("Course",text="Course")
    tree.heading("Phone",text="Phone")

    conn=sqlite3.connect("ai_college_erp.db")
    cur=conn.cursor()

    cur.execute("SELECT * FROM students")

    rows=cur.fetchall()

    for r in rows:
        tree.insert("",tk.END,values=(r[0],r[1],r[2],r[3]))

    conn.close()

    tree.pack(fill="both",expand=True)

# ---------------- TEACHER ----------------

def teacher_window(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame,text="Teacher Management",
             font=("Arial",18)).pack(pady=10)

    name=tk.Entry(frame)
    name.pack()

    subject=tk.Entry(frame)
    subject.pack()

    def add_teacher():

        conn=sqlite3.connect("ai_college_erp.db")
        cur=conn.cursor()

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

    book=tk.Entry(frame)
    book.pack()

    author=tk.Entry(frame)
    author.pack()

    def add_book():

        conn=sqlite3.connect("ai_college_erp.db")
        cur=conn.cursor()

        cur.execute(
        "INSERT INTO books(name,author) VALUES(?,?)",
        (book.get(),author.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Book Added")

    tk.Button(frame,text="Add Book",
              command=add_book).pack(pady=10)

# ---------------- GRAPH ----------------

def attendance_graph():

    labels=["Present","Absent"]
    values=[85,15]

    plt.bar(labels,values)

    plt.title("Attendance Report")

    plt.show()

# ---------------- PDF ----------------

def generate_pdf():

    c=canvas.Canvas("report.pdf")

    c.drawString(100,750,"College ERP Report")
    c.drawString(100,700,"Student Data")

    c.save()

    messagebox.showinfo("Success","PDF Generated")

# ---------------- AI CHATBOT ----------------

def ai_chatbot():

    win=tk.Toplevel()
    win.title("AI Assistant")

    chat=tk.Text(win,height=15,width=50)
    chat.pack()

    entry=tk.Entry(win,width=40)
    entry.pack()

    def send():

        msg=entry.get().lower()

        if "fees" in msg:
            reply="Fees can be paid in accounts department."

        elif "library" in msg:
            reply="Library timing is 9 AM to 4 PM."

        elif "admission" in msg:
            reply="Contact admin office for admission."

        else:
            reply="Sorry I don't understand."

        chat.insert(tk.END,"You: "+msg+"\n")
        chat.insert(tk.END,"AI: "+reply+"\n\n")

        entry.delete(0,tk.END)

    tk.Button(win,text="Send",command=send).pack()

# ---------------- MAIN ----------------

connect_db()

root=tk.Tk()
root.title("AI College ERP Login")
root.geometry("300x200")

tk.Label(root,text="Username").pack()
username=tk.Entry(root)
username.pack()

tk.Label(root,text="Password").pack()
password=tk.Entry(root,show="*")
password.pack()

tk.Button(root,text="Login",command=login).pack(pady=10)

status=tk.Label(root,text="")
status.pack()

root.mainloop()