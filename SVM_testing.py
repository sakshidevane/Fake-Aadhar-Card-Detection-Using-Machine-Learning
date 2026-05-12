import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np
import joblib

# ================= GLOBAL =================
fn = ""

# ================= LOAD MODEL =================
svm_model = joblib.load("aadhaar_svm_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# ================= WINDOW =================
root = tk.Tk()
root.title("Fake / Real Aadhaar Card Detection (SVM)")
root.state("zoomed")
root.configure(bg="#0A0A0A")

# ================= HEADER =================
header = tk.Frame(root, bg="#B71C1C", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="🛡️ FAKE / REAL AADHAAR CARD DETECTION SYSTEM (SVM)",
    font=("Segoe UI", 26, "bold"),
    bg="#B71C1C",
    fg="white"
).pack(pady=15)

# ================= MAIN CONTAINER =================
main_frame = tk.Frame(root, bg="#0A0A0A")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ================= LEFT CONTROL PANEL =================
control_panel = tk.Frame(main_frame, bg="#111111", width=260)
control_panel.pack(side="left", fill="y", padx=15)
control_panel.pack_propagate(False)

tk.Label(
    control_panel,
    text="CONTROL PANEL",
    font=("Segoe UI", 18, "bold"),
    bg="#111111",
    fg="#00E5FF"
).pack(pady=25)

def side_btn(text, cmd, color="#B71C1C"):
    return tk.Button(
        control_panel,
        text=text,
        command=cmd,
        font=("Segoe UI", 14, "bold"),
        bg=color,
        fg="white",
        relief="flat",
        height=2,
        width=18
    )

# ================= CENTER IMAGE DISPLAY =================
display_frame = tk.Frame(main_frame, bg="#0A0A0A")
display_frame.pack(side="left", expand=True, fill="both")

def image_card(title):
    frame = tk.Frame(display_frame, bg="#151A30", width=300, height=360)
    frame.pack(side="left", padx=20)
    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 14, "bold"),
        bg="#151A30",
        fg="#00E5FF"
    ).pack(pady=10)

    lbl = tk.Label(frame, bg="white")
    lbl.pack(expand=True, fill="both", padx=10, pady=10)

    return lbl

img_original = image_card("ORIGINAL IMAGE")
img_gray = image_card("GRAY IMAGE")
img_binary = image_card("BINARY IMAGE")

# ================= RESULT PANEL =================
result_frame = tk.Frame(root, bg="#111111", height=180)
result_frame.pack(fill="x", padx=20, pady=20)
result_frame.pack_propagate(False)

result_label = tk.Label(
    result_frame,
    text="NO IMAGE",
    font=("Segoe UI", 28, "bold"),
    bg="#000000",
    fg="white",
    width=40,
    height=4
)
result_label.pack(pady=20)

# ================= IMAGE SHOW FUNCTION =================
def show_image(lbl, img):
    img = img.resize((260, 260))
    imgtk = ImageTk.PhotoImage(img)
    lbl.config(image=imgtk)
    lbl.image = imgtk

# ================= FUNCTIONS =================
def upload_image():
    global fn
    fn = askopenfilename(
        title="Select Aadhaar Image",
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )
    if fn:
        img = Image.open(fn)
        show_image(img_original, img)
        result_label.config(text="IMAGE LOADED", fg="#FFEB3B")

def preprocess():
    if not fn:
        result_label.config(text="NO IMAGE SELECTED", fg="red")
        return

    img = cv2.imread(fn)
    img = cv2.resize(img, (260, 260))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    show_image(img_gray, Image.fromarray(gray))
    show_image(img_binary, Image.fromarray(thresh))
    result_label.config(text="PREPROCESSING DONE", fg="#00E5FF")

def detect():
    if not fn:
        result_label.config(text="NO IMAGE", fg="red")
        return

    img = cv2.imread(fn)
    img = cv2.resize(img, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.flatten().reshape(1, -1)

    pred = svm_model.predict(img)
    result = label_encoder.inverse_transform(pred)[0]

    if str(result).lower() == "0":
        result_label.config(
            text="FAKE AADHAAR\nSVM ALGORITHM",
            fg="#FF1744",
            bg="#2A0000"
        )
    else:
        result_label.config(
            text="REAL AADHAAR\nSVM ALGORITHM",
            fg="#00E676",
            bg="#002A12"
        )

# ================= BUTTONS =================
side_btn("SELECT IMAGE", upload_image).pack(pady=15)
side_btn("IMAGE PREPROCESS", preprocess).pack(pady=15)
side_btn("SVM DETECTION", detect, "#6A1B9A").pack(pady=15)
side_btn("EXIT", root.destroy, "#C62828").pack(side="bottom", pady=15)

# ================= FOOTER =================
footer = tk.Label(
    root,
    text="Machine Learning Based Fake/Real Aadhaar Detection | SVM Model",
    bg="#000814",
    fg="#90CAF9",
    font=("Segoe UI", 10),
    height=2
)
footer.pack(fill="x")

root.mainloop()
