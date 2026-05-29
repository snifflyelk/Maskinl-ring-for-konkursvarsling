import pandas as pd

# Filnavn
input_fil = "alle_enheter_AS_ASA.csv"
output_fil = "analyseklare_enheter.csv"

# 1. Les CSV
df = pd.read_csv(input_fil, dtype=str)

# 2. Velg relevante variabler
relevante_kolonner = [
    # Avhengig variabel
    "konkurs",
    "konkursdato",

    # Revisjonsfravalg
    "fravalgRevisjonDato",
    "fravalgRevisjonBeslutningsDato",

    # Selskapskarakteristika
    "organisasjonsnummer",
    "navn",
    "organisasjonsform.kode",
    "stiftelsesdato",
    "registreringsdatoEnhetsregisteret",
    "antallAnsatte",
    "harRegistrertAntallAnsatte",
    "kapital.belop",
    "kapital.innbetalt",
    "kapital.fulltInnbetalt",
    "kapital.bundet",

    # Bransje
    "naeringskode1.kode",
    "naeringskode1.beskrivelse",

    # Geografi
    "postadresse.postnummer",
    "postadresse.kommunenummer",

    # MVA
    "registrertIMvaregisteret",
    "registreringsdatoMerverdiavgiftsregisteret",

    # Juridiske signalvariabler
    "underAvvikling",
    "underTvangsavviklingEllerTvangsopplosning",
    "tvangsopplostPgaManglendeRevisorDato",
    "tvangsopplostPgaManglendeRegnskapDato",
    "tvangsavvikletPgaManglendeSlettingDato",
    "underRekonstruksjonsforhandlingDato",

    # Konsern
    "erIKonsern"
]

# 3. Filtrer DataFrame
df_out = df[relevante_kolonner]

# 4. Fjern duplikater
df_out = df_out.drop_duplicates(subset=["organisasjonsnummer"])

# 5. Lagre ny fil
df_out.to_csv(output_fil, index=False, encoding="utf-8")

print(f"Ny analysefil lagret som {output_fil}")
print(f"Antall selskaper i analysen: {len(df_out)}")