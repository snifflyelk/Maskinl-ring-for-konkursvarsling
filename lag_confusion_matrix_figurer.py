import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patheffects as path_effects
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier


def load_data():
    df = pd.read_csv("feature_engineered_enheter.csv")
    df["fylke"] = df["postadresse.kommunenummer"].astype(str).str[:2]

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
    cat_cols = ["bransje_2siffer", "fylke"]

    for col in num_cols + bin_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in cat_cols:
        df[col] = df[col].astype(str)

    X = df[num_cols + bin_cols + cat_cols]
    y = df["konkurs_bin"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        stratify=y,
        random_state=42,
    )

    for col in cat_cols:
        X_train[col] = X_train[col].fillna("MISSING").astype(str)
        X_test[col] = X_test[col].fillna("MISSING").astype(str)

    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)

    return X_train, X_test, y_train, y_test, num_cols, bin_cols, cat_cols


def train_logistic(X_train, y_train, num_cols, bin_cols, cat_cols):
    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols + bin_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocess),
            (
                "logreg",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=2000,
                    solver="liblinear",
                    random_state=42,
                ),
            ),
        ]
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train, num_cols, bin_cols, cat_cols):
    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols + bin_cols),
            (
                "cat",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                cat_cols,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocess),
            (
                "xgb",
                XGBClassifier(
                    n_estimators=300,
                    learning_rate=0.05,
                    max_depth=6,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    objective="binary:logistic",
                    eval_metric="auc",
                    scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    model.fit(X_train, y_train)
    return model


def plot_confusion_matrices(y_test, logistic_probs, xgb_probs, threshold, output_path):
    logistic_pred = (logistic_probs >= threshold).astype(int)
    xgb_pred = (xgb_probs >= threshold).astype(int)

    logistic_cm = confusion_matrix(y_test, logistic_pred)
    xgb_cm = confusion_matrix(y_test, xgb_pred)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    matrices = [
        (logistic_cm, f"Logistic regression (threshold={threshold:.2f})"),
        (xgb_cm, f"XGBoost (threshold={threshold:.2f})"),
    ]

    for ax, (cm, title) in zip(axes, matrices):
        im = ax.imshow(cm, interpolation="nearest", cmap="viridis")
        ax.set_title(title)
        ax.set_xlabel("Predicted label")
        ax.set_ylabel("True label")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                text = ax.text(
                    j,
                    i,
                    f"{cm[i, j]}",
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=11,
                    fontweight="bold",
                )
                text.set_path_effects(
                    [path_effects.withStroke(linewidth=2.5, foreground="black")]
                )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    os.makedirs("figurer_modell", exist_ok=True)

    X_train, X_test, y_train, y_test, num_cols, bin_cols, cat_cols = load_data()

    logistic_model = train_logistic(X_train, y_train, num_cols, bin_cols, cat_cols)
    xgb_model = train_xgboost(X_train, y_train, num_cols, bin_cols, cat_cols)

    logistic_probs = logistic_model.predict_proba(X_test)[:, 1]
    xgb_probs = xgb_model.predict_proba(X_test)[:, 1]

    threshold_files = {
        0.20: "figurer_modell/confusion_matrix_threshold_0_20.png",
        0.50: "figurer_modell/confusion_matrix_threshold_0_50.png",
        0.44: "figurer_modell/confusion_matrix_threshold_0_44.png",
    }

    for threshold, output_path in threshold_files.items():
        plot_confusion_matrices(y_test, logistic_probs, xgb_probs, threshold, output_path)
        print(f"Lagret: {output_path}")


if __name__ == "__main__":
    main()