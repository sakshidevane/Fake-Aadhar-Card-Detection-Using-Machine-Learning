import tkinter as tk
from PIL import Image, ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
import CNNModel

global fn
fn=""

# ================= WINDOW =================
root = tk.Tk()
root.title("Fake/Real Aadhaar Card Detection")
root.state("zoomed")
root.configure(bg="#0A0A0A")  # Dark theme

# ================= HEADER =================
header = tk.Frame(root, bg="#B71C1C", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="🛡️ FAKE / REAL AADHAAR CARD DETECTION SYSTEM",
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

tk.Label(control_panel, text="CONTROL PANEL",
         font=("Segoe UI", 18, "bold"),
         bg="#111111", fg="#00E5FF").pack(pady=25)

def side_btn(text, cmd, color="#B71C1C"):
    return tk.Button(
        control_panel, text=text, command=cmd,
        font=("Segoe UI", 14, "bold"),
        bg=color, fg="white",
        relief="flat", height=2, width=18
    )

# ================= CENTER IMAGE DISPLAY =================
display_frame = tk.Frame(main_frame, bg="#0A0A0A")
display_frame.pack(side="left", expand=True, fill="both")

def image_card(title):
    frame = tk.Frame(display_frame, bg="#151A30", width=300, height=360)
    frame.pack(side="left", padx=20)
    frame.pack_propagate(False)

    tk.Label(frame, text=title,
             font=("Segoe UI", 14, "bold"),
             bg="#151A30", fg="#00E5FF").pack(pady=10)

    lbl = tk.Label(frame, bg="white")
    lbl.pack(expand=True, fill="both", padx=10, pady=10)

    return lbl

# Panels for images
img_original = image_card("ORIGINAL IMAGE")
img_gray = image_card("GRAY IMAGE")
img_binary = image_card("BINARY IMAGE")

# ================= PREDICTION RESULT ROW =================
result_frame = tk.Frame(root, bg="#111111", height=180)
result_frame.pack(fill="x", padx=20, pady=20)
result_frame.pack_propagate(False)

result_label = tk.Label(result_frame, text="NO IMAGE",
                        font=("Segoe UI", 28, "bold"),
                        bg="#000000", fg="white",
                        width=40, height=4)
result_label.pack(pady=20)

# ================= IMAGE SHOW FUNCTION =================
def show_image(lbl, pil_img):
    pil_img = pil_img.resize((260, 260))
    imgtk = ImageTk.PhotoImage(pil_img)
    lbl.config(image=imgtk)
    lbl.image = imgtk   # Prevent garbage collection

# ================= CORE FUNCTIONS =================
def update_label(str_T):
    result_label.config(text=str_T)

def openimage():
    global fn
    fn = askopenfilename(title='Select Aadhaar Image',
                         filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if fn:
        img = Image.open(fn)
        show_image(img_original, img)
        update_label("Image Loaded")

def convert_grey():
    if not fn:
        update_label("No image selected")
        return
    img = cv2.imread(fn)
    img = cv2.resize(img, (260, 260))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    show_image(img_gray, Image.fromarray(gray))
    show_image(img_binary, Image.fromarray(thresh))
    update_label("Preprocessing Done")

def train_model():
    update_label("Model Training Start...")
    start = time.time()
    CNNModel.main()  # Your CNN training function
    end = time.time()
    update_label(f"Model Training Completed in {end-start:.2f} sec")

def test_model_proc(fn):
    IMAGE_SIZE = 100
    model = load_model('fakeaadhar_model.h5')
    img = Image.open(fn)
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    img = np.array(img)
    img = img.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3).astype('float32') / 255.0
    prediction = model.predict(img)
    class_idx = np.argmax(prediction)
    return "Fake Aadhaar (CNN Algorithm)" if class_idx == 0 else "Real Aadhaar (CNN Algorithm)"

def test_model():
    if not fn:
        update_label("Please Select Image First")
        return
    update_label("Prediction Running...")
    start = time.time()
    result = test_model_proc(fn)
    end = time.time()
    update_label(f"{result}\nExecution Time: {end-start:.2f} sec")

# ================= CONTROL PANEL BUTTONS =================
side_btn("SELECT IMAGE", openimage).pack(pady=15)
side_btn("IMAGE PREPROCESS", convert_grey).pack(pady=15)
#side_btn("TRAIN MODEL", train_model, "#2E7D32").pack(pady=15)
side_btn("CNN DETECTION", test_model, "#6A1B9A").pack(pady=15)
side_btn("EXIT", root.destroy, "#C62828").pack(side="bottom", pady=15)

# ================= FOOTER =================
footer = tk.Label(root,
                  text="Deep Learning Based Fake/Real Aadhaar Detection | CNN Model",
                  bg="#000814",
                  fg="#90CAF9",
                  font=("Segoe UI", 10),
                  height=2)
footer.pack(fill="x")

root.mainloop()
