# Data tilgengelighet

## Kort oppsummering

Repositoriet inneholder kode og reproduksjonsoppsett, men ikke fullt raadatauttrekk i offentlig versjon.

## Hva som ikke er publisert

Filer med raadata og avledede datafiler er holdt utenfor offentlig repo via .gitignore, blant annet:

- alle_enheter.json
- analyseklare_enheter.csv
- feature_engineered_enheter.csv
- andre store eller avledede CSV-filer

Dette er gjort for a unnga ukritisk deling av store datamengder og for a skille tydelig mellom kode og data.

## Hvordan gjenskape analyser

Standard reproduksjon kjores fra prosjektroten:

```powershell
python vedlegg/run_reproduksjon.py --mode snapshot
```

For eksakt reproduksjon av opprinnelig datagrunnlag kreves snapshot-filen alle_enheter.json med samme hash som oppgitt i:

- vedlegg/metadata_datafreeze.json

Hvis snapshot ikke er tilgjengelig, kan pipeline kjores med ny uthenting:

```powershell
python vedlegg/run_reproduksjon.py --mode api
```

Merk at API-modus kan gi avvik i resultater fordi registerdata endres over tid.

## Kontakt

Ved behov for avklaringer om datagrunnlag, tilgang eller reproduksjon, ta kontakt med forfatterne av masteroppgaven.
