# Vedlegg: Reproduksjonspakke for masteroppgaven

Denne mappen samler kode og oppsett for a gjenskape analysen fra datauthenting/datagrunnlag til modellkjoring og terskelanalyse.

## Innhold

- `scripts/`: kopi av alle Python-skript i prosjektet
- `run_reproduksjon.py`: ett entrypoint for kjeding av sentrale steg
- `requirements.txt`: avhengigheter
- `metadata_datafreeze.json`: datafreeze-manifest for snapshot og referansedato
- `output/`: reproduksjonsartefakter (fylles ved kjoring)

## Viktig om eksakt datagrunnlag

Eksakt gjenskaping av de samme dataene krever snapshot-filen:

- `alle_enheter.json` (i prosjektroten)

Hashen til snapshot-filen er lagret i `metadata_datafreeze.json`.
Hvis hash stemmer, brukes samme datagrunnlag som ved opprinnelig uttrekk.

## Hurtigstart

Kjør fra prosjektroten:

```powershell
python vedlegg/run_reproduksjon.py --mode snapshot
```

Dette kjører:

1. `scripts/konverter_json_til_csv_kun_AS_ASA.py`
2. `scripts/lag_analysefil.py`
3. `scripts/feature_engineered_enheter.py`
4. `scripts/model_logistisk.py`
5. `scripts/model_1.py`
6. `scripts/robusthet_lekkasje.py`

Og kopierer sentrale resultater til `vedlegg/output/`.

## Alternativer

Kun dataforberedelse (uten modeller):

```powershell
python vedlegg/run_reproduksjon.py --mode snapshot --skip-models
```

Ny uthenting fra API (kan gi avvik fra opprinnelige resultater):

```powershell
python vedlegg/run_reproduksjon.py --mode api
```

## Miljø

Installer avhengigheter i virtuelt miljø:

```powershell
pip install -r vedlegg/requirements.txt
```

## Kommentar

Noen skript i `scripts/` er inkludert som full dokumentasjon av arbeidsloypa, men er ikke nodvendige i standard reproduksjonspipeline.
