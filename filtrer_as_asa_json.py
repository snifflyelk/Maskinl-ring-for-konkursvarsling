import pandas as pd
import json
import gzip

filnavn = "enheter_alle.json.gz"

# 1. Åpne gzip-komprimert JSON
with gzip.open(filnavn, "rt", encoding="utf-8") as f:
    data = json.load(f)

# 2. Flatten JSON-strukturen til en tabell
df = pd.json_normalize(data)

print("Antall rader totalt:", len(df))
print("\nKolonner funnet i datasettet:")
for col in df.columns:
    print(" -", col)

# 3. Filtrer AS og ASA
as_asa = df[df["organisasjonsform.kode"].isin(["AS", "ASA"])]

print("\nAntall AS/ASA funnet:", len(as_asa))

# 4. Lag ren CSV med bare organisasjonsnummer
as_asa[["organisasjonsnummer"]].to_csv("organisasjonsnumre_as_asa.csv", index=False)

print("\nFilen 'organisasjonsnumre_as_asa.csv' er laget.")
