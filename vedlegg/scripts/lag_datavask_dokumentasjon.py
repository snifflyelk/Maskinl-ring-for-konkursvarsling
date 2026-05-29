from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUT_CSV = ROOT / "rensetabell_datavask.csv"
OUT_TXT = ROOT / "metodeavsnitt_datavask_med_tall.txt"
OUT_PNG = ROOT / "figurer_kap3_5" / "kap3_metode" / "figur_3_4_datavask_flytskjema.png"


def count_orgnummer_in_json(path: Path) -> int:
    needle = '"organisasjonsnummer"'
    chunk_size = 4 * 1024 * 1024
    count = 0

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        prev = ""
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            text = prev + chunk
            count += text.count(needle)
            prev = text[-(len(needle) - 1) :]

    return count


def make_table() -> pd.DataFrame:
    raw_json_n = count_orgnummer_in_json(ROOT / "alle_enheter.json")

    as_asa_n = len(pd.read_csv(ROOT / "alle_enheter_AS_ASA.csv", dtype=str))
    analyse_n = len(pd.read_csv(ROOT / "analyseklare_enheter.csv", dtype=str))
    feature_n = len(pd.read_csv(ROOT / "feature_engineered_enheter.csv", dtype=str))

    robust_df = pd.read_csv(ROOT / "robusthet_lekkasje_resultater.csv")
    full_n = int(robust_df.loc[robust_df["variant"] == "full_med_juridiske", "n_obs"].iloc[0])
    early_n = int(
        robust_df.loc[
            robust_df["variant"] == "tidligvarsel_utvalg_uten_juridiske", "n_obs"
        ].iloc[0]
    )

    rows = [
        {
            "steg": "1. Raa data (alle_enheter.json)",
            "input_n": raw_json_n,
            "output_n": raw_json_n,
            "fjernet_n": 0,
            "begrunnelse": "Utgangspunkt foer filtrering.",
            "i_hovedpipeline": "Ja",
            "kilde": "alle_enheter.json (stroemmende opptelling av organisasjonsnummer)",
        },
        {
            "steg": "2. Filtrering til AS/ASA",
            "input_n": raw_json_n,
            "output_n": as_asa_n,
            "fjernet_n": raw_json_n - as_asa_n,
            "begrunnelse": "Fjerner enheter som ikke er organisasjonsform AS eller ASA.",
            "i_hovedpipeline": "Ja",
            "kilde": "konverter_json_til_csv_kun_AS_ASA.py",
        },
        {
            "steg": "3. Utvalg av analysevariabler",
            "input_n": as_asa_n,
            "output_n": analyse_n,
            "fjernet_n": as_asa_n - analyse_n,
            "begrunnelse": "Beholder kun relevante kolonner, ingen radfiltrering.",
            "i_hovedpipeline": "Ja",
            "kilde": "lag_analysefil.py",
        },
        {
            "steg": "4. Duplikatkontroll paa organisasjonsnummer",
            "input_n": analyse_n,
            "output_n": analyse_n,
            "fjernet_n": 0,
            "begrunnelse": "drop_duplicates er brukt, men ga 0 fjernede observasjoner i lagret fil.",
            "i_hovedpipeline": "Ja",
            "kilde": "lag_analysefil.py + verifisert i CSV",
        },
        {
            "steg": "5. Feature engineering",
            "input_n": analyse_n,
            "output_n": feature_n,
            "fjernet_n": analyse_n - feature_n,
            "begrunnelse": "Transformasjoner/avledede variabler, ingen radfiltrering.",
            "i_hovedpipeline": "Ja",
            "kilde": "feature_engineered_enheter.py",
        },
        {
            "steg": "6. Modellklargjoering av missing",
            "input_n": feature_n,
            "output_n": feature_n,
            "fjernet_n": 0,
            "begrunnelse": "Manglende verdier haandteres med fillna('MISSING')/fillna(0), ikke dropp.",
            "i_hovedpipeline": "Ja",
            "kilde": "model_logistisk.py, model_1.py, lag_figurer_kap3_5.py",
        },
        {
            "steg": "7. Tidligvarsel-utvalg (robusthetstest)",
            "input_n": full_n,
            "output_n": early_n,
            "fjernet_n": full_n - early_n,
            "begrunnelse": "Ekskluderer observasjoner med minst ett juridisk signal = 1.",
            "i_hovedpipeline": "Nei (kun robusthet)",
            "kilde": "robusthet_lekkasje.py + robusthet_lekkasje_resultater.csv",
        },
    ]

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    return df


