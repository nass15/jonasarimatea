import tkinter as tk

from PIL import Image, ImageTk

from tkinter import messagebox

import sqlite3

import os



login_frame = None

admin_login_frame = None

sign_up_frame = None

selected_icon_filename = None

current_user_id = None

current_points = 0

books_read_count = 0

read_books = set()  # Track books read in the current session





# Custom style for buttons with rounded corners

class RoundButton(tk.Button):

    def __init__(self, master=None, **kwargs):

        super().__init__(master, **kwargs)

        self.config(relief="flat", borderwidth=0)





def setup_database():

    conn = sqlite3.connect("users.db")

    c = conn.cursor()



    # Ensure the users table exists with the points column

    c.execute(

        """CREATE TABLE IF NOT EXISTS users 

                 (username TEXT PRIMARY KEY, 

                  password TEXT, 

                  avatar TEXT DEFAULT NULL,

                  selected_icon_filename TEXT DEFAULT NULL,

                  points INTEGER DEFAULT 0)"""

    )



    # In case the table already exists without the points column, add it

    try:

        c.execute("ALTER TABLE users ADD COLUMN points INTEGER DEFAULT 0")

    except sqlite3.OperationalError:

        # The column already exists, so we catch the error silently

        pass



    # Create or ensure the leaderboards table exists

    c.execute(

        """CREATE TABLE IF NOT EXISTS leaderboards 

                 (username TEXT PRIMARY KEY, 

                  points INTEGER DEFAULT 0)"""

    )



    # Create or ensure the read_books table exists with book_key

    c.execute(

        """CREATE TABLE IF NOT EXISTS read_books 

                 (username TEXT, 

                  book_key TEXT, 

                  PRIMARY KEY (username, book_key),

                  FOREIGN KEY (username) REFERENCES users(username))"""

    )



    # If the table exists but book_key does not, add it

    try:

        c.execute("SELECT book_key FROM read_books LIMIT 1")

    except sqlite3.OperationalError:

        c.execute("ALTER TABLE read_books ADD COLUMN book_key TEXT")



    conn.commit()

    conn.close()



    # Optionally, ensure all existing users have a points value (if not already set)

    conn = sqlite3.connect("users.db")

    c = conn.cursor()

    c.execute("UPDATE users SET points = 0 WHERE points IS NULL")

    conn.commit()

    conn.close()





