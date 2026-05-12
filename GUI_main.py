import tkinter as tk
from PIL import Image, ImageTk
from subprocess import call

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Fake Aadhaar Card Detection")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.configure(bg="#0f172a")

# ================= BACKGROUND IMAGE =================
try:
    bg = Image.open("1.jpg")
    bg = bg.resize((w, h), Image.Resampling.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

# ================= OVERLAY =================
overlay = tk.Frame(root, bg="#0f172a")
overlay.place(x=0, y=0, relwidth=1, relheight=1)
overlay.configure(bg="#0f172a")
overlay.attributes = lambda *args: None  # prevents error

# ================= HEADER =================
header = tk.Frame(root, bg="#020617", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="Fake Aadhaar Card Detection",
    font=("Segoe UI", 28, "bold"),
    bg="#020617",
    fg="white"
).pack(side="left", padx=40)

# ================= BUTTON FUNCTIONS =================
def open_login():
    call(["python", "login.py"])

def open_register():
    call(["python", "registration.py"])

# ================= HEADER BUTTONS =================
def nav_button(text, cmd):
    btn = tk.Button(
        header,
        text=text,
        font=("Segoe UI", 13, "bold"),
        bg="#22c55e",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=cmd
    )
    btn.pack(side="right", padx=15, pady=20)

    btn.bind("<Enter>", lambda e: btn.config(bg="#16a34a"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#22c55e"))
    return btn

nav_button("Register", open_register)
nav_button("Login", open_login)

# ================= HERO SECTION =================
hero = tk.Frame(root, bg="#0f172a")
hero.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    hero,
    text="AI Powered Aadhaar Verification",
    font=("Segoe UI", 42, "bold"),
    bg="#0f172a",
    fg="white"
).pack(pady=10)

tk.Label(
    hero,
    text="Detect Fake & Real Aadhaar Cards using Advanced Machine Learning",
    font=("Segoe UI", 16),
    bg="#0f172a",
    fg="#cbd5f5"
).pack(pady=10)

# ================= CTA BUTTON =================
cta = tk.Button(
    hero,
    text="Get Started",
    font=("Segoe UI", 16, "bold"),
    bg="#22c55e",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=open_login
)
cta.pack(pady=30, ipadx=40, ipady=10)

cta.bind("<Enter>", lambda e: cta.config(bg="#16a34a"))
cta.bind("<Leave>", lambda e: cta.config(bg="#22c55e"))

# ================= FEATURE CARDS =================
features = tk.Frame(root, bg="#0f172a")
features.place(relx=0.5, rely=0.75, anchor="center")

feature_list = [
    "🔍 Fake Aadhaar Detection",
    "🤖 AI & ML Based System",
    "🔐 Secure Login & Registration",
    "⚡ Fast & Accurate Results"
]

for f in feature_list:
    card = tk.Label(
        features,
        text=f,
        font=("Segoe UI", 14, "bold"),
        bg="#020617",
        fg="white",
        padx=20,
        pady=15
    )
    card.pack(side="left", padx=10)

# ================= FOOTER =================
footer = tk.Frame(root, bg="#020617", height=50)
footer.pack(side="bottom", fill="x")

tk.Label(
    footer,
    text="© 2025 Fake Aadhaar Card Detection System",
    font=("Segoe UI", 11),
    bg="#020617",
    fg="#94a3b8"
).pack(pady=10)

# ================= RUN =================
root.mainloop()
