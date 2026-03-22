import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder

# -------------------------------
# Create outputs folder
# -------------------------------
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("data/maternal_health.csv")

# -------------------------------
# Feature Engineering (MUST MATCH MODEL)
# -------------------------------
df["PulsePressure"] = df["SystolicBP"] - df["DiastolicBP"]
df["MAP"] = (df["SystolicBP"] + 2 * df["DiastolicBP"]) / 3
df["BP_Ratio"] = df["SystolicBP"] / df["DiastolicBP"]

# -------------------------------
# Encode target
# -------------------------------
label_encoder = LabelEncoder()
df["RiskLevel"] = label_encoder.fit_transform(df["RiskLevel"])

# -------------------------------
# Split data
# -------------------------------
X = df.drop("RiskLevel", axis=1)
y = df["RiskLevel"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# Load trained model & scaler
# -------------------------------
model = joblib.load("models/model.pkl")
scaler = joblib.load("models/scaler.pkl")

# -------------------------------
# Scale + Predict
# -------------------------------
X_test_scaled = scaler.transform(X_test)
y_pred = model.predict(X_test_scaled)

# -------------------------------
# 1. Correlation Heatmap
# -------------------------------
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("outputs/heatmap.png", dpi=300)
plt.close()

# -------------------------------
# 2. Class Distribution
# -------------------------------
plt.figure(figsize=(6,4))
sns.countplot(x=y, palette="viridis")
plt.title("Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/class_distribution.png", dpi=300)
plt.close()

# -------------------------------
# 3. Feature Distribution
# -------------------------------
df.hist(figsize=(12,10), bins=20)
plt.suptitle("Feature Distributions", fontsize=16)
plt.tight_layout()
plt.savefig("outputs/feature_distribution.png", dpi=300)
plt.close()

# -------------------------------
# 4. Confusion Matrix
# -------------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=label_encoder.classes_,
    yticklabels=label_encoder.classes_
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("outputs/confusion_matrix.png", dpi=300)
plt.close()

print("✅ All visualizations saved in 'outputs/' folder")