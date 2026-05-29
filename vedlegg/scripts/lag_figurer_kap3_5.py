import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    auc,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier


DATA_PATH = Path("feature_engineered_enheter.csv")
OUT_DIR = Path("figurer_kap3_5")

NUM_COLS = [
    "alder_aar",
    "antallAnsatte",
    "kapital.belop",
    "kapital.innbetalt",
    "kapital.fulltInnbetalt",
    "kapital.bundet",
]

BIN_COLS = [
    "revisjonsfravalg",
    "mva_registrert",
    "underAvvikling_bin",
    "underTvangsavviklingEllerTvangsopplosning_bin",
]

CAT_COLS = ["bransje_2siffer", "fylke"]
ALL_FEATURES = NUM_COLS + BIN_COLS + CAT_COLS


def ensure_output_dirs() -> None:
    for chapter in ["kap3_metode", "kap4_eda", "kap5_resultater"]:
        (OUT_DIR / chapter).mkdir(parents=True, exist_ok=True)


def load_and_prepare_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["fylke"] = df["postadresse.kommunenummer"].astype(str).str[:2]

    for col in NUM_COLS + BIN_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in CAT_COLS:
        df[col] = df[col].astype(str)

    return df


def make_chapter3_figures(df: pd.DataFrame) -> None:
    cap3 = OUT_DIR / "kap3_metode"

    # 3.1 Analysis pipeline
    fig, ax = plt.subplots(figsize=(15, 2.8))
    ax.axis("off")

    boxes = [
        {"x": 0.02, "w": 0.19, "txt": "Data\nfeature_engineered_enheter.csv"},
        {"x": 0.24, "w": 0.16, "txt": "Feature\nengineering + split"},
        {"x": 0.44, "w": 0.13, "txt": "Models\nLogReg + XGBoost"},
        {"x": 0.63, "w": 0.13, "txt": "Evaluation\nROC, PR, AUC, CM"},
        {"x": 0.85, "w": 0.07, "txt": "Threshold\nanalysis"},
    ]

    for b in boxes:
        ax.text(
            b["x"] + b["w"] / 2,
            0.5,
            b["txt"],
            ha="center",
            va="center",
            fontsize=13,
            bbox={"boxstyle": "round,pad=0.42", "fc": "#e8f1fb", "ec": "#2b6cb0"},
            transform=ax.transAxes,
        )

    for i in range(len(boxes) - 1):
        x1 = boxes[i]["x"] + boxes[i]["w"]
        x2 = boxes[i + 1]["x"]
        ax.annotate(
            "",
            xy=(x2, 0.5),
            xytext=(x1, 0.5),
            xycoords=ax.transAxes,
            arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#2b6cb0"},
        )

    plt.title("Figure 3.1 - Analysis pipeline", fontsize=17, pad=6)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.12)
    plt.tight_layout(pad=0.2)
    plt.savefig(cap3 / "figur_3_1_analysepipeline.png", dpi=300)
    plt.close()

    # 3.2 Variable overview by group
    group_names = [
        "Numeric\nfeatures",
        "Binary\nfeatures",
        "Categorical\nfeatures",
        "Total\nmodel inputs",
    ]
    group_counts = [len(NUM_COLS), len(BIN_COLS), len(CAT_COLS), len(ALL_FEATURES)]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(group_names, group_counts, color=["#2b6cb0", "#2f855a", "#d69e2e", "#4a5568"])
    ax.set_ylabel("Count")
    ax.set_title("Figure 3.2 - Variable overview used in models")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.1, f"{int(b.get_height())}", ha="center")
    plt.tight_layout()
    plt.savefig(cap3 / "figur_3_2_variabeloversikt.png", dpi=300)
    plt.close()

    # 3.3 Class imbalance
    y_counts = df["konkurs_bin"].astype(int).value_counts().sort_index()
    labels = ["No bankruptcy (0)", "Bankruptcy (1)"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, y_counts.values, color=["#718096", "#c53030"])
    ax.set_ylabel("Count")
    ax.set_title("Figure 3.3 - Class imbalance in target variable")
    total = y_counts.sum()
    for i, b in enumerate(bars):
        pct = 100 * y_counts.values[i] / total
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.01 * total, f"{pct:.2f}%", ha="center")
    plt.tight_layout()
    plt.savefig(cap3 / "figur_3_3_klasseubalanse.png", dpi=300)
    plt.close()


