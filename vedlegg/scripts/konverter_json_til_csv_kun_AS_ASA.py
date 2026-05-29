import pandas as pd
import json

# Filnavn
input_fil = "alle_enheter.json"
output_fil = "alle_enheter_AS_ASA.csv"

# 1. Les JSON-filen
with open(input_fil, "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Normaliser JSON til en flat tabell
df = pd.json_normalize(data)

# 3. Filtrer til kun AS og ASA
df_as_asa = df[df["organisasjonsform.kode"].isin(["AS", "ASA"])]

print(f"Antall enheter totalt: {len(df)}")
print(f"Antall AS/ASA: {len(df_as_asa)}")

# 4. Lagre som CSV
df_as_asa.to_csv(output_fil, index=False, encoding="utf-8")

print(f"Konvertering fullført! Lagret som {output_fil}")