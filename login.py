import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
import sqlite3

# ======================= MAIN WINDOW =======================
root = tk.Tk()
root.title("Fake vs Real Aadhaar Detection - Login")
root.geometry("900x600")
root.configure(bg="#0f172a")
root.resizable(True, True)

username = tk.StringVar()
password = tk.StringVar()

# ======================= DATABASE =======================
def login():
    with sqlite3.connect("evaluation.db") as db:
        cursor = db.cursor()
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
        db.commit()

        cursor.execute(
            "SELECT * FROM registration WHERE username=? AND password=?",
            (username.get(), password.get())
        )
        result = cursor.fetchone()

        if result:
            ms.showinfo("Success", "Login Successful!")
            root.destroy()
            
            from subprocess import call
            call(['python','GUI_master.py'])
            
        else:
            ms.showerror("Error", "Invalid Username or Password")

# ======================= HEADER =======================
tk.Label(
    root,
    text="Fake vs Real Aadhaar Detection",
    font=("Segoe UI", 30, "bold"),
    bg="#0f172a",
    fg="white"
).pack(pady=25)

tk.Label(
    root,
    text="Secure Identity Verification System",
    font=("Segoe UI", 14),
    bg="#0f172a",
    fg="#cbd5f5"
).pack()

# ======================= MAIN FRAME =======================
main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack(expand=True)

# ======================= LEFT PANEL =======================
left_panel = tk.Frame(main_frame, bg="#020617", width=300, height=360)
left_panel.grid(row=0, column=0, padx=20)
left_panel.pack_propagate(False)

tk.Label(
    left_panel,
    text="🔐 Smart Authentication",
    font=("Segoe UI", 18, "bold"),
    bg="#020617",
    fg="#22c55e"
).pack(pady=25)

features = [
    "✔ Fake Aadhaar Detection",
    "✔ Secure Login System",
    "✔ AI Based Verification",
    "✔ Real-time Results"
]

for f in features:
    tk.Label(
        left_panel,
        text=f,
        font=("Segoe UI", 12),
        bg="#020617",
        fg="white",
        anchor="w"
    ).pack(fill="x", padx=25, pady=8)

# ======================= LOGIN CARD =======================
card = tk.Frame(main_frame, bg="white", width=380, height=360)
card.grid(row=0, column=1, padx=20)
card.pack_propagate(False)

tk.Label(
    card,
    text="Welcome Back 👋",
    font=("Segoe UI", 20, "bold"),
    bg="white",
    fg="#1e293b"
).pack(pady=20)

tk.Label(
    card,
    text="Login to your account",
    font=("Segoe UI", 12),
    bg="white",
    fg="#64748b"
).pack()

def registration():
    from subprocess import call
    call(["python","registration.py"])
    root.destroy()
    
# ======================= INPUT FIELDS =======================
def input_field(parent, label, var, show=None):
    tk.Label(
        parent,
        text=label,
        font=("Segoe UI", 11),
        bg="white",
        fg="#1e293b",
        anchor="w"
    ).pack(fill="x", padx=30, pady=(15, 5))

    entry = ttk.Entry(parent, textvariable=var, show=show)
    entry.pack(padx=30, fill="x")
    return entry

input_field(card, "👤 Username", username)
input_field(card, "🔒 Password", password, show="*")

# ======================= BUTTONS =======================
login_btn = tk.Button(
    card,
    text="Login",
    font=("Segoe UI", 13, "bold"),
    bg="#22c55e",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=login
)
login_btn.pack(pady=25, ipadx=60)

# Hover effect
login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#16a34a"))
login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#22c55e"))

register_btn = tk.Button(
    card,
    text="Create New Account",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#2563eb",
    relief="flat",
    cursor="hand2",
    command=registration
)
register_btn.pack()

# ======================= FOOTER =======================
tk.Label(
    card,
    text="© Aadhaar Verification System",
    font=("Segoe UI", 9),
    fg="#64748b",
    bg="white"
).pack(side="bottom", pady=12)

# ======================= RUN =======================
root.mainloop()
