import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ---------------------------------------------------------
# 1. LAST DATASETT
# ---------------------------------------------------------
df = pd.read_csv("feature_engineered_enheter.csv")


# ---------------------------------------------------------
# 2. LAG FYLKE
# ---------------------------------------------------------
df["fylke"] = df["postadresse.kommunenummer"].astype(str).str[:2]


# ---------------------------------------------------------
# 3. DEFINER VARIABLER
# ---------------------------------------------------------
num_cols = [
    "alder_aar",
    "antallAnsatte",
    "kapital.belop",
    "kapital.innbetalt",
    "kapital.fulltInnbetalt",
    "kapital.bundet",
]

bin_cols = [
    "revisjonsfravalg",
    "mva_registrert",
    "underAvvikling_bin",
    "underTvangsavviklingEllerTvangsopplosning_bin",
]

cat_cols = [
    "bransje_2siffer",
    "fylke",
]


# ---------------------------------------------------------
# 4. TVING NUMERISKE KOLONNER TIL NUMBER
# ---------------------------------------------------------
for col in num_cols + bin_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ---------------------------------------------------------
# 5. TVING KATEGORIER TIL STRING
# ---------------------------------------------------------
for col in cat_cols:
    df[col] = df[col].astype(str)


# ---------------------------------------------------------
# 6. DEFINER X OG y
# ---------------------------------------------------------
X = df[num_cols + bin_cols + cat_cols]
y = df["konkurs_bin"].astype(int)


# ---------------------------------------------------------
# 7. SPLITT DATA
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    stratify=y,
    random_state=42,
)

print("Train:", y_train.value_counts())
print("Test:", y_test.value_counts())


# ---------------------------------------------------------
# 8. RENS KATEGORIKOLONNER
# ---------------------------------------------------------
for col in cat_cols:
    X_train[col] = X_train[col].fillna("MISSING").astype(str)
    X_test[col] = X_test[col].fillna("MISSING").astype(str)


# ---------------------------------------------------------
# 9. FYLL MANGLENDE VERDIER
# ---------------------------------------------------------
X_train = X_train.fillna(0)
X_test = X_test.fillna(0)


# ---------------------------------------------------------
# 10. PREPROSESSERING
# ---------------------------------------------------------
preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols + bin_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ]
)


# ---------------------------------------------------------
# 11. LOGISTISK MODELL
# ---------------------------------------------------------
logreg_model = LogisticRegression(
    class_weight="balanced",
    max_iter=2000,
    solver="liblinear",
    random_state=42,
)

model = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("logreg", logreg_model),
    ]
)


# ---------------------------------------------------------
# 12. TREN MODELLEN
# ---------------------------------------------------------
model.fit(X_train, y_train)


# ---------------------------------------------------------
# 13. EVALUERING (STANDARD 0.5-TERSKEL)
# ---------------------------------------------------------
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred_default = (y_pred_proba >= 0.5).astype(int)

auc = roc_auc_score(y_test, y_pred_proba)
print("AUC-score:", auc)

print("\nConfusion matrix (terskel 0.5):")
print(confusion_matrix(y_test, y_pred_default))

print("\nClassification report (terskel 0.5):")
print(classification_report(y_test, y_pred_default))


# ---------------------------------------------------------
# 14. AUTOMATISK TERSKEL-ANALYSE
# ---------------------------------------------------------
thresholds = np.arange(0.01, 0.51, 0.01)
results = []

for t in thresholds:
    y_pred_t = (y_pred_proba >= t).astype(int)
    cm = confusion_matrix(y_test, y_pred_t)
    tn, fp, fn, tp = cm.ravel()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    youden_j = recall - (fp / (fp + tn))

    results.append([t, precision, recall, f1, accuracy, youden_j])

results_df = pd.DataFrame(
    results,
    columns=["threshold", "precision", "recall", "f1", "accuracy", "youden_j"],
)

print("\n--- Terskelanalyse (0.01 til 0.50) ---")
print(results_df)

best_f1 = results_df.loc[results_df["f1"].idxmax()]
best_recall = results_df.loc[results_df["recall"].idxmax()]
best_youden = results_df.loc[results_df["youden_j"].idxmax()]

print("\nBeste terskel etter F1-score:")
print(best_f1)

print("\nBeste terskel etter recall:")
print(best_recall)

print("\nBeste terskel etter Youden's J:")
print(best_youden)


# ---------------------------------------------------------
# 15. PLOTT AV TERSKEL-EFFEKTER
# ---------------------------------------------------------
os.makedirs("figurer_modell", exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(results_df["threshold"], results_df["recall"], label="Recall", color="blue")
plt.plot(results_df["threshold"], results_df["precision"], label="Precision", color="green")
plt.plot(results_df["threshold"], results_df["f1"], label="F1-score", color="red")
plt.xlabel("Terskel")
plt.ylabel("Score")
plt.title("Effekt av terskelvalg pa Recall, Precision og F1 (logistisk)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figurer_modell/terskelanalyse_logistisk.png", dpi=300)
plt.show()


# ---------------------------------------------------------
# 16. ROC-KURVE
# ---------------------------------------------------------
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC-kurve for logistisk regresjon")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figurer_modell/ROC-kurve_logistisk.png", dpi=300)
plt.show()