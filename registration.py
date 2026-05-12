import tkinter as tk
from tkinter import ttk, messagebox as ms
import sqlite3
import re

# ======================= WINDOW =======================
window = tk.Tk()
window.title("User Registration")
window.geometry("900x650")
window.configure(bg="#0f172a")
window.resizable(True, True)

# ======================= VARIABLES =======================
Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.StringVar()
gender = tk.StringVar()
age = tk.StringVar()
password = tk.StringVar()
password1 = tk.StringVar()

# ======================= DATABASE =======================
conn = sqlite3.connect("evaluation.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS registration (
        Fullname TEXT,
        address TEXT,
        username TEXT,
        Email TEXT,
        Phoneno TEXT,
        Gender TEXT,
        age TEXT,
        password TEXT
    )
""")
conn.commit()
conn.close()

# ======================= PASSWORD CHECK =======================
def password_check(pwd):
    if len(pwd) < 6:
        return False
    if not re.search("[A-Z]", pwd):
        return False
    if not re.search("[a-z]", pwd):
        return False
    if not re.search("[0-9]", pwd):
        return False
    if not re.search("[@#$%]", pwd):
        return False
    return True

# ======================= REGISTER FUNCTION =======================
def register():
    if Fullname.get() == "" or Fullname.get().isdigit():
        ms.showerror("Error", "Enter valid full name")
        return

    if Email.get() == "" or not re.match(r"[^@]+@[^@]+\.[^@]+", Email.get()):
        ms.showerror("Error", "Enter valid email")
        return

    if not Phoneno.get().isdigit() or len(Phoneno.get()) != 10:
        ms.showerror("Error", "Enter valid 10-digit phone number")
        return

    if password.get() != password1.get():
        ms.showerror("Error", "Passwords do not match")
        return

    if not password_check(password.get()):
        ms.showerror(
            "Error",
            "Password must contain:\n• 1 Uppercase\n• 1 Lowercase\n• 1 Number\n• 1 Symbol (@#$%)"
        )
        return

    conn = sqlite3.connect("evaluation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration WHERE username=?", (username.get(),))
    if cursor.fetchone():
        ms.showerror("Error", "Username already exists")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO registration VALUES (?,?,?,?,?,?,?,?)",
        (
            Fullname.get(),
            address.get(),
            username.get(),
            Email.get(),
            Phoneno.get(),
            gender.get(),
            age.get(),
            password.get()
        )
    )
    conn.commit()
    conn.close()

    ms.showinfo("Success", "Registration Successful!")
    window.destroy()
    
    from subprocess import call
    call(["python", "login.py"])


# ======================= HEADER =======================
tk.Label(
    window,
    text="Create New Account",
    font=("Segoe UI", 30, "bold"),
    bg="#0f172a",
    fg="white"
).pack(pady=20)

tk.Label(
    window,
    text="Secure Aadhaar Verification System",
    font=("Segoe UI", 14),
    bg="#0f172a",
    fg="#cbd5f5"
).pack()

# ======================= CARD =======================
card = tk.Frame(window, bg="white", width=500, height=520)
card.pack(pady=30)
card.pack_propagate(False)

# ======================= INPUT FIELD FUNCTION =======================
def input_field(label, var, y):
    tk.Label(card, text=label, bg="white", font=("Segoe UI", 11)).place(x=40, y=y)
    ttk.Entry(card, textvariable=var).place(x=220, y=y+2, width=220)

# ======================= FORM =======================
input_field("Full Name", Fullname, 30)
input_field("Address", address, 70)
input_field("Email", Email, 110)
input_field("Phone Number", Phoneno, 150)

tk.Label(card, text="Gender", bg="white", font=("Segoe UI", 11)).place(x=40, y=190)
ttk.Radiobutton(card, text="Male", variable=gender, value="Male").place(x=220, y=190)
ttk.Radiobutton(card, text="Female", variable=gender, value="Female").place(x=300, y=190)

input_field("Age", age, 230)
input_field("Username", username, 270)

tk.Label(card, text="Password", bg="white", font=("Segoe UI", 11)).place(x=40, y=310)
ttk.Entry(card, textvariable=password, show="*").place(x=220, y=312, width=220)

tk.Label(card, text="Confirm Password", bg="white", font=("Segoe UI", 11)).place(x=40, y=350)
ttk.Entry(card, textvariable=password1, show="*").place(x=220, y=352, width=220)

# ======================= BUTTON =======================
btn = tk.Button(
    card,
    text="Register",
    bg="#22c55e",
    fg="white",
    font=("Segoe UI", 14, "bold"),
    relief="flat",
    cursor="hand2",
    command=register
)
btn.place(x=180, y=420, width=150)

# Hover Effect
btn.bind("<Enter>", lambda e: btn.config(bg="#16a34a"))
btn.bind("<Leave>", lambda e: btn.config(bg="#22c55e"))

# ======================= RUN =======================
window.mainloop()
