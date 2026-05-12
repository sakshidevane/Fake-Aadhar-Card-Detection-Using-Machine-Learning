import os
import cv2
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# -----------------------------------
# CONFIGURATION
# -----------------------------------
IMG_SIZE = 100
TRAIN_DIR = "training_set"
TEST_DIR = "testing_set"
MODEL_PATH = "aadhaar_svm_model.pkl"

# -----------------------------------
# LOAD IMAGES FUNCTION
# -----------------------------------
def load_data(folder):
    data = []
    labels = []

    for label in os.listdir(folder):
        label_path = os.path.join(folder, label)

        for img_name in os.listdir(label_path):
            img_path = os.path.join(label_path, img_name)

            img = cv2.imread(img_path)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            data.append(img.flatten())
            labels.append(label)

    return np.array(data), np.array(labels)

# -----------------------------------
# LOAD TRAIN & TEST DATA
# -----------------------------------
X_train, y_train = load_data(TRAIN_DIR)
X_test, y_test = load_data(TEST_DIR)

# -----------------------------------
# LABEL ENCODING
# -----------------------------------
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
y_test = encoder.transform(y_test)

# -----------------------------------
# TRAIN SVM MODEL
# -----------------------------------
svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(X_train, y_train)

# -----------------------------------
# SAVE MODEL
# -----------------------------------
joblib.dump(svm_model, MODEL_PATH)
joblib.dump(encoder, "label_encoder.pkl")

print("Model saved as:", MODEL_PATH)

# -----------------------------------
# LOAD MODEL (FOR TESTING)
# -----------------------------------
svm_loaded = joblib.load(MODEL_PATH)
encoder_loaded = joblib.load("label_encoder.pkl")

# -----------------------------------
# PREDICTION
# -----------------------------------
y_pred = svm_loaded.predict(X_test)

# -----------------------------------
# EVALUATION
# -----------------------------------
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=encoder_loaded.classes_))

# -----------------------------------
# CONFUSION MATRIX
# -----------------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=encoder_loaded.classes_,
            yticklabels=encoder_loaded.classes_)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Aadhaar Real vs Fake")
plt.show()
