import requests
import pandas as pd

def hent_enheter(orgform):
    side = 0
    alle = []

    while True:
        url = f"https://data.brreg.no/enhetsregisteret/api/enheter?organisasjonsform={orgform}&size=1000&page={side}"
        r = requests.get(url)
        print(f"Henter {orgform}, side {side}, status {r.status_code}")

        if r.status_code != 200:
            break

        data = r.json()

        # Hvis ingen flere resultater, stopp
        if "_embedded" not in data or "enheter" not in data["_embedded"]:
            break

        enheter = data["_embedded"]["enheter"]
        alle.extend(enheter)

        # Sjekk om vi er på siste side
        if "page" in data and (data["page"]["number"] + 1 >= data["page"]["totalPages"]):
            break

        side += 1

    return alle


# Hent AS og ASA
as_enheter = hent_enheter("AS")
asa_enheter = hent_enheter("ASA")

# Slå sammen
alle = as_enheter + asa_enheter

# Lag DataFrame
df = pd.DataFrame(alle)

# Ta kun organisasjonsnummer og navn
df = df[["organisasjonsnummer", "navn", "organisasjonsform"]]

# Lagre til CSV
df.to_csv("organisasjonsnumre_as_asa.csv", index=False, encoding="utf-8")

print("\nFerdig! Filen 'organisasjonsnumre_as_asa.csv' er laget.")