def make_flow_figure(df: pd.DataFrame) -> None:
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    main = df[df["i_hovedpipeline"] == "Ja"].copy()

    labels = [
        f"{r.steg}\nN={int(r.output_n):,}".replace(",", " ")
        for r in main.itertuples(index=False)
    ]

    fig, ax = plt.subplots(figsize=(16, 3.2))
    ax.axis("off")

    n = len(labels)
    x_start = 0.02
    gap = 0.02
    box_w = (0.96 - (n - 1) * gap) / n
    y = 0.52

    boxes = []
    for i, text in enumerate(labels):
        x = x_start + i * (box_w + gap)
        ax.text(
            x + box_w / 2,
            y,
            text,
            ha="center",
            va="center",
            fontsize=9.5,
            bbox={"boxstyle": "round,pad=0.35", "fc": "#E8F1FB", "ec": "#2B6CB0", "lw": 1.3},
            transform=ax.transAxes,
        )
        boxes.append((x, box_w))

    for i in range(n - 1):
        x1 = boxes[i][0] + boxes[i][1]
        x2 = boxes[i + 1][0]
        ax.annotate(
            "",
            xy=(x2, y),
            xytext=(x1, y),
            xycoords=ax.transAxes,
            arrowprops={"arrowstyle": "->", "lw": 1.6, "color": "#2B6CB0"},
        )

    ax.text(
        0.5,
        0.10,
        "Figur 3.4 - Datavask og filtreringsprosess med observasjonstall (hovedpipeline)",
        ha="center",
        va="center",
        fontsize=11,
        transform=ax.transAxes,
    )

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close()


def make_method_text(df: pd.DataFrame) -> None:
    row = {r["steg"]: r for _, r in df.iterrows()}

    raw_n = int(row["1. Raa data (alle_enheter.json)"]["output_n"])
    as_asa_n = int(row["2. Filtrering til AS/ASA"]["output_n"])
    as_asa_removed = int(row["2. Filtrering til AS/ASA"]["fjernet_n"])
    analyse_n = int(row["3. Utvalg av analysevariabler"]["output_n"])
    feature_n = int(row["5. Feature engineering"]["output_n"])

    early_removed = int(row["7. Tidligvarsel-utvalg (robusthetstest)"]["fjernet_n"])

    analyse_df = pd.read_csv(ROOT / "analyseklare_enheter.csv", dtype=str)
    miss_industry = int(analyse_df["naeringskode1.kode"].isna().sum())
    miss_muni = int(analyse_df["postadresse.kommunenummer"].isna().sum())
    miss_emp = int(analyse_df["antallAnsatte"].isna().sum())

    total = len(analyse_df)
    miss_industry_pct = 100 * miss_industry / total
    miss_muni_pct = 100 * miss_muni / total
    miss_emp_pct = 100 * miss_emp / total

    text = (
        "Forslag til metodeavsnitt med konkrete tall\n\n"
        "Datagrunnlaget besto av {raw_n:,} enheter i alle_enheter.json. Etter filtrering til "
        "organisasjonsformene AS og ASA var {as_asa_n:,} observasjoner igjen, noe som innebar "
        "at {as_asa_removed:,} observasjoner ble fjernet fordi de ikke tilhoerte maelpopulasjonen. "
        "Deretter ble datasettet avgrenset til relevante analysevariabler, uten at observasjoner "
        "ble fjernet (N={analyse_n:,}).\n\n"
        "I neste steg ble duplikater kontrollert paa organisasjonsnummer. Selv om drop_duplicates "
        "ble benyttet, var antall fjernede observasjoner 0 i den lagrede analysefilen. Feature "
        "engineering ble deretter gjennomfoert uten ytterligere bortfall, slik at endelig "
        "hoveddatasett for modellering var N={feature_n:,}.\n\n"
        "Manglende verdier ble i modellklargjoeringen haandtert ved imputering/koding "
        "(fillna('MISSING') for kategoriske variabler og fillna(0) for numeriske), ikke ved "
        "sletting av rader. I analysefilen var andel manglende verdier blant annet "
        "{miss_emp:,} ({miss_emp_pct:.1f} %) for antallAnsatte, "
        "{miss_muni:,} ({miss_muni_pct:.1f} %) for postadresse.kommunenummer, og "
        "{miss_industry:,} ({miss_industry_pct:.1f} %) for naeringskode1.kode.\n\n"
        "I en separat robusthetsanalyse (tidligvarsel-utvalg) ble observasjoner med juridiske "
        "signalsvariabler satt til 1 ekskludert. Dette reduserte utvalget med {early_removed:,} "
        "observasjoner. Dette steget er ikke en del av hovedpipelinen, men en sensitivitetsanalyse."
    ).format(
        raw_n=raw_n,
        as_asa_n=as_asa_n,
        as_asa_removed=as_asa_removed,
        analyse_n=analyse_n,
        feature_n=feature_n,
        miss_emp=miss_emp,
        miss_emp_pct=miss_emp_pct,
        miss_muni=miss_muni,
        miss_muni_pct=miss_muni_pct,
        miss_industry=miss_industry,
        miss_industry_pct=miss_industry_pct,
        early_removed=early_removed,
    )

    OUT_TXT.write_text(text, encoding="utf-8")


def main() -> None:
    df = make_table()
    make_flow_figure(df)
    make_method_text(df)

    print(f"Laget: {OUT_CSV}")
    print(f"Laget: {OUT_TXT}")
    print(f"Laget: {OUT_PNG}")


if __name__ == "__main__":
    main()
