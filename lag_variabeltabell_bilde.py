import matplotlib.pyplot as plt


def main() -> None:
    columns = ["Variabel", "Rolle", "Type i modell", "Kommentar"]
    rows = [
        ["konkurs_bin", "Maalvariabel (y)", "Binaer (0/1)", "Konkursutfall som predikeres"],
        ["alder_aar", "Forklaringsvariabel (X)", "Numerisk", "Selskapsalder i aar"],
        ["antallAnsatte", "Forklaringsvariabel (X)", "Numerisk", "Storrelsesindikator"],
        ["kapital.belop", "Forklaringsvariabel (X)", "Numerisk", "Kapitalrelatert variabel"],
        ["kapital.innbetalt", "Forklaringsvariabel (X)", "Numerisk", "Kapitalrelatert variabel"],
        ["kapital.fulltInnbetalt", "Forklaringsvariabel (X)", "Numerisk", "Kapitalrelatert variabel"],
        ["kapital.bundet", "Forklaringsvariabel (X)", "Numerisk", "Kapitalrelatert variabel"],
        ["revisjonsfravalg", "Forklaringsvariabel (X)", "Binaer", "Revisjonsstatus"],
        ["mva_registrert", "Forklaringsvariabel (X)", "Binaer", "MVA-registrering"],
        ["underAvvikling_bin", "Forklaringsvariabel (X)", "Binaer", "Juridisk risikosignal"],
        [
            "underTvangsavviklingEllerTvangsopplosning_bin",
            "Forklaringsvariabel (X)",
            "Binaer",
            "Juridisk risikosignal",
        ],
        ["bransje_2siffer", "Forklaringsvariabel (X)", "Kategorisk", "Bransjekode (2-siffer)"],
        [
            "fylke",
            "Forklaringsvariabel (X)",
            "Kategorisk (avledet)",
            "Avledes fra postadresse.kommunenummer",
        ],
    ]

    fig, ax = plt.subplots(figsize=(22, 10))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="left",
        colLoc="left",
        loc="center",
        colColours=["#E8EEF7", "#E8EEF7", "#E8EEF7", "#E8EEF7"],
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)

    col_widths = [0.34, 0.23, 0.18, 0.25]
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_height(cell.get_height() * 1.1)
        cell.set_edgecolor("#6B7280")
        if col < len(col_widths):
            cell.set_width(col_widths[col])

    plt.title("Tabell: Variabler brukt i modellen", fontsize=18, weight="bold", pad=18)
    plt.tight_layout()
    plt.savefig("tabell_variabler_modell.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
