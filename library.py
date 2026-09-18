# Define Library class
class Library:
    
    # Constructor method (runs automatically when object is created)
    def __init__(self):
        self.books = {}      # Dictionary to store book details
        self.students = {}   # Dictionary to store student details
        self.add_default_books()  # Call function to add default books
    
    # Function to add default BCA and Pharmacy books
    def add_default_books(self):
        
        # BCA Books added to books dictionary
        # Each book has: title, issued status, and student who issued it
        self.books["B101"] = {"title": "Programming in C", "issued": False, "student": None}
        self.books["B102"] = {"title": "Data Structures", "issued": False, "student": None}
        self.books["B103"] = {"title": "Database Management System", "issued": False, "student": None}
        
        # Pharmacy Books added
        self.books["P201"] = {"title": "Pharmacology", "issued": False, "student": None}
        self.books["P202"] = {"title": "Pharmaceutics", "issued": False, "student": None}
        self.books["P203"] = {"title": "Pharmaceutical Chemistry", "issued": False, "student": None}

    # Function to add a new student
    def add_student(self, student_id, name, course):
        
        # Check if student ID already exists
        if student_id in self.students:
            print("Student ID already exists!")
        else:
            # Add student details in dictionary
            self.students[student_id] = {
                "name": name,
                "course": course
            }
            print("Student added successfully!")

    # Function to display all students
    def view_students(self):
        
        # If no students exist
        if not self.students:
            print("No students available.")
        else:
            # Loop through student dictionary
            for sid, details in self.students.items():
                print(f"ID: {sid}, Name: {details['name']}, Course: {details['course']}")

    # Function to display all books
    def view_books(self):
        
        # Loop through books dictionary
        for book_id, details in self.books.items():
            
            # Check book status
            status = "Issued" if details["issued"] else "Available"
            
            # Check which student issued it
            issued_to = details["student"] if details["student"] else "None"
            
            # Print book details
            print(f"ID: {book_id}, Title: {details['title']}, Status: {status}, Issued To: {issued_to}")

    # Function to issue a book to a student
    def issue_book(self, book_id, student_id):
        
        # Check if book exists
        if book_id not in self.books:
            print("Book ID not found!")
            return
        
        # Check if student exists
        if student_id not in self.students:
            print("Student ID not found!")
            return
        
        # Check if book is already issued
        if not self.books[book_id]["issued"]:
            
            # Mark book as issued
            self.books[book_id]["issued"] = True
            
            # Store student name who issued the book
            self.books[book_id]["student"] = self.students[student_id]["name"]
            
            print("Book issued successfully!")
        else:
            print("Book is already issued.")

    # Function to return a book
    def return_book(self, book_id):
        
        # Check if book exists AND is issued
        if book_id in self.books and self.books[book_id]["issued"]:
            
            # Mark book as not issued
            self.books[book_id]["issued"] = False
            
            # Remove student name
            self.books[book_id]["student"] = None
            
            print("Book returned successfully!")
        else:
            print("Book not issued or not found!")


# ================= MAIN PROGRAM =================

# Create Library object
library = Library()

# Infinite loop to keep program running
while True:
    
    # Display menu options
    print("\n--- Library Management System ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. View Books")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Exit")

    # Take user choice
    choice = input("Enter your choice: ")

    # If user selects option 1
    if choice == "1":
        sid = input("Enter Student ID: ")
        name = input("Enter Student Name: ")
        course = input("Enter Course (BCA/Pharmacy): ")
        library.add_student(sid, name, course)

    # If user selects option 2
    elif choice == "2":
        library.view_students()

    # If user selects option 3
    elif choice == "3":
        library.view_books()

    # If user selects option 4
    elif choice == "4":
        book_id = input("Enter Book ID: ")
        student_id = input("Enter Student ID: ")
        library.issue_book(book_id, student_id)

    # If user selects option 5
    elif choice == "5":
        book_id = input("Enter Book ID: ")
        library.return_book(book_id)

    # If user selects option 6
    elif choice == "6":
        print("Exiting program...")
        break   # Stop loop and end program

    # If user enters wrong choice
    else:
        print("Invalid choice! Try again.")