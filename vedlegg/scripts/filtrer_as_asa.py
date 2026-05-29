import pandas as pd

filnavn = "enheter_2026-02-03T04-23-42.272983144 (1).csv.gz"

# Les filen robust
df = pd.read_csv(
    filnavn,
    compression="gzip",
    sep=";",
    on_bad_lines="skip",
    dtype=str,
    engine="python"
)

print("Antall rader totalt:", len(df))

# Filtrer ut AS og ASA
print("\nKolonnenavn tolket av pandas:")
print(df.columns.tolist())


print("Antall AS/ASA funnet:", len(organisasjonsform.kode))

# Lag ren CSV med bare organisasjonsnummer
organisasjonsform.kode[["organisasjonsnummer"]].to_csv("organisasjonsnumre_as_asa.csv", index=False)

print("\nFilen 'organisasjonsnumre_as_asa.csv' er laget.")