def register_user():

    username = username_entry.get()

    password = password_entry.get()

    reenter_password = reenterpassword_entry.get()



    if username and password and reenter_password:

        if password == reenter_password:

            try:

                conn = sqlite3.connect("users.db")

                c = conn.cursor()



                c.execute("SELECT * FROM users WHERE username = ?", (username,))

                if c.fetchone() is None:

                    avatar = selected_icon_filename if selected_icon_filename else None



                    c.execute(

                        """INSERT INTO users (username, password, avatar, selected_icon_filename, points) 

                                VALUES (?, ?, ?, ?, 0)""",

                        (username, password, avatar, selected_icon_filename),

                    )

                    conn.commit()

                    messagebox.showinfo("Success", "Registration successful!")

                    conn.close()



                    book_conn = sqlite3.connect("book_database.db")

                    book_c = book_conn.cursor()

                    create_table_sql = """

                    CREATE TABLE IF NOT EXISTS books (

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        title TEXT NOT NULL,

                        author TEXT NOT NULL,

                        cover_path TEXT

                    );

                    """

                    book_c.execute(create_table_sql)

                    book_conn.commit()



                    book_c.execute("SELECT COUNT(*) FROM books")

                    count = book_c.fetchone()[0]



                    if count == 0:

                        books = [

                            (

                                "The Information Superhighway Beyond the Internet",

                                "Peter Otte",

                                r"Images\\the information superhighway beyond the internet.png",

                            ),

                            (

                                "Using Microsoft Office",

                                "Unknown",

                                r"Images\\Using Microsoft office.png",

                            ),

                            (

                                "Word Processing Applications and Living Online",

                                "Unknown",

                                r"Images\Word processing.png",

                            ),

                            (

                                "M.S DOS 5.0 - User's Guide and Reference Condensed Edition",

                                "Unknown",

                                r"Images\\M.S DOS 5.0 - User's Guide and Reference Condensed Edition.jpg",

                            ),

                            (

                                "Microsoft Excel 2003 Proficiency in Electronic Spreadsheet",

                                "Unknown",

                                r"Images\\Microsoft Excel 2003 Proficiency in Electronic Spreadsheet.jpg",

                            ),

                            (

                                "Management Information Systems: Managing the Digital Firm",

                                "Kenneth C. Laudon, Jane P. Luadon",

                                r"Images\\Management Information Systems Managing the Digital Firm.jpg",

                            ),

                            (

                                "Photoshop Elements 3",

                                "Craig Hoeschen",

                                r"Images\\Photoshop Elements 3.jpg",

                            ),

                            (

                                "Digital And Analog Controls",

                                "Marvin A. Needler",

                                r"Images\Digital And Analog Controls.jpg",

                            ),

                            (

                                "Computer Software",

                                "Ivan Flores",

                                r"Images\\Computer Software.jpg",

                            ),

                            (

                                "Introductions to Computers Concepts",

                                "Juny Pilapil La Putt",

                                r"Images\\Introductions to Computers Concepts.jpg",

                            ),

                            (

                                "Data Structures and Algorithms",

                                "Alfred V. Aho, John E. Hopcroft, Jeffry D. Ullman",

                                r"Images\Data Structures and Algorithms.jpg",

                            ),

                            (

                                "Modern Cable Television Technology",

                                "Ciciora, Walter, Farmer, James and Large, David",

                                r"Images\\Modern Cable Television Technology.jpg",

                            ),

                            (

                                "Building PC for Dummies",

                                "Mark Chambers",

                                r"Images\Building PC for Dummies.jpg",

                            ),

                            (

                                "Lotus Notes Release 4 for Dummies",

                                "Londergan, Stephen and Freeland, Pat",

                                r"Images\\Lotus Notes Release 4 for Dummies.jpg",

                            ),

                            (

                                "Novell's Guide to NetWare 4.01 Networks",

                                "Currid, Cheryl C. , Stephen Saxon",

                                r"Images\\Novell's Guide to NetWare 4.01 Networks.jpg",

                            ),

                            (

                                "Computer Literacy Program: Worktext in Computer Skills for Grade 6",

                                "Unknown",

                                r"Images\\Computer Literacy Program Worktext in Computer Skills for Grade 6.jpg",

                            ),

                            (

                                "Understanding Structural Analysis",

                                "Kassimali, Aslam",

                                r"Images\\Understanding Structural Analysis.jpg",

                            ),

                            (

                                "Computers  and Information Processing",

                                "Unknown",

                                r"Images\\Computers  and Information Processing.jpg",

                            ),

                            (

                                "Sattelite Communication Systems",

                                "Richharia, M.",

                                r"Images\Sattelite Communication Systems.jpg",

                            ),

                            (

                                "Recreation Programming: Designing and Staging Leisure Experiences",

                                "Rossman, Robert J., and Schlatter, Barbara E.",

                                r"Images\\Recreation Programming Designing and Staging Leisure Experiences.jpg",

                            ),

                            (

                                "Antennas And Wave Propagation ",

                                "Chris Harvey",

                                r"Images\Antennas And Wave Propagation.jpg",

                            ),

                            (

                                "Auditing IT Infrastructures for Compliance",

                                "R.Johnson, M.Weiss, et al.",

                                r"Images\Auditing IT Infrastructures for Compliance.jpg",

                            ),

                            (

                                "Fundamentals of Internet of Things",

                                "Farzin John Dian",

                                r"Images\\Fundamentals of Internet of Things; For Students and Professionals.jpg",

                            ),

                            (

                                "Digital Electronics",

                                "R.Tokheim & P. Hoppe",

                                r"Images\Digital Electronics.jpg",

                            ),

                            (

                                "3D Printing for Energy Applications",

                                "Pandey, Mukesh",

                                r"Images\\3D Printing for Energy Applications.jpg",

                            ),

                            (

                                "Deep Learning Applications",

                                "Q.Xuan,Yun Xiang et al.",

                                r"Images\Deep Learning Applications In Computer Vision, Signals, and Networks.jpg",

                            ),

                            (

                                "Data Science for IOT Engineers",

                                "P.G. Madhavan",

                                r"Images\Data Science for IOT Engineers A Systems Analytics Approach.jpg",

                            ),

                            (

                                "Cognitive Computing for Human Robot Interaction",

                                "M.Mittal,R. Shah,et al.editor",

                                r"Images\\Cognitive Computing for Human Robot Interaction Principles and Practices.jpg",

                            ),

                            (

                                "Fundamentals of Electronic Materials and Devices",

                                "Avik ghosh",

                                r"Images\\Fundamentals of Electronic Materials and Devices A Gentle Introduction to the Quantum Classical World.jpg",

                            ),

                            (

                                "Digital Electronics: A Practical Approach",

                                "Kate Timberlake",

                                r"Images\Digital Electronics A Practical Approach - Copy.jpg",

                            ),

                            (

                                "A Framework for Marketing Management",

                                "Kotler, Philip and Keler Kevin LAne",

                                r"Images\A Framework for Marketing Management.jpg",

                            ),

                        ]



                        for book in books:

                            book_c.execute(

                                "INSERT INTO books (title, author, cover_path) VALUES (?, ?, ?)",

                                book,

                            )

                        book_conn.commit()



                    book_conn.close()



                    global current_user_id

                    current_user_id = username

                    setup_new_interface()

                    return True

                else:

                    messagebox.showerror("Error", "Username already exists!")

                    conn.close()

                    return False

            except sqlite3.Error as e:

                messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

                return False

            finally:

                if conn:

                    conn.close()

        else:

            messagebox.showerror("Error", "Passwords do not match!")

            return False

    else:

        messagebox.showerror("Error", "Please fill in all fields.")

        return False





