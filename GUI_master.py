import tkinter as tk
from PIL import Image, ImageTk
from subprocess import call

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Fake & Real Aadhaar Card Detection")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.configure(bg="#0f172a")

# ================= BACKGROUND IMAGE =================
try:
    bg = Image.open("img3.jpeg")
    bg = bg.resize((w, h), Image.Resampling.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

# ================= OVERLAY =================
overlay = tk.Frame(root, bg="#0f172a")
overlay.place(x=0, y=0, relwidth=1, relheight=1)
overlay.attributes = lambda *args: None

# ================= HEADER =================
header = tk.Frame(root, bg="#020617", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="Fake & Real Aadhaar Card Detection",
    font=("Segoe UI", 28, "bold"),
    bg="#020617",
    fg="white"
).pack(pady=20)

# ================= BUTTON FUNCTIONS =================
def svm_testing():
    call(["python", "SVM_testing.py"])

def cnn_testing():
    call(["python", "CNN_testing.py"])

def exit_app():
    root.destroy()

# ================= MAIN DASHBOARD =================
dashboard = tk.Frame(root, bg="#0f172a")
dashboard.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    dashboard,
    text="Select Detection Method",
    font=("Segoe UI", 22, "bold"),
    bg="#0f172a",
    fg="white"
).pack(pady=20)

# ================= CARD BUTTON STYLE =================
def card_button(parent, text, cmd):
    btn = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 16, "bold"),
        bg="#22c55e",
        fg="white",
        relief="flat",
        cursor="hand2",
        width=25,
        height=2,
        command=cmd
    )
    btn.pack(pady=15)

    btn.bind("<Enter>", lambda e: btn.config(bg="#16a34a"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#22c55e"))

# ================= BUTTONS =================
card_button(dashboard, "🔍 SVM Testing", svm_testing)
card_button(dashboard, "🤖 CNN Testing", cnn_testing)

exit_btn = tk.Button(
    dashboard,
    text="Exit",
    font=("Segoe UI", 14, "bold"),
    bg="#ef4444",
    fg="white",
    relief="flat",
    cursor="hand2",
    width=18,
    height=1,
    command=exit_app
)
exit_btn.pack(pady=30)

exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#dc2626"))
exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#ef4444"))

# ================= FOOTER =================
footer = tk.Frame(root, bg="#020617", height=50)
footer.pack(side="bottom", fill="x")

tk.Label(
    footer,
    text="© Fake Aadhaar Card Detection System",
    font=("Segoe UI", 11),
    bg="#020617",
    fg="#94a3b8"
).pack(pady=10)

# ================= RUN =================
root.mainloop()
