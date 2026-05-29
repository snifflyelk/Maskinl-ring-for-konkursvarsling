import json
import warnings

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier


warnings.filterwarnings("ignore", category=UserWarning)


RANDOM_STATE = 42
DATA_FILE = "feature_engineered_enheter.csv"
OUTPUT_FILE = "robusthet_lekkasje_resultater.csv"


BASE_NUM_COLS = [
    "alder_aar",
    "antallAnsatte",
    "kapital.belop",
    "kapital.innbetalt",
    "kapital.fulltInnbetalt",
    "kapital.bundet",
]

BASE_BIN_COLS = [
    "revisjonsfravalg",
    "mva_registrert",
]

JURIDISKE_COLS = [
    "underAvvikling_bin",
    "underTvangsavviklingEllerTvangsopplosning_bin",
    "tvangsopplostPgaManglendeRevisorDato_bin",
    "tvangsopplostPgaManglendeRegnskapDato_bin",
    "tvangsavvikletPgaManglendeSlettingDato_bin",
    "underRekonstruksjonsforhandlingDato_bin",
]

CAT_COLS = [
    "bransje_2siffer",
    "fylke",
]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)

    if "fylke" not in df.columns and "postadresse.kommunenummer" in df.columns:
        df["fylke"] = df["postadresse.kommunenummer"].astype(str).str[:2]

    needed_cols = ["konkurs_bin"] + BASE_NUM_COLS + BASE_BIN_COLS + JURIDISKE_COLS + CAT_COLS
    missing = [c for c in needed_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Mangler kolonner i datasettet: {missing}")

    for col in BASE_NUM_COLS + BASE_BIN_COLS + JURIDISKE_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in CAT_COLS:
        df[col] = df[col].astype(str)

    df["konkurs_bin"] = pd.to_numeric(df["konkurs_bin"], errors="coerce").fillna(0).astype(int)
    return df


def build_logistic_pipeline(num_bin_cols, cat_cols):
    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_bin_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        solver="liblinear",
        random_state=RANDOM_STATE,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("model", model),
        ]
    )


def build_xgb_pipeline(num_bin_cols, cat_cols, y_train):
    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_bin_cols),
            (
                "cat",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                cat_cols,
            ),
        ]
    )

    neg = int((y_train == 0).sum())
    pos = int((y_train == 1).sum())
    scale_pos_weight = (neg / pos) if pos > 0 else 1.0

    model = XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="auc",
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("model", model),
        ]
    )


def evaluate_predictions(y_true, y_prob, threshold):
    y_pred = (y_prob >= threshold).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )

    return {
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
    }


def run_variant(df, variant_name, features, threshold_list):
    X = df[features].copy()
    y = df["konkurs_bin"].copy()

    cat_cols = [c for c in CAT_COLS if c in features]
    num_bin_cols = [c for c in features if c not in cat_cols]

    for col in cat_cols:
        X[col] = X[col].fillna("MISSING").astype(str)
    for col in num_bin_cols:
        X[col] = pd.to_numeric(X[col], errors="coerce")
    X = X.fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    rows = []

    for model_name in ["logistisk", "xgboost"]:
        if model_name == "logistisk":
            model = build_logistic_pipeline(num_bin_cols, cat_cols)
        else:
            model = build_xgb_pipeline(num_bin_cols, cat_cols, y_train)

        model.fit(X_train, y_train)
        y_prob = model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)

        for t in threshold_list:
            m = evaluate_predictions(y_test, y_prob, t)
            rows.append(
                {
                    "variant": variant_name,
                    "model": model_name,
                    "threshold": t,
                    "n_obs": int(len(X)),
                    "n_pos": int(y.sum()),
                    "pos_rate": float(y.mean()),
                    "auc": float(auc),
                    "pr_auc": float(pr_auc),
                    "precision": m["precision"],
                    "recall": m["recall"],
                    "f1": m["f1"],
                    "features": json.dumps(features, ensure_ascii=True),
                }
            )

    return rows


def main():
    df = load_data()

    full_features = BASE_NUM_COLS + BASE_BIN_COLS + JURIDISKE_COLS + CAT_COLS
    no_legal_features = BASE_NUM_COLS + BASE_BIN_COLS + CAT_COLS
    legal_only_features = JURIDISKE_COLS

    threshold_list = [0.20, 0.44, 0.50]
    all_rows = []

    # Variant 1: Full modell (inkluderer juridiske signalvariabler)
    all_rows.extend(run_variant(df, "full_med_juridiske", full_features, threshold_list))

    # Variant 2: Fjern alle juridiske signalvariabler
    all_rows.extend(run_variant(df, "uten_juridiske", no_legal_features, threshold_list))

    # Variant 3: Kun juridiske signalvariabler
    all_rows.extend(run_variant(df, "kun_juridiske", legal_only_features, threshold_list))

    # Variant 4: Tidligvarsel-utvalg (dropper foretak med juridisk signal = 1)
    juridisk_sum = df[JURIDISKE_COLS].fillna(0).sum(axis=1)
    early_df = df.loc[juridisk_sum == 0].copy()

    if early_df["konkurs_bin"].sum() >= 50:
        all_rows.extend(
            run_variant(
                early_df,
                "tidligvarsel_utvalg_uten_juridiske",
                no_legal_features,
                threshold_list,
            )
        )
    else:
        print(
            "Advarsel: For fa konkursobservasjoner i tidligvarsel-utvalget "
            "til stabil modelltrening. Hopper over variant 4."
        )

    result_df = pd.DataFrame(all_rows)
    result_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    summary = (
        result_df.sort_values(["variant", "model", "threshold"])
        [[
            "variant",
            "model",
            "threshold",
            "n_obs",
            "n_pos",
            "auc",
            "pr_auc",
            "precision",
            "recall",
            "f1",
        ]]
    )

    print("\nRobusthetsanalyse ferdig.")
    print(f"Resultater lagret i: {OUTPUT_FILE}")
    print("\nKort oppsummering:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()