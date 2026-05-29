import pandas as pd
import numpy as np

# Filnavn
input_fil = "analyseklare_enheter.csv"
output_fil = "feature_engineered_enheter.csv"

# 1. Les data
df = pd.read_csv(input_fil, dtype=str)

# 2. Konverter datoer til datetime
dato_kolonner = [
    "stiftelsesdato",
    "registreringsdatoEnhetsregisteret",
    "fravalgRevisjonDato",
    "fravalgRevisjonBeslutningsDato",
    "registreringsdatoMerverdiavgiftsregisteret",
    "konkursdato",
    "tvangsopplostPgaManglendeRevisorDato",
    "tvangsopplostPgaManglendeRegnskapDato",
    "tvangsavvikletPgaManglendeSlettingDato",
    "underRekonstruksjonsforhandlingDato"
]

for kol in dato_kolonner:
    if kol in df.columns:
        df[kol] = pd.to_datetime(df[kol], errors="coerce")

# 3. Lag alder på selskapet
df["alder_aar"] = (
    (pd.Timestamp.today() - df["stiftelsesdato"])
    .dt.days / 365.25
)

# 4. Revisjonsfravalg (binær)
df["revisjonsfravalg"] = np.where(df["fravalgRevisjonDato"].notna(), 1, 0)

# 5. MVA-registrering (binær)
df["mva_registrert"] = np.where(df["registrertIMvaregisteret"] == "true", 1, 0)

# 6. Bransje på 2-siffer nivå
df["bransje_2siffer"] = df["naeringskode1.kode"].str.slice(0, 2)

# 7. Juridiske risikosignaler (binære)
juridiske = [
    "underAvvikling",
    "underTvangsavviklingEllerTvangsopplosning",
]

for kol in juridiske:
    df[kol + "_bin"] = np.where(df[kol] == "true", 1, 0)

dato_juridiske = [
    "tvangsopplostPgaManglendeRevisorDato",
    "tvangsopplostPgaManglendeRegnskapDato",
    "tvangsavvikletPgaManglendeSlettingDato",
    "underRekonstruksjonsforhandlingDato"
]

for kol in dato_juridiske:
    df[kol + "_bin"] = np.where(df[kol].notna(), 1, 0)

# 8. Antall ansatte (numerisk)
df["antallAnsatte"] = pd.to_numeric(df["antallAnsatte"], errors="coerce")

# 9. Kapital (numerisk)
kapital_kolonner = [
    "kapital.belop",
    "kapital.innbetalt",
    "kapital.fulltInnbetalt",
    "kapital.bundet"
]

for kol in kapital_kolonner:
    df[kol] = pd.to_numeric(df[kol], errors="coerce")

# 10. Konkurs (binær) – ROBUST FRA true/false
df["konkurs_bin"] = (
    df["konkurs"]
    .astype(str)
    .str.lower()
    .eq("true")
    .astype(int)
)

print("Fordeling konkurs_bin:")
print(df["konkurs_bin"].value_counts())

# 11. Velg kun variabler som er nyttige i modell
kolonner_til_modell = [
    "organisasjonsnummer",
    "konkurs_bin",
    "alder_aar",
    "antallAnsatte",
    "kapital.belop",
    "kapital.innbetalt",
    "kapital.fulltInnbetalt",
    "kapital.bundet",
    "revisjonsfravalg",
    "mva_registrert",
    "bransje_2siffer",
    "underAvvikling_bin",
    "underTvangsavviklingEllerTvangsopplosning_bin",
    "tvangsopplostPgaManglendeRevisorDato_bin",
    "tvangsopplostPgaManglendeRegnskapDato_bin",
    "tvangsavvikletPgaManglendeSlettingDato_bin",
    "underRekonstruksjonsforhandlingDato_bin",
    "postadresse.kommunenummer"
]

df_out = df[kolonner_til_modell]

# 12. Lagre resultat
df_out.to_csv(output_fil, index=False, encoding="utf-8")

print(f"Feature engineering fullført! Lagret som {output_fil}")
print(f"Antall selskaper i datasettet: {len(df_out)}")
