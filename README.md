# Maskinlaering for konkursvarsling

En sammenligning av logistisk regresjon og XGBoost for konkursvarsling i norske aksjeselskaper.

## Om prosjektet

Dette repositoriet inneholder kode brukt i masteroppgaven, inkludert:

- innhenting/utvalg av foretak
- datavask og variabeltransformasjon
- modellering med logistisk regresjon og XGBoost
- terskelanalyser og robusthetsanalyser
- reproduksjonspakke for innleveringsvedlegg

## Reproduksjon (anbefalt start)

Fra prosjektroten kan hele standardpipeline kjores med:

```powershell
python vedlegg/run_reproduksjon.py --mode snapshot
```

Dette bruker lagret snapshot (alle_enheter.json) og kopierer sentrale artefakter til vedlegg/output/.

Kun dataforberedelse (uten modeller):

```powershell
python vedlegg/run_reproduksjon.py --mode snapshot --skip-models
```

Ny API-uthenting (kan gi avvik fra opprinnelige resultater):

```powershell
python vedlegg/run_reproduksjon.py --mode api
```

## Miljo

Installer avhengigheter:

```powershell
pip install -r vedlegg/requirements.txt
```

## Prosjektstruktur

- vedlegg/: reproduksjonspakke for masteroppgaven
- vedlegg/scripts/: kopi av sentrale analyseskript
- vedlegg/run_reproduksjon.py: samlet entrypoint for reproduksjon
- vedlegg/metadata_datafreeze.json: datafreeze-manifest (hash/tidsstempel)
- toppnivaa .py-filer: originale analyseskript brukt i arbeidet

## Data og deling

Av hensyn til storrelse, reproduksjonskontroll og delingsvurderinger er ikke hele datagrunnlaget inkludert i GitHub-repoet.

Se DATA_TILGJENGELIGHET.md for detaljer om:

- hva som er utelatt
- hvordan eksakt dataversjon verifiseres
- hvordan analysen gjenskapes

## Lisens

Kode i dette repositoriet er publisert under MIT License.
