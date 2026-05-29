import pandas as pd
import json
import gzip

filnavn = "enheter_alle.json.gz"

# Åpne og last inn JSON-filen
with gzip.open(filnavn, "rt", encoding="utf-8") as f:
    data = json.load(f)

# Normaliser JSON til tabell
df = pd.json_normalize(data)

# Skriv ut kolonnenavn
print("\n=== Kolonner i enheter_alle.json.gz ===")
for col in df.columns:
    print(col)

# Vis de første radene
print("\n=== Første 5 rader ===")
print(df.head())