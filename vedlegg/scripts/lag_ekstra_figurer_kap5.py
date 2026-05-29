from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import auc, precision_recall_curve

from lag_figurer_kap3_5 import fit_models, load_and_prepare_data


OUT_DIR = Path("figurer_kap3_5") / "kap5_resultater"


def make_pr_curve(y_true: pd.Series, log_proba: np.ndarray, xgb_proba: np.ndarray) -> None:
    p_l, r_l, _ = precision_recall_curve(y_true, log_proba)
    p_x, r_x, _ = precision_recall_curve(y_true, xgb_proba)

    pr_auc_l = auc(r_l, p_l)
    pr_auc_x = auc(r_x, p_x)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(r_l, p_l, label=f"Logistic regression (PR AUC={pr_auc_l:.3f})", lw=2)
    ax.plot(r_x, p_x, label=f"XGBoost (PR AUC={pr_auc_x:.3f})", lw=2)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Ekstra figur 1 - Precision-Recall curve")
    ax.grid(alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figur_ekstra_1_pr_kurve.png", dpi=300)
    plt.close()


def cumulative_gain(y_true: pd.Series, y_score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    df = pd.DataFrame({"y": np.asarray(y_true), "score": y_score})
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df["cum_pos"] = df["y"].cumsum()

    total_pos = df["y"].sum()
    if total_pos == 0:
        return np.array([0.0, 1.0]), np.array([0.0, 1.0])

    x = np.arange(1, len(df) + 1) / len(df)
    y = (df["cum_pos"] / total_pos).to_numpy()

    x = np.insert(x, 0, 0.0)
    y = np.insert(y, 0, 0.0)
    return x, y


def make_lift_gain_plot(y_true: pd.Series, log_proba: np.ndarray, xgb_proba: np.ndarray) -> None:
    x_l, y_l = cumulative_gain(y_true, log_proba)
    x_x, y_x = cumulative_gain(y_true, xgb_proba)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_l, y_l, label="Logistic regression", lw=2)
    ax.plot(x_x, y_x, label="XGBoost", lw=2)
    ax.plot([0, 1], [0, 1], "--", color="gray", label="Random baseline")
    ax.set_xlabel("Andel selskaper vurdert (fra høyest risiko)")
    ax.set_ylabel("Andel konkurser fanget")
    ax.set_title("Ekstra figur 3 - Cumulative gain / top-k capture")
    ax.grid(alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figur_ekstra_3_lift_topk_capture.png", dpi=300)
    plt.close()


def decile_bankruptcy_rates(y_true: pd.Series, y_score: np.ndarray) -> pd.DataFrame:
    df = pd.DataFrame({"y": np.asarray(y_true), "score": y_score})
    # Use rank to avoid qcut issues when many equal scores exist.
    df["rank"] = df["score"].rank(method="first")
    df["decile"] = pd.qcut(df["rank"], 10, labels=False) + 1

    out = (
        df.groupby("decile", as_index=False)
        .agg(bankruptcy_rate=("y", "mean"), n=("y", "size"))
        .sort_values("decile", ascending=False)
    )
    return out


def make_decile_plot(y_true: pd.Series, log_proba: np.ndarray, xgb_proba: np.ndarray) -> None:
    d_l = decile_bankruptcy_rates(y_true, log_proba)
    d_x = decile_bankruptcy_rates(y_true, xgb_proba)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(d_l["decile"], d_l["bankruptcy_rate"], marker="o", lw=2, label="Logistic regression")
    ax.plot(d_x["decile"], d_x["bankruptcy_rate"], marker="o", lw=2, label="XGBoost")
    ax.set_xlabel("Decile (10 = høyest predikert risiko)")
    ax.set_ylabel("Faktisk konkursrate")
    ax.set_title("Ekstra figur 4 - Konkursrate per risikodecil")
    ax.set_xticks(list(range(10, 0, -1)))
    ax.grid(alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figur_ekstra_4_decile_konkursrate.png", dpi=300)
    plt.close()

    merged = d_l[["decile", "bankruptcy_rate", "n"]].rename(
        columns={"bankruptcy_rate": "logistic_bankruptcy_rate", "n": "logistic_n"}
    ).merge(
        d_x[["decile", "bankruptcy_rate", "n"]].rename(
            columns={"bankruptcy_rate": "xgboost_bankruptcy_rate", "n": "xgboost_n"}
        ),
        on="decile",
        how="inner",
    )
    merged.to_csv(OUT_DIR / "figur_ekstra_4_decile_konkursrate_data.csv", index=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_prepare_data()
    _, y_test, _, log_proba, _, xgb_proba = fit_models(df)

    make_pr_curve(y_test, log_proba, xgb_proba)
    make_lift_gain_plot(y_test, log_proba, xgb_proba)
    make_decile_plot(y_test, log_proba, xgb_proba)

    print(f"Lagret ekstra figurer i: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