# Function to toggle password visibility

def toggle_password_visibility(entry, var, check):

    if var.get():

        entry.config(show="")

        check.config(selectcolor="blue")

    else:

        entry.config(show="*")

        check.config(selectcolor="white")





# User login for general users

def login_user():

    username = username_entry.get()

    password = password_entry.get()



    if username and password:

        conn = sqlite3.connect("users.db")

        c = conn.cursor()

        c.execute(

            "SELECT * FROM users WHERE username = ? AND password = ?",

            (username, password),

        )

        user = c.fetchone()

        if user:

            global selected_icon_filename, current_user_id, current_points, books_read_count

            try:

                selected_icon_filename = user[3] if len(user) > 3 else None

                current_user_id = username

                current_points = user[4] if len(user) > 4 else 0  # Points from database

                books_read_count = (

                    current_points // 10

                )  # Assuming each book read gives 10 points



                # Load read books for this user

                c.execute(

                    "SELECT book_key FROM read_books WHERE username = ?", (username,)

                )

                read_books.clear()

                for book in c.fetchall():

                    read_books.add(book[0])



            except IndexError:

                selected_icon_filename = None

                current_points = 0

                books_read_count = 0

                print(

                    "Warning: selected_icon_filename or points not found in database."

                )



            messagebox.showinfo("Success", "Login successful!")

            setup_new_interface()

        else:

            messagebox.showerror("Error", "Invalid username or password.")

        conn.close()

    else:

        messagebox.showerror("Error", "Please enter both username and password.")





def on_login_student():

    global login_frame



    for widget in root.winfo_children():

        widget.place_forget()



    if login_frame is None or not login_frame.winfo_exists():

        login_frame = tk.Frame(root, bg="maroon")



        username_label = tk.Label(

            login_frame,

            text="PUP ID:",

            bg="maroon",

            fg="white",

            font=("Helvetica", 14, "bold"),

        )

        username_label.pack(pady=10)



        global username_entry

        username_entry = tk.Entry(

            login_frame, borderwidth=5, width=30, font=("Helvetica", 12)

        )

        username_entry.pack(pady=10)



        password_label = tk.Label(

            login_frame,

            text="Password:",

            bg="maroon",

            fg="white",

            font=("Helvetica", 14, "bold"),

        )

        password_label.pack(pady=10)



        global password_entry

        password_entry = tk.Entry(

            login_frame, borderwidth=5, show="*", width=30, font=("Helvetica", 12)

        )

        password_entry.pack(pady=10)



        show_password_var = tk.BooleanVar()

        show_password_check = tk.Checkbutton(

            login_frame,

            text="Show Password",

            variable=show_password_var,

            command=lambda: toggle_password_visibility(

                password_entry, show_password_var, show_password_check

            ),

            bg="maroon",

            fg="white",

            selectcolor="white",

            activebackground="darkred",

            indicatoron=1,

            height=1,

            width=15,

        )

        show_password_check.pack(pady=5, anchor="c")



        login_button = tk.Button(

            login_frame,

            text="Login",

            command=login_user,

            bg="#FFD700",

            fg="maroon",

            font=("Helvetica", 12),

            width=10,

            height=1,

        )

        login_button.pack(pady=10)



        back_button = tk.Button(

            login_frame,

            text="Back",

            command=go_back,

            bg="white",

            fg="maroon",

            font=("Helvetica", 12),

            width=10,

            height=1,

        )

        back_button.pack(pady=10)



    login_frame.pack(fill="both", expand=True)

    login_frame.lift()





def on_login_admin():

    global admin_login_frame



    for widget in root.winfo_children():

        widget.place_forget()



    if admin_login_frame is None or not admin_login_frame.winfo_exists():

        admin_login_frame = tk.Frame(root, bg="maroon")



        admin_username_label = tk.Label(

            admin_login_frame,

            text="Admin Username:",

            bg="maroon",

            fg="white",

            font=("Helvetica", 14, "bold"),

        )

        admin_username_label.pack(pady=10)



        global admin_username_entry

        admin_username_entry = tk.Entry(

            admin_login_frame, borderwidth=5, width=30, font=("Helvetica", 12)

        )

        admin_username_entry.pack(pady=10)



        admin_password_label = tk.Label(

            admin_login_frame,

            text="Admin Password:",

            bg="maroon",

            fg="white",

            font=("Helvetica", 14, "bold"),

        )

        admin_password_label.pack(pady=10)



        global admin_password_entry

        admin_password_entry = tk.Entry(

            admin_login_frame, borderwidth=5, show="*", width=30, font=("Helvetica", 12)

        )

        admin_password_entry.pack(pady=10)



        admin_show_password_var = tk.BooleanVar()

        admin_show_p