def make_chapter4_figures(df: pd.DataFrame) -> None:
    cap4 = OUT_DIR / "kap4_eda"

    # 4.1 Age distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    age = df["alder_aar"].dropna()
    ax.hist(age, bins=40, color="#2b6cb0", edgecolor="white")
    ax.set_title("Figure 4.1 - Distribution of firm age")
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig(cap4 / "figur_4_1_fordeling_alder.png", dpi=300)
    plt.close()

    # 4.2 Employee distribution (log-scale y)
    fig, ax = plt.subplots(figsize=(8, 5))
    ansatte = df["antallAnsatte"].fillna(0)
    ax.hist(ansatte, bins=40, color="#2f855a", edgecolor="white")
    ax.set_yscale("log")
    ax.set_title("Figure 4.2 - Distribution of number of employees")
    ax.set_xlabel("Number of employees")
    ax.set_ylabel("Count (log scale)")
    plt.tight_layout()
    plt.savefig(cap4 / "figur_4_2_fordeling_ansatte.png", dpi=300)
    plt.close()

    # 4.3 Bankruptcy rate by industry (top 10 by frequency)
    tmp = df.copy()
    tmp["bransje_2siffer"] = tmp["bransje_2siffer"].astype(str)
    top_ind = tmp["bransje_2siffer"].value_counts().head(10).index
    sub_ind = tmp[tmp["bransje_2siffer"].isin(top_ind)]
    rate_ind = sub_ind.groupby("bransje_2siffer")["konkurs_bin"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(rate_ind.index, rate_ind.values, color="#805ad5")
    ax.set_title("Figure 4.3 - Bankruptcy rate by industry (top 10)")
    ax.set_xlabel("Industry code (2-digit)")
    ax.set_ylabel("Bankruptcy rate")
    plt.tight_layout()
    plt.savefig(cap4 / "figur_4_3_konkursrate_bransje.png", dpi=300)
    plt.close()

    # 4.4 Bankruptcy rate by county (top 10 by frequency)
    top_fylke = tmp["fylke"].value_counts().head(10).index
    sub_fylke = tmp[tmp["fylke"].isin(top_fylke)]
    rate_fylke = sub_fylke.groupby("fylke")["konkurs_bin"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(rate_fylke.index, rate_fylke.values, color="#d69e2e")
    ax.set_title("Figure 4.4 - Bankruptcy rate by county (top 10)")
    ax.set_xlabel("County code")
    ax.set_ylabel("Bankruptcy rate")
    plt.tight_layout()
    plt.savefig(cap4 / "figur_4_4_konkursrate_fylke.png", dpi=300)
    plt.close()

    # 4.5 Correlation heatmap for numeric variables used in models
    corr_cols = NUM_COLS + BIN_COLS + ["konkurs_bin"]
    corr = df[corr_cols].corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr.columns, fontsize=8)
    ax.set_title("Figure 4.5 - Correlation matrix (numeric model variables)")
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Correlation", rotation=270, labelpad=12)
    plt.tight_layout()
    plt.savefig(cap4 / "figur_4_5_korrelasjonsmatrise.png", dpi=300)
    plt.close()


def fit_models(df: pd.DataFrame):
    X = df[ALL_FEATURES].copy()
    y = df["konkurs_bin"].astype(int)

    for col in CAT_COLS:
        X[col] = X[col].fillna("MISSING").astype(str)
    X = X.fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        stratify=y,
        random_state=42,
    )

    log_pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUM_COLS + BIN_COLS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
        ]
    )
    log_model = Pipeline(
        steps=[
            ("preprocess", log_pre),
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
    log_model.fit(X_train, y_train)
    log_proba = log_model.predict_proba(X_test)[:, 1]

    xgb_pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUM_COLS + BIN_COLS),
            (
                "cat",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                CAT_COLS,
            ),
        ]
    )
    xgb_model = Pipeline(
        steps=[
            ("preprocess", xgb_pre),
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
    xgb_model.fit(X_train, y_train)
    xgb_proba = xgb_model.predict_proba(X_test)[:, 1]

    return X_test, y_test, log_model, log_proba, xgb_model, xgb_proba


def threshold_metrics(y_true: pd.Series, y_proba: np.ndarray, thresholds: np.ndarray) -> pd.DataFrame:
    rows = []
    for t in thresholds:
        pred = (y_proba >= t).astype(int)
        rows.append(
            {
                "threshold": t,
                "precision": precision_score(y_true, pred, zero_division=0),
                "recall": recall_score(y_true, pred, zero_division=0),
                "f1": f1_score(y_true, pred, zero_division=0),
            }
        )
    return pd.DataFrame(rows)


def make_chapter5_figures(X_test, y_test, log_model, log_proba, xgb_model, xgb_proba) -> None:
    cap5 = OUT_DIR / "kap5_resultater"

    # 5.1 Combined ROC
    fpr_l, tpr_l, _ = roc_curve(y_test, log_proba)
    fpr_x, tpr_x, _ = roc_curve(y_test, xgb_proba)
    auc_l = roc_auc_score(y_test, log_proba)
    auc_x = roc_auc_score(y_test, xgb_proba)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr_l, tpr_l, label=f"Logistic regression (AUC={auc_l:.3f})", lw=2)
    ax.plot(fpr_x, tpr_x, label=f"XGBoost (AUC={auc_x:.3f})", lw=2)
    ax.plot([0, 1], [0, 1], "--", color="gray")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Figure 5.1 - ROC curve comparison")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(cap5 / "figur_5_1_roc_sammenligning.png", dpi=300)
    plt.close()

    # 5.2 Combined Precision-Recall
    p_l, r_l, _ = precision_recall_curve(y_test, log_proba)
    p_x, r_x, _ = precision_recall_curve(y_test, xgb_proba)
    pr_auc_l = auc(r_l, p_l)
    pr_auc_x = auc(r_x, p_x)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(r_l, p_l, label=f"Logistic regression (PR AUC={pr_auc_l:.3f})", lw=2)
    ax.plot(r_x, p_x, label=f"XGBoost (PR AUC={pr_auc_x:.3f})", lw=2)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Figure 5.2 - Precision-Recall curve comparison")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(cap5 / "figur_5_2_pr_sammenligning.png", dpi=300)
    plt.close()

    # 5.3 Threshold analysis (both models)
    th = np.arange(0.01, 0.51, 0.01)
    m_l = threshold_metrics(y_test, log_proba, th)
    m_x = threshold_metrics(y_test, xgb_proba, th)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    for metric, color in [("recall", "#2b6cb0"), ("precision", "#2f855a"), ("f1", "#c53030")]:
        axes[0].plot(m_l["threshold"], m_l[metric], label=metric.capitalize(), color=color)
        axes[1].plot(m_x["threshold"], m_x[metric], label=metric.capitalize(), color=color)

    axes[0].set_title("Logistic regression")
    axes[1].set_title("XGBoost")
    for ax in axes:
        ax.set_xlabel("Threshold")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Score")
    axes[1].legend(loc="best")
    fig.suptitle("Figure 5.3 - Threshold analysis (Precision, Recall, F1)")
    plt.tight_layout()
    plt.savefig(cap5 / "figur_5_3_terskelanalyse.png", dpi=300)
    plt.close()

    # 5.4 Confusion matrices at threshold 0.44
    t_use = 0.44
    pred_l = (log_proba >= t_use).astype(int)
    pred_x = (xgb_proba >= t_use).astype(int)

    cm_l = confusion_matrix(y_test, pred_l)
    cm_x = confusion_matrix(y_test, pred_x)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ConfusionMatrixDisplay(cm_l).plot(ax=axes[0], colorbar=False)
    axes[0].set_title("Logistic regression (threshold=0.44)")
    ConfusionMatrixDisplay(cm_x).plot(ax=axes[1], colorbar=False)
    axes[1].set_title("XGBoost (threshold=0.44)")
    fig.suptitle("Figure 5.4 - Confusion matrices at operational threshold")
    plt.tight_layout()
    plt.savefig(cap5 / "figur_5_4_confusion_matrices.png", dpi=300)
    plt.close()

    # 5.5 XGBoost feature importance
    xgb_step = xgb_model.named_steps["xgb"]
    importances = xgb_step.feature_importances_
    feat_names = NUM_COLS + BIN_COLS + CAT_COLS
    imp_df = pd.DataFrame({"feature": feat_names, "importance": importances}).sort_values("importance", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    top = imp_df.head(12)
    ax.barh(top["feature"], top["importance"], color="#805ad5")
    ax.invert_yaxis()
    ax.set_xlabel("Importance")
    ax.set_title("Figure 5.5 - XGBoost feature importance")
    plt.tight_layout()
    plt.savefig(cap5 / "figur_5_5_feature_importance_xgb.png", dpi=300)
    plt.close()

    # Optional compact summary chart for chapter text support
    metrics_summary = pd.DataFrame(
        {
            "Model": ["Logistic regression", "XGBoost"],
            "AUC": [auc_l, auc_x],
            "Recall@0.44": [recall_score(y_test, pred_l), recall_score(y_test, pred_x)],
            "Precision@0.44": [precision_score(y_test, pred_l, zero_division=0), precision_score(y_test, pred_x, zero_division=0)],
            "F1@0.44": [f1_score(y_test, pred_l, zero_division=0), f1_score(y_test, pred_x, zero_division=0)],
        }
    )
    metrics_summary.to_csv(cap5 / "modelloppsummering_kap5.csv", index=False)


def main() -> None:
    ensure_output_dirs()
    df = load_and_prepare_data()

    make_chapter3_figures(df)
    make_chapter4_figures(df)

    X_test, y_test, log_model, log_proba, xgb_model, xgb_proba = fit_models(df)
    make_chapter5_figures(X_test, y_test, log_model, log_proba, xgb_model, xgb_proba)

    print(f"Saved figures under: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
