import pandas as pd
import numpy as np
import joblib
from datetime import datetime

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

# -------------------------------
# 1. Load Data
# -------------------------------
df = pd.read_csv("data/maternal_health.csv")


# -------------------------------
# Feature Engineering
# -------------------------------

# Pulse Pressure
df["PulsePressure"] = df["SystolicBP"] - df["DiastolicBP"]

# Mean Arterial Pressure
df["MAP"] = (df["SystolicBP"] + 2 * df["DiastolicBP"]) / 3

# BP Ratio
df["BP_Ratio"] = df["SystolicBP"] / df["DiastolicBP"]


# -------------------------------
# 2. Encode Target
# -------------------------------
le = LabelEncoder()
df['RiskLevel'] = le.fit_transform(df['RiskLevel'])

X = df.drop('RiskLevel', axis=1)
y = df['RiskLevel']

# -------------------------------
# 3. Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# -------------------------------
# 4. Scaling
# -------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------
# 5. Model (Optimized XGBoost)
# -------------------------------

model = XGBClassifier(
    n_estimators=450,
    learning_rate=0.04,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric='mlogloss',
    random_state=42
)

# -------------------------------
# 6. Pipeline (NO LEAKAGE)
# -------------------------------
pipeline = Pipeline([
    #('smote', SMOTE(random_state=42)),
    ('model', model)
])

# -------------------------------
# 7. Cross Validation
# -------------------------------
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(
    pipeline,
    X_train_scaled,
    y_train,
    cv=skf,
    scoring='f1_macro'
)

print("CV F1 (Macro):", scores.mean())


# -------------------------------
# 8. Train Final Model
# -------------------------------
pipeline.fit(X_train_scaled, y_train)

# -------------------------------
# 9. Evaluation
# -------------------------------
y_pred = pipeline.predict(X_test_scaled)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------------
# 10. Save Model + Scaler + Encoder
# -------------------------------
joblib.dump(pipeline, "models/model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(le, "models/label_encoder.pkl")

print("\nModel saved successfully!")
