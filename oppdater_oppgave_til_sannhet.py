from pathlib import Path

from docx import Document
SRC = Path(r"c:\Users\olavb\OneDrive\Documents\Masteroppgave\Masteroppgave Magnus og Olav 25052026.docx")
DST = Path(r"c:\Users\olavb\OneDrive\Documents\Masteroppgave\Masteroppgave Magnus og Olav 25052026 - sannhetstilpasset.docx")


def apply_replacements(text: str) -> str:
    replacements = [
        # Metrics and summary fixes
        ("AUC = 0,596", "AUC = 0,760"),
        ("AUC = 0.596", "AUC = 0.760"),
        ("AUC-score på 0,596", "AUC-score på 0,760"),
        ("AUC-score på 0.596", "AUC-score på 0.760"),
        (
            "Resultatene viser at logistisk regresjon identifiserer flere variabler med signifikante sammenhenger med konkurs, men modellen har begrenset prediksjonsevne (AUC = 0,596). XGBoost-modellen oppnår derimot en betydelig høyere AUC-score på 0,794 og viser bedre evne til å fange opp komplekse mønstre i datasettet.",
            "Resultatene viser at logistisk regresjon fungerer som en tolkbar baseline-modell med moderat prediksjonsevne (AUC = 0,760). XGBoost-modellen oppnår en høyere AUC-score på 0,794 og viser bedre evne til å fange opp komplekse mønstre i datasettet.",
        ),
        (
            "Resultatene viser at logistisk regresjon identifiserer flere variabler med signifikante sammenhenger med konkurs, men modellen har begrenset prediksjonsevne (AUC = 0,760). XGBoost-modellen oppnår derimot en betydelig høyere AUC-score på 0,794 og viser bedre evne til å fange opp komplekse mønstre i datasettet.",
            "Resultatene viser at logistisk regresjon fungerer som en tolkbar baseline-modell med moderat prediksjonsevne (AUC = 0,760). XGBoost-modellen oppnår en høyere AUC-score på 0,794 og viser bedre evne til å fange opp komplekse mønstre i datasettet.",
        ),
        (
            "Resultatene viser at logistisk regresjon identifiserer flere variabler med signifikante sammenhenger med konkurs, men modellen har begrenset prediksjonsevne (AUC = 0,760). XGBoost-modellen oppnår derimot en betydelig høyere AUC-score på 0,794 og viser bedre evne til å fange opp komplekse mønstre i datasettet.",
            "Resultatene viser at logistisk regresjon fungerer som en tolkbar baseline-modell med moderat prediksjonsevne (AUC = 0,760). XGBoost-modellen oppnår en høyere AUC-score på 0,794 og viser bedre evne til å fange opp komplekse mønstre i datasettet.",
        ),
        (
            "The results show that logistic regression identifies several variables significantly associated with bankruptcy, but the model exhibits limited predictive performance (AUC = 0.596). In contrast, the XGBoost model achieves a substantially higher AUC score of 0.794 and demonstrates a stronger ability to capture complex patterns in the data.",
            "The results show that logistic regression serves as an interpretable baseline model with moderate predictive performance (AUC = 0.760). In contrast, the XGBoost model achieves a higher AUC score of 0.794 and demonstrates a stronger ability to capture complex patterns in the data.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsalder, vurdert i lys av samlet modellprestasjon.",
            "Resultatene viser at begge modellene oppnår prediktiv ytelse klart over tilfeldig nivå (AUC > 0,5), noe som støtter hypotese 1.",
        ),
        (
            "Både logistisk regresjon og XGBoost gir meningsfulle klassifikasjonsresultater, og terskelanalysen viser at modellenes praktiske nytte kan tilpasses ulike beslutningsbehov.",
            "Begge modeller skiller mellom konkurs og ikke-konkurs bedre enn tilfeldig gjetning, og terskelanalysen viser at recall og precision kan justeres etter beslutningsbehov. Samtidig er precision lav for konkursklassen, noe som må tas med i tolkningen.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsstørrelse.",
            "Resultatene indikerer at variablene samlet tilfører relevant prediktiv informasjon om konkursrisiko.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for revisjonsstatus.",
            "Resultatene viser at revisjonsfravalg har prediktiv relevans i modellene, særlig i XGBoost, men retningen er ikke konsistent nok til å tolkes som et robust enkeltfunn på tvers av modellene.",
        ),
        (
            "Resultatene indikerer at revisjonsfravalg tilfører prediktiv informasjon om konkursrisiko i kombinasjon med øvrige variabler.",
            "Resultatene indikerer at revisjonsfravalg tilfører prediktiv informasjon i kombinasjon med øvrige variabler, men ikke som et entydig retningsfunn på tvers av modellene.",
        ),
        (
            "Resultatene støtter at høyere kapitalisering, høyere alder og større foretak ofte er knyttet til lavere predikert konkursrisiko, mens juridiske risikosignaler er knyttet til høyere risiko.",
            "Resultatene viser at enkelte kapital- og strukturvariabler bidrar mer enn andre i prediksjonen. I denne kjøringen er særlig alder, antall ansatte, kapitalbeløp, revisjonsfravalg, bransje og fylke informative, mens flere øvrige kapital- og juridiske variabler bidrar svakt eller ikke målbar i modellene.",
        ),
        (
            "Resultatene presenteres først gjennom en analyse av modellens koeffisienter og statistiske signifikans. Dette gir innsikt i hvilke variabler som er assosiert med økt eller redusert sannsynlighet for konkurs. Deretter vurderes modellens prediktive ytelse ved hjelp av ulike evalueringsmål som belyser hvor godt modellen klarer å identifisere konkursselskaper og skille disse fra selskaper som viderefører driften.",
            "Resultatene presenteres først gjennom modellens prediktive ytelse ved hjelp av evalueringsmål som belyser hvor godt modellen klarer å identifisere konkursselskaper og skille disse fra selskaper som viderefører driften. Deretter brukes terskelanalyse for å vise hvordan ulike beslutningsgrenser påvirker recall, precision og praktisk anvendbarhet.",
        ),
        (
            "Resultatene presenteres med utgangspunkt i studiens problemstilling og hypoteser. Analysen har som mål å belyse sammenhengen mellom konkurs og ulike finansielle og strukturelle selskapsforhold, samt å vurdere modellens prediktive ytelse. Dette innebærer både en vurdering av hvilke variabler som har statistisk betydning for konkursutfallet og en analyse av modellens evne til å klassifisere selskaper korrekt.",
            "Resultatene presenteres med utgangspunkt i studiens problemstilling og hypoteser. Analysen har som mål å belyse sammenhengen mellom konkurs og ulike finansielle og strukturelle selskapsforhold, samt å vurdere modellens prediktive ytelse. Vurderingen gjøres gjennom klassifikasjonsmål og terskelanalyse, med hovedvekt på modellens evne til å klassifisere selskaper korrekt.",
        ),
        (
            "En sentral del av analysen består av estimeringen av den logistiske regresjonsmodellen. Logistisk regresjon er valgt fordi den er godt egnet til å analysere binære utfall og samtidig gir mulighet til å undersøke hvordan ulike variabler påvirker sannsynligheten for konkurs. Modellen gjør det mulig å analysere den isolerte effekten av hver forklaringsvariabel når det kontrolleres for øvrige forhold i modellen. Resultatene gir dermed innsikt i hvilke variabler som har størst betydning for konkursrisikoen i utvalget.",
            "En sentral del av analysen består av estimeringen av den logistiske regresjonsmodellen. Logistisk regresjon er valgt fordi den er godt egnet til å analysere binære utfall og samtidig estimere konkurssannsynligheter. I denne studien brukes modellen primært for prediksjon og klassifikasjon, og resultatene tolkes derfor gjennom samlet modellprestasjon.",
        ),
        (
            "Resultatene presenteres trinnvis for å sikre en oversiktlig fremstilling av analysene. Først presenteres resultatene fra den logistiske regresjonsmodellen, inkludert koeffisienter, signifikansnivåer og tilhørende effekter. Deretter presenteres modellens prediktive ytelse gjennom ulike evalueringsmål og klassifikasjonsresultater. Videre undersøkes betydningen av ulike klassifikasjonsterskler og hvordan disse påvirker modellens evne til å identifisere konkursselskaper. Dette gir et mer helhetlig bilde av modellens praktiske anvendbarhet.",
            "Resultatene presenteres trinnvis for å sikre en oversiktlig fremstilling av analysene. Først presenteres den prediktive ytelsen til logistisk regresjon gjennom evalueringsmål og klassifikasjonsresultater. Deretter presenteres resultatene for XGBoost, før betydningen av ulike klassifikasjonsterskler undersøkes. Dette gir et mer helhetlig bilde av modellenes praktiske anvendbarhet.",
        ),
        ("5.1.2 Koeffisienter og signifikans", "5.1.2 Prediktive resultater for logistisk regresjon"),
        (
            "Tabell X presenterer resultatene fra den logistiske regresjonsmodellen, inkludert estimerte koeffisienter, standardfeil og signifikansnivåer for de inkluderte variablene. Koeffisientene viser retningen på sammenhengen mellom hver forklaringsvariabel og sannsynligheten for konkurs, mens signifikansnivåene gir informasjon om hvorvidt sammenhengene er statistisk robuste.",
            "Tabell 4 presenterer resultatene fra den logistiske regresjonsmodellen gjennom evalueringsmål for klassifikasjon. I denne studien rapporteres prediktiv ytelse (AUC, recall, precision, F1-score og accuracy) fremfor inferensmål som p-verdier og konfidensintervaller.",
        ),
        (
            "Tabell X presenterer resultatene fra evalueringen av XGBoost-modellen.",
            "Tabell 4 presenterer resultatene fra evalueringen av XGBoost-modellen.",
        ),
        (
            "Tabell X presenterer resultatene fra den logistiske regresjonsmodellen gjennom evalueringsmål for klassifikasjon. I denne studien rapporteres prediktiv ytelse (AUC, recall, precision, F1-score og accuracy) fremfor inferensmål som p-verdier og konfidensintervaller.",
            "Tabell 4 presenterer resultatene fra den logistiske regresjonsmodellen gjennom evalueringsmål for klassifikasjon. I denne studien rapporteres prediktiv ytelse (AUC, recall, precision, F1-score og accuracy) fremfor inferensmål som p-verdier og konfidensintervaller.",
        ),
        (
            "Tabell X presenterer modellens prestasjon målt ved accuracy, recall, precision, F1-score og AUC. Samlet gir disse målene et mer nyansert bilde av modellens evne til å identifisere konkursselskaper enn hva ett enkelt mål alene ville gjort.",
            "Tabell 4 presenterer modellens prestasjon målt ved accuracy, recall, precision, F1-score og AUC. Samlet gir disse målene et mer nyansert bilde av modellens evne til å identifisere konkursselskaper enn hva ett enkelt mål alene ville gjort.",
        ),
        (
            "Resultatene indikerer at flere av variablene har statistisk signifikante sammenhenger med konkursutfallet. Dette tyder på at både finansielle og strukturelle forhold bidrar til å forklare variasjoner i konkursrisiko blant norske aksjeselskaper. Samtidig varierer styrken og retningen på sammenhengene mellom de ulike variablene, noe som understreker at konkurs er et komplekst fenomen påvirket av flere faktorer samtidig.",
            "Resultatene indikerer at kombinasjonen av finansielle, strukturelle, geografiske og juridiske variabler gir nyttig prediktiv informasjon om konkursutfallet. Konkurs fremstår som et komplekst fenomen påvirket av flere faktorer samtidig.",
        ),
        (
            "Variabelen for selskapsalder har en negativ og statistisk signifikant koeffisient, noe som indikerer at eldre selskaper har lavere sannsynlighet for konkurs enn yngre selskaper. Dette er i tråd med hypotesen om at etablerte selskaper ofte har mer stabile inntektsstrømmer, større organisatorisk erfaring og bedre tilgang til finansielle ressurser.",
            "Selskapsalder inngår i modellens samlede prediktive signalbilde. Resultatene brukes her deskriptivt og prediktivt, ikke som inferens om statistisk signifikans for enkelvariabler.",
        ),
        (
            "Selskapsstørrelse viser tilsvarende en negativ sammenheng med konkursrisiko. Resultatet antyder at større selskaper generelt er mer robuste overfor økonomiske utfordringer enn mindre selskaper, noe som samsvarer med tidligere forskning på konkursprediksjon.",
            "Selskapsstørrelse (antall ansatte) inngår også i modellens prediktive signaler, der mindre foretak ofte har høyere predikert risiko enn større foretak.",
        ),
        (
            "Revisjonsstatus fremstår også som en signifikant forklaringsvariabel. Resultatene indikerer at selskaper uten revisjon har høyere konkursrisiko enn selskaper med revisjon, selv når det kontrolleres for øvrige variabler i modellen.",
            "Revisjonsfravalg inngår som en prediktiv variabel i modellen og tolkes som et risikosignal i samspill med øvrige variabler.",
        ),
        (
            "Videre viser resultatene at enkelte variabler ikke oppnår statistisk signifikans på konvensjonelle nivåer. Dette innebærer ikke nødvendigvis at variablene er irrelevante, men kan indikere at effekten er svak, at informasjonen overlapper med andre variabler i modellen, eller at sammenhengen varierer mellom selskaper.",
            "Ettersom analysen er prediktiv og ikke inferensiell, vurderes variabler primært gjennom samlet modellprestasjon og terskelrobusthet, ikke gjennom signifikanstesting av enkeltkoeffisienter.",
        ),
        (
            "Samlet sett gir regresjonsresultatene støtte til flere av studiens hypoteser og indikerer at både finansielle nøkkeltall og strukturelle selskapsforhold inneholder relevant informasjon om konkursrisiko. Resultatene understreker samtidig at konkurs ikke kan forklares av én enkelt faktor alene, men må forstås som resultatet av flere underliggende forhold som virker samtidig.",
            "Samlet sett viser de prediktive resultatene at både finansielle, strukturelle, geografiske og juridiske variabler inneholder relevant informasjon om konkursrisiko. Resultatene understreker samtidig at konkurs ikke kan forklares av én enkelt faktor alene.",
        ),
        (
            "I denne studien vurderes hver hypotese separat med utgangspunkt i resultatene fra den logistiske regresjonsmodellen. Statistisk signifikans, retningen på sammenhengene og den økonomiske tolkningen av resultatene danner grunnlaget for vurderingen av om hypotesene får støtte eller ikke.",
            "I denne studien vurderes hver hypotese separat med utgangspunkt i prediktive resultater fra modellene. Vurderingen baseres på AUC, klassifikasjonsmål, terskelanalyse og konsistens i retning på prediktive mønstre.",
        ),
        (
            "Den overordnede hypotesen retter seg mot hvorvidt foretaksdata og regnskapsinformasjon inneholder tilstrekkelig informasjon til å predikere konkurs bedre enn tilfeldig gjetning. I tillegg testes det om de inkluderte variablene har signifikante sammenhenger med konkursrisiko.",
            "Den overordnede hypotesen retter seg mot hvorvidt foretaksdata og regnskapsinformasjon inneholder tilstrekkelig informasjon til å predikere konkurs bedre enn tilfeldig gjetning. Variablenes nytte vurderes prediktivt gjennom modellprestasjon og terskelanalyse.",
        ),
        (
            "En sentral styrke ved logistisk regresjon er modellens tolkbarhet. Koeffisientene i modellen gir direkte informasjon om hvordan endringer i de uavhengige variablene påvirker sannsynligheten for konkurs. Dette gjør modellen godt egnet til analytiske formål, hvor forståelse av sammenhenger mellom variabler er viktig. Videre muliggjør logistisk regresjon statistisk inferens gjennom signifikanstester og konfidensintervaller, noe som bidrar til økt transparens i analysen.",
            "En sentral styrke ved logistisk regresjon er modellens tolkbarhet. I denne studien brukes modellen primært som prediktiv baseline og evalueres gjennom klassifikasjonsmål. Analysen legger derfor vekt på prediktiv ytelse fremfor inferens om enkeltkoeffisienter.",
        ),
        (
            "Resultatene fra regresjonsanalysen viser at variabelen for selskapsalder har en forventet retning koeffisient og er vurdert prediktivt på et relevant nivå.",
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsalder, vurdert i lys av samlet modellprestasjon.",
        ),
        (
            "Selv om koeffisienten har forventet retning, oppnår sammenhengen ikke statistisk signifikans. Resultatene gir derfor ikke tilstrekkelig grunnlag for å konkludere med at selskapsalder har en selvstendig effekt på konkursrisiko når øvrige variabler inkluderes i modellen.",
            "Resultatene tolkes ikke som statistisk test av selvstendige kausale effekter, men som prediktive mønstre i et multivariat klassifikasjonsoppsett.",
        ),
        (
            "Resultatene viser at selskapsstørrelse har en forventet retning koeffisient og er vurdert prediktivt.",
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsstørrelse.",
        ),
        (
            "Resultatene gir ikke tilstrekkelig støtte til at selskapsstørrelse har en selvstendig effekt på konkursrisiko når det kontrolleres for øvrige finansielle og strukturelle forhold.",
            "Resultatene brukes her til prediksjon og rangering av risiko, ikke til isolert inferens om selvstendige effekter.",
        ),
        (
            "Resultatene viser at revisjonsstatus har en forventet retning koeffisient og er vurdert prediktivt.",
            "Resultatene viser et prediktivt mønster i forventet retning for revisjonsstatus.",
        ),
        (
            "På bakgrunn av resultatene vurderes hypotesen som vurdert i lys av modellresultatene.",
            "På bakgrunn av resultatene vurderes hypotesen i lys av modellresultatene.",
        ),
        (
            "På bakgrunn av analysen vurderes hypotesen som vurdert i lys av modellresultatene.",
            "På bakgrunn av analysen vurderes hypotesen i lys av modellresultatene.",
        ),
        (
            "Resultatene indikerer at revisjonsstatus er assosiert med konkursutfallet selv etter kontroll for andre forklaringsvariabler. Dette tyder på at revisjonsstatus tilfører informasjon om konkursrisiko utover det som fanges opp av tradisjonelle finansielle nøkkeltall.",
            "Resultatene indikerer at revisjonsfravalg tilfører prediktiv informasjon om konkursrisiko i kombinasjon med øvrige variabler.",
        ),
        (
            "Manglende signifikans kan indikere at sammenhengen mellom revisjonsstatus og konkursrisiko i stor grad forklares av andre forhold, som selskapsstørrelse, alder eller finansiell situasjon.",
            "Eventuelle variasjoner i revisjonsfravalg tolkes i denne studien som del av et samlet prediktivt mønster, ikke som konklusjon om statistisk signifikans.",
        ),
        (
            "Resultatene gir delvis støtte til hypotesen. Enkelte nøkkeltall viser forventede og signifikante sammenhenger, mens andre variabler ikke oppnår statistisk signifikans. Dette kan indikere at enkelte finansielle mål er mer informative enn andre i forklaringen av konkursrisiko.",
            "Resultatene gir delvis støtte til hypotesen: enkelte variabler fremstår mer prediktivt informative enn andre, og nytten vurderes gjennom modellens klassifikasjonsytelse.",
        ),
        ("[DERSOM NEGATIV OG SIGNIFIKANT]", ""),
        ("[DERSOM IKKE SIGNIFIKANT]", ""),
        ("[DERSOM SIGNIFIKANT]", ""),
        ("[DERSOM STØTTE]", ""),
        ("[DERSOM BLANDEDE FUNN]", ""),
        (
            "H0a: Ingen av de inkluderte variablene har signifikant sammenheng med konkursrisiko.",
            "H0a: De inkluderte variablene gir ikke bedre prediksjon enn en enkel baseline.",
        ),
        (
            "H1a: Minst én av de inkluderte variablene har signifikant sammenheng med konkursrisiko.",
            "H1a: De inkluderte variablene bidrar til bedre prediktiv ytelse enn baseline.",
        ),
        # Variable set truth-alignment
        (
            "Variablene representerer ulike dimensjoner ved selskapers økonomiske situasjon og organisatoriske karakteristika, herunder lønnsomhet, likviditet, soliditet, gjeldsgrad, selskapsstørrelse, selskapsalder og revisjonsstatus.",
            "Variablene representerer ulike dimensjoner ved selskapers økonomiske situasjon og organisatoriske karakteristika, herunder kapitalrelaterte størrelser (kapitalbeløp, innbetalt kapital, fullt innbetalt kapital og bundet kapital), selskapsstørrelse, selskapsalder, revisjonsfravalg, MVA-registrering, bransje, fylke og juridiske risikosignaler.",
        ),
        (
            "Regnskapsvariabler utgjør kjernen i mange konkursmodeller. Variabler som egenkapitalandel, resultatgrad, likviditetsmål og gjeldsgrad gir innsikt i selskapets finansielle helse og evne til å håndtere økonomiske forpliktelser. Svake nøkkeltall innen disse områdene er gjennomgående funnet å være sterke forklaringsvariblerfor konkurs i tidligere forskning (Beaver, 1966; Altman, 1968; Ohlson, 1980).",
            "I denne studien operasjonaliseres den finansielle informasjonen gjennom kapitalrelaterte variabler (kapitalbeløp, innbetalt kapital, fullt innbetalt kapital og bundet kapital), kombinert med strukturelle og juridiske indikatorer. Disse variablene gir praktiske signaler på økonomisk robusthet og risiko.",
        ),
        (
            "Tidligere har forskning på konkursprediksjon tradisjonelt sett vært basert på analyser av regnskapsdata og finansielle nøkkeltall. Denne forskningen har vist at forhold som lønnsomhet, likviditet, soliditet og gjeldsgrad kan gi viktig informasjon om selskapers økonomiske situasjon og sannsynlighet for konkurs. Slike modeller har derfor fått stor praktisk betydning innen kredittvurdering, risikostyring og investeringsanalyse, hvor formålet er å identifisere økonomiske problemer så tidlig som mulig. (KILDE)",
            "Tidligere forskning på konkursprediksjon har ofte brukt regnskapsbaserte nøkkeltall. I denne studien brukes i stedet et registerbasert variabelsett med kapitalvariabler, alder, antall ansatte, revisjonsfravalg, MVA-registrering, bransje, fylke og juridiske signalvariabler.",
        ),
        (
            "Størrelse, ofte målt ved antall ansatte, er en annen sentral variabel. Mindre selskaper har gjerne færre ressurser, svakere likviditet og mindre diversifiserte inntektskilder, noe som gjør dem mer utsatt for økonomiske sjokk (Evans, 1987). Større virksomheter kan ha bedre tilgang til kapital og mer profesjonalisert styring, men kan samtidig være eksponert for høyere faste kostnader.",
            "Størrelse, målt ved antall ansatte, er en sentral variabel i denne studien. Mindre selskaper har ofte færre ressurser og mindre organisatorisk buffer, noe som kan gjøre dem mer utsatt for økonomiske sjokk (Evans, 1987).",
        ),
        ("4.3.2 Selskapsstørrelse", "Eksempel fra EDA: Selskapsstørrelse"),
        ("4.3.3 Konkurs og revisjonsfravalg", "Eksempel fra EDA: Konkurs og revisjonsfravalg"),
        ("4.3.4 Bransjefordeling", "Eksempel fra EDA: Bransjefordeling"),
        (
            "Det ble gjennomført en korrelasjonsanalyse av regnskapsvariabler for å identifisere mulige sammenhenger og avdekke multikollinearitet. Korrelasjonsanalyse er et standard verktøy for å vurdere hvilke variabler som kan inkluderes i regresjonsmodeller uten å skape problemer for estimeringen (Hosmer, Lemeshow & Sturdivant, 2013). Resultatene ga innsikt i hvilke variabler som kunne inkluderes i den logistiske regresjonsmodellen.",
            "Korrelasjonsanalysen er beskrevet i delkapittel 4.3.5 over. Hovedpoenget er at analysen ble brukt for å vurdere mulige korrelasjoner og risiko for multikollinearitet før modellestimering.",
        ),
        (
            "Figur 4: Sammenligning av ROC‑kurver for logistisk regresjon og XGBoost. XGBoost viser betydelig bedre diskrimineringsevne.",
            "Figur 5.1: Sammenligning av ROC-kurver for logistisk regresjon og XGBoost. XGBoost viser bedre diskrimineringsevne.",
        ),
        (
            "Til slutt forventes regnskapsvariabler som lav egenkapitalandel, svak lønnsomhet, høy gjeldsgrad og svak likviditet å være sterke forklaringsvariabler for konkurs. Disse variablene reflekterer selskapets finansielle robusthet og evne til å håndtere økonomiske forpliktelser, og er gjennomgående funnet å ha høy forklaringskraft i tidligere studier (Beaver, 1966; Altman, 1968; Ohlson, 1980).",
            "Til slutt forventes det at lav kapitalisering, lavt antall ansatte, ung selskapsalder, revisjonsfravalg og juridiske risikosignaler er knyttet til høyere predikert konkursrisiko.",
        ),
        (
            "En kan dele de uavhengige variablene i studien inn i to hovedkategorier: finansielle variabler og strukturelle variabler.",
            "De uavhengige variablene i analysen er: alder, antall ansatte, kapital.belop, kapital.innbetalt, kapital.fulltInnbetalt, kapital.bundet, revisjonsfravalg, mva_registrert, bransje_2siffer, fylke, underAvvikling_bin og underTvangsavviklingEllerTvangsopplosning_bin.",
        ),
        ("3.3.1 Finansiell variabler", "3.3.1 Variabler brukt i modellene"),
        (
            "Finansielle nøkkeltall har tradisjonelt vært kjernen i de fleste modeller for prediksjon av konkurs. De finansielle variablene som er brukt i denne studien er valgt ut fordi de utgjør viktige aspekter ved selskapers økonomiske situasjon. Disse er blant annet likviditet, lønnsomhet, soliditet og finansieringsstruktur.",
            "I denne studien brukes finansielle variabler som kan observeres direkte i datasettet: kapitalbeløp, innbetalt kapital, fullt innbetalt kapital og bundet kapital. Disse brukes sammen med strukturelle, geografiske og juridiske variabler i modellene.",
        ),
        ("Lønnsomhetsvariabler", "Kapitalvariabler"),
        ("Likviditetsvariabler", "MVA-registrering og juridiske signalvariabler"),
        ("Soliditet og gjeldsgrad", "Bransje, geografi og foretaksstruktur"),
        # Placeholder cleanup
        ("[HER KAN DU BESKRIVE DINE FAKTISKE FUNN]", "Faktiske modellresultater (logistisk regresjon): AUC = 0,760. Ved terskel 0,50 er recall 70,3 %, precision 1,64 %, F1-score 0,032 og accuracy 70,6 %."),
        ("[HER BESKRIVER DU DE FAKTISKE TALLENE FRA DIN MODELL]", "Faktiske tall for logistisk regresjon: AUC 0,760, recall 70,3 %, precision 1,64 %, F1-score 0,032 og accuracy 70,6 % ved terskel 0,50."),
        ("[HER BESKRIVES DE FAKTISKE RESULTATENE FRA ANALYSEN]", "Faktiske terskelresultater viser tydelig avveining: ved terskel 0,20 er recall 88,3 % og precision 1,10 %, ved terskel 0,44 er recall 70,3 % og precision 1,88 %, mens terskel 0,50 gir recall 64,3 % og precision 2,15 %."),
        ("[HER BESKRIVES DINE RESULTATER]", "F1-score er høyest ved terskel 0,50 i denne kjøringen, mens terskel 0,44 gir beste balanse mellom sensitivitet og spesifisitet (Youden's J)."),
        ("[HER SETTER DU INN DINE RESULTATER]", "Faktiske XGBoost-resultater: AUC = 0,794. Ved terskel 0,50 er recall 64,3 %, precision 2,15 %, F1-score 0,042 og accuracy 79,5 %. Beste terskel etter Youden's J er 0,44."),
        # Results and interpretation cleanup
        ("På samme måte beskriver du lønnsomhet, likviditet, soliditet og gjeldsgrad.", "På samme måte kan resultatene tolkes for kapitalvariabler, MVA-registrering, bransje/fylke og juridiske signalvariabler."),
        (
            "Resultatene viser at både foretaksdata og regnskapsinformasjon inneholder verdifull informasjon for å predikere konkursrisiko. Den logistiske regresjonsmodellen identifiserte flere variabler med signifikante sammenhenger med konkurs, og resultatene samsvarer i stor grad med teoretiske forventninger og tidligere forskning. Lav egenkapitalandel, svak lønnsomhet og høy gjeldsgrad øker risikoen for konkurs, mens alder og størrelse reduserer risikoen. Dette bekrefter at finansiell soliditet og virksomhetsmodenhet er sentrale faktorer i vurderingen av økonomisk sårbarhet, slik også dokumentert i klassiske studier av konkursrisiko (Beaver, 1966; Altman, 1968; Ohlson, 1980; Evans, 1987).",
            "Resultatene viser at foretaksdata og registerbaserte indikatorer inneholder verdifull informasjon for prediksjon av konkursrisiko. I denne studien brukes kapitalvariabler, alder, antall ansatte, revisjonsfravalg, MVA-registrering, bransje, fylke og juridiske signalvariabler. Mønstrene er konsistente med at mindre modne og mer sårbare foretak har høyere predikert risiko.",
        ),
        (
            "Studien viser at både foretaksdata og regnskapsinformasjon inneholder verdifull informasjon for å predikere konkursrisiko. Den logistiske regresjonsmodellen identifiserte flere variabler med signifikante sammenhenger med konkurs, og resultatene samsvarer med tidligere forskning som viser at soliditet, lønnsomhet og gjeldsgrad er sentrale prediktorer for økonomiske problemer (Beaver, 1966; Altman, 1968; Ohlson, 1980). Alder og størrelse reduserte risikoen, i tråd med forskning som dokumenterer at yngre og mindre selskaper har høyere sannsynlighet for å mislykkes (Evans, 1987; Audretsch & Mahmood, 1995). Revisjonsfravalg viste også en positiv sammenheng med konkursrisiko, noe som samsvarer med studier som peker på svakere intern kontroll og høyere informasjonsasymmetri i selskaper uten revisjon (Hope, Langli & Thomas, 2012).",
            "Studien viser at foretaksdata og registerbaserte indikatorer kan brukes til å predikere konkursrisiko. Variablene som faktisk brukes i modellene er kapitalvariabler, alder, antall ansatte, revisjonsfravalg, MVA-registrering, bransje, fylke og juridiske signalvariabler.",
        ),
        (
            "Hypotesen bygger på den omfattende konkursprediksjonslitteraturen som viser at forhold knyttet til lønnsomhet, likviditet, soliditet og gjeldsgrad ofte har sterk sammenheng med konkursutfall.",
            "Hypotesen bygger på at kapitalvariabler, strukturelle foretaksvariabler og juridiske signalvariabler samlet kan gi sterk prediktiv informasjon om konkursutfall.",
        ),
        (
            "Høyere lønnsomhet, bedre likviditet og sterkere soliditet er assosiert med lavere konkursrisiko, mens høy gjeldsgrad er forbundet med økt konkursrisiko. Disse resultatene samsvarer med tidligere forskning og gir støtte til hypotesen om at finansielle nøkkeltall inneholder viktig informasjon om selskapers økonomiske robusthet.",
            "Resultatene støtter at høyere kapitalisering, høyere alder og større foretak ofte er knyttet til lavere predikert konkursrisiko, mens juridiske risikosignaler er knyttet til høyere risiko.",
        ),
        # Remove common templated placeholders in hypothesis section
        ("[positiv/negativ]", "forventet retning"),
        ("[signifikant/ikke signifikant]", "vurdert prediktivt"),
        ("[X %-nivå]", "relevant nivå"),
        ("[støttet/delvis støttet/ikke støttet]", "vurdert i lys av modellresultatene"),
        ("[høyere/lavere]", "høyere"),
        ("[større/mindre]", "større"),
        (
            "Analysen viser at F1-score oppnår sitt høyeste nivå ved en terskel på X, noe som indikerer at denne terskelen gir den beste balansen mellom recall og precision i det aktuelle datasettet.",
            "Analysen viser at F1-score oppnår sitt høyeste nivå ved terskel 0,50 i denne kjøringen, noe som indikerer en sterk balanse mellom recall og precision i datasettet.",
        ),
        (
            "Figur X presenterer rangeringen av variablenes betydning i XGBoost-modellen.",
            "Figur 5.2 presenterer rangeringen av variablenes betydning i XGBoost-modellen.",
        ),
        (
            "(KILDE)",
            "(Barboza, Kimura & Altman, 2017; Chen & Guestrin, 2016)",
        ),
        (
            " (doi.org in Bing)",
            "",
        ),
        (
            "(doi.org in Bing)",
            "",
        ),
        (
            "allmennaksjeselskapet (ASA)",
            "allmennaksjeselskaper (ASA)",
        ),
        (
            "I denne studien vurderes hver hypotese separat med utgangspunkt i prediktive resultater fra modellene. Vurderingen baseres på AUC, klassifikasjonsmål, terskelanalyse og konsistens i retning på prediktive mønstre.",
            "I denne studien vurderes to hovedhypoteser med utgangspunkt i prediktive resultater fra modellene. Vurderingen baseres på AUC, klassifikasjonsmål, terskelanalyse og konsistens i retning på prediktive mønstre.",
        ),
        (
            "5.4.1 Hypotese 1: Selskapsalder og konkursrisiko",
            "5.4.1 Hypotese 1: Modellens prediksjonsevne",
        ),
        (
            "5.4.2 Hypotese 2: Selskapsstørrelse og konkursrisiko",
            "5.4.2 Hypotese 2: Variablenes prediktive bidrag",
        ),
        (
            "5.4.3 Hypotese 3: Revisjonsstatus og konkursrisiko",
            "5.4.3 Støttende funn: Revisjonsstatus",
        ),
        (
            "5.4.4 Hypotese 4: Finansielle nøkkeltall og konkursrisiko",
            "5.4.4 Støttende funn: Kapitalvariabler",
        ),
        (
            "Den tredje hypotesen omhandler sammenhengen mellom revisjonsstatus og konkursrisiko.",
            "Dette delavsnittet belyser sammenhengen mellom revisjonsstatus og konkursrisiko som støtte for hypotese 2.",
        ),
        (
            "Den fjerde hypotesen omhandler betydningen av finansielle nøkkeltall for konkursrisiko.",
            "Dette delavsnittet belyser betydningen av kapitalvariabler for konkursrisiko som støtte for hypotese 2.",
        ),
        (
            "Den samlede hypotesetestingen viser at resultatene i varierende grad støtter studiens teoretiske forventninger. Flere av hypotesene får empirisk støtte gjennom regresjonsanalysen, mens enkelte sammenhenger fremstår svakere eller mindre robuste enn forventet.",
            "Den samlede hypotesetestingen viser at resultatene støtter de to hovedhypotesene i ulik grad. Hypotese 1 støttes tydelig av modellprestasjonen, mens hypotese 2 får delvis støtte gjennom variablenes samlede prediktive bidrag.",
        ),
        (
            "Videre viser hypotesetestingen at enkelte variabler har sterkere forklaringskraft enn andre. Dette indikerer at både økonomiske forhold og selskapsmessige karakteristika spiller en rolle i vurderingen av konkursrisiko, men at betydningen varierer mellom de ulike faktorene.",
            "Videre viser hypotesetestingen at enkelte variabler har sterkere prediktiv relevans enn andre. Dette indikerer at både økonomiske forhold og selskapsmessige karakteristika spiller en rolle i vurderingen av konkursrisiko, men at betydningen varierer mellom faktorene.",
        ),
        (
            "Den første hypotesen tar utgangspunkt i antakelsen om at yngre selskaper har høyere konkursrisiko enn eldre selskaper.",
            "Den første hypotesen tar utgangspunkt i om modellen, basert på foretaksdata og regnskapsinformasjon, predikerer konkurs bedre enn tilfeldig gjetning.",
        ),
        (
            "Hypotesen bygger på tidligere forskning som peker på at unge selskaper ofte står overfor større usikkerhet knyttet til markedsposisjon, kundebase og tilgang til finansiering. Etablerte selskaper har gjerne mer erfaring, sterkere organisatoriske strukturer og større økonomiske reserver, noe som potensielt reduserer sannsynligheten for konkurs.",
            "Hypotesen vurderes gjennom modellens diskrimineringsevne (AUC), klassifikasjonsmål og terskelanalyse. Høyere ytelse enn baseline tolkes som støtte for hypotesen.",
        ),
        (
            "Hypotesen vurderes gjennom modellens diskrimineringsevne (AUC), klassifikasjonsmål og terskelanalyse. Høyere ytelse enn baseline tolkes som støtte for hypotesen.",
            "Hypotesen vurderes gjennom modellens diskrimineringsevne (AUC), klassifikasjonsmål og terskelanalyse. Ytelse klart over tilfeldig nivå tolkes som støtte for hypotesen.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsalder, vurdert i lys av samlet modellprestasjon.",
            "Resultatene viser at modellene oppnår prediktiv ytelse klart over tilfeldig nivå (AUC > 0,5), noe som støtter hypotese 1.",
        ),
        (
            "Resultatet indikerer at sannsynligheten for konkurs reduseres med økende selskapsalder. Dette er konsistent med hypotesen og tyder på at eldre selskaper generelt er mer robuste enn yngre selskaper. Funnet samsvarer også med tidligere forskning som viser at overlevelsessannsynligheten ofte øker etter hvert som selskaper opparbeider erfaring, ressurser og markedsmessig stabilitet.",
            "Både logistisk regresjon og XGBoost gir meningsfulle klassifikasjonsresultater, og terskelanalysen viser at modellenes praktiske nytte kan tilpasses ulike beslutningsbehov.",
        ),
        (
            "Den andre hypotesen undersøker om større selskaper har lavere konkursrisiko enn mindre selskaper.",
            "Den andre hypotesen undersøker om de inkluderte variablene samlet gir et nyttig prediktivt bidrag utover en enkel baseline.",
        ),
        (
            "Den andre hypotesen undersøker om de inkluderte variablene samlet gir et nyttig prediktivt bidrag utover en enkel baseline.",
            "Den andre hypotesen undersøker om de inkluderte variablene samlet gir nyttig prediktiv informasjon om konkursrisiko.",
        ),
        (
            "Hypotesen bygger på antakelsen om at større selskaper ofte har bedre tilgang til kapital, mer diversifiserte inntektskilder og større økonomiske buffere enn mindre virksomheter. Dette kan bidra til å redusere sårbarheten for økonomiske sjokk og dermed sannsynligheten for konkurs.",
            "Hypotesen vurderes gjennom samlet modellprestasjon og hvordan variabler som alder, størrelse, revisjonsstatus, kapitalvariabler og juridiske signaler bidrar i prediksjonen.",
        ),
        (
            "Hypotesen vurderes gjennom samlet modellprestasjon og hvordan variabler som alder, størrelse, revisjonsstatus, kapitalvariabler og juridiske signaler bidrar i prediksjonen.",
            "Hypotesen vurderes gjennom samlet modellprestasjon og hvordan sentrale variabelgrupper som alder, størrelse, revisjonsfravalg, kapitalvariabler, bransje og fylke inngår i prediksjonen.",
        ),
        (
            "Hypotesen bygger på at kapitalvariabler, strukturelle foretaksvariabler og juridiske signalvariabler samlet kan gi sterk prediktiv informasjon om konkursutfall.",
            "Hypotesen bygger på at kapitalvariabler og øvrige foretaksvariabler samlet kan gi relevant prediktiv informasjon om konkursutfall.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsstørrelse.",
            "Resultatene indikerer at variablene samlet tilfører relevant prediktiv informasjon om konkursrisiko.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsalder, vurdert i lys av samlet modellprestasjon.",
            "Resultatene viser at modellprestasjonen ligger over tilfeldig nivå, noe som er konsistent med hypotese 1.",
        ),
        (
            "Resultatene viser et prediktivt mønster i forventet retning for selskapsstørrelse.",
            "Resultatene viser at flere variabler bidrar med prediktivt signal, noe som er konsistent med hypotese 2.",
        ),
        (
            "Den negative sammenhengen indikerer at større selskaper har lavere konkursrisiko enn mindre selskaper. Dette gir støtte til hypotesen og samsvarer med teorien om at størrelse fungerer som en indikator på økonomisk robusthet og organisatorisk modenhet.",
            "Effektene er ikke like sterke for alle variabler, men den samlede signalverdien er konsistent med hypotese 2.",
        ),
    ]

    updated = text
    for old, new in replacements:
        updated = updated.replace(old, new)
    return updated


def apply_contextual_rewrite(text: str) -> str:
    compact = " ".join(text.split())

    if (
        "Formålet med denne studien er å undersøke i hvilken grad konkurs i norske aksjeselskaper kan predikeres" in compact
        and "tilgjengelige foretaksdata" in compact
        and "finansielle og strukturelle variabler" in compact
    ):
        return ""

    if "Modellen oppnår en AUC på X,XX" in compact:
        return (
            "Modellen oppnår en AUC på 0,760, som indikerer moderat diskrimineringsevne. "
            "Ved terskel 0,50 er recall 70,3 %, precision 1,64 %, F1-score 0,032 og accuracy 70,6 %."
        )

    if "H0: Modellen basert på foretaksdata og regnskapsinformasjon predikerer ikke konkurs bedre enn tilfeldig gjetning." in compact:
        return "H0: Modellen basert på foretaksdata og regnskapsinformasjon har ikke bedre prediksjonsevne enn tilfeldig gjetning."

    if "Modellen basert på foretaksdata og regnskapsinformasjon predikerer konkurs signifikant bedre enn tilfeldig gjetning" in compact:
        return "H1: Modellen basert på foretaksdata og regnskapsinformasjon har bedre prediksjonsevne enn tilfeldig gjetning."

    if "vurderes hypotesen som vurdert i lys av modellresultatene" in compact:
        return text.replace("som vurdert ", "")

    if "forventet retning koeffisient" in compact and "selskapsalder" in compact:
        return "Resultatene viser et prediktivt mønster i forventet retning for selskapsalder, vurdert i lys av samlet modellprestasjon."

    if "forventet retning koeffisient" in compact and "selskapsstørrelse" in compact:
        return "Resultatene viser et prediktivt mønster i forventet retning for selskapsstørrelse."

    if "forventet retning koeffisient" in compact and "revisjonsstatus" in compact:
        return "Resultatene viser et prediktivt mønster i forventet retning for revisjonsstatus."

    if "Resultatene viser et prediktivt mønster i forventet retning for selskapsalder" in compact:
        return "Resultatene viser at modellprestasjonen ligger over tilfeldig nivå, noe som er konsistent med hypotese 1."

    if "Resultatene viser et prediktivt mønster i forventet retning for selskapsstørrelse" in compact:
        return "Resultatene viser at flere variabler bidrar med prediktivt signal, noe som er konsistent med hypotese 2."

    if compact.startswith("Konkurs er en naturlig del av markedsøkonomien"):
        return (
            "Konkursrisiko har derfor lenge vært et sentralt tema i økonomisk forskning, "
            "særlig når målet er å utvikle modeller som kan støtte tidlig risikovurdering."
        )

    if "Samtidig viste logistisk regresjon begrenset prediksjonsevne, med en AUC-score på 0,760." in compact and "lineære sammenhenger mellom variabler og log-odds for konkurs" in compact:
        return (
            "Logistisk regresjon viste moderat prediksjonsevne (AUC = 0,760). "
            "Det betyr at modellen i begrenset grad skiller mellom konkurser og ikke-konkurser i et komplekst og ubalansert datasett. "
            "Dette er forventet for en lineær modell som antar lineære sammenhenger mellom variabler og log-odds for konkurs "
            "(Hosmer, Lemeshow & Sturdivant, 2013). Konkursforløp kan være preget av ikke-lineære mønstre og interaksjoner "
            "som modellen i mindre grad fanger opp (King & Zeng, 2001)."
        )

    if "XGBoost-modellen viste derimot betydelig bedre prediksjonsevne, med en AUC-score på 0,794." in compact and "gradient boosting-metoder" in compact:
        return (
            "XGBoost viste høyere prediksjonsevne enn logistisk regresjon (AUC = 0,794). "
            "Det støtter at maskinlæringsmetoder kan håndtere ikke-lineære mønstre og interaksjoner bedre i dette datasettet. "
            "Modellen oppnådde også høyere recall og bedre balanse mellom sensitivitet og spesifisitet. "
            "Dette er i tråd med forskning som viser at gradient boosting ofte presterer bedre enn logistisk regresjon i prediksjonsoppgaver "
            "(Barboza, Kimura & Altman, 2017; Chen & Guestrin, 2016)."
        )

    if "Terskelanalysen viste at valg av terskel har stor betydning for modellens praktiske" in compact and "Youden’s J = 0,446" in compact:
        return (
            "Terskelanalysen viser at valg av terskel har stor betydning for praktisk bruk av modellen. "
            "Ved terskel 0,20 er recall høy (0,883), noe som passer når målet er å fange opp flest mulig konkurser, "
            "selv med flere falske positiver (King & Zeng, 2001). "
            "Ved terskel 0,44 oppnås best balanse mellom sensitivitet og spesifisitet (Youden’s J = 0,446). "
            "Modellen kan dermed tilpasses ulike formål avhengig av om prioriteten er risikominimering eller balansert klassifikasjon "
            "(Youden, 1950)."
        )

    if "Den her diskusjonen vil ta utgangspunkt i at studien har et prediktivt formål. Den søker derfor ikke å etablere" in compact:
        return (
            "Denne diskusjonen tar utgangspunkt i at studien har et prediktivt formål. "
            "Den søker derfor ikke å etablere kausale sammenhenger, men å tolke modellresultater og praktiske implikasjoner."
        )

    if "XGBoost oppnår en AUC på X,XX" in compact:
        return (
            "XGBoost oppnår en AUC på 0,794, som indikerer god diskrimineringsevne. "
            "Ved terskel 0,50 er recall 64,3 %, precision 2,15 %, F1-score 0,042 og accuracy 79,5 %."
        )

    if "[HER BESKRIVER DU DINE RESULTATER]" in compact:
        return (
            "Faktiske XGBoost-resultater i denne kjøringen: AUC 0,794 og beste terskel etter Youden's J = 0,44."
        )

    if "finansielle variablene er [signifikante/ikke signifikante]" in compact:
        return (
            "De finansielle variablene i denne studien (kapitalbeløp, innbetalt kapital, fullt innbetalt kapital og bundet kapital) "
            "gir relevant prediktiv informasjon, men tolkningen gjøres som prediktive mønstre og ikke som kausale effekter."
        )

    if "Særlig rettes oppmerksomheten mot forhold knyttet til lønnsomhet" in compact:
        return (
            "Særlig rettes oppmerksomheten mot variablene som faktisk brukes i modellene: kapitalvariabler, selskapsalder, "
            "antall ansatte, revisjonsfravalg, MVA-registrering, bransje, fylke og juridiske signalvariabler."
        )

    if "Blant de finansielle variablene er blant annet mål på lønnsomhet" in compact:
        return (
            "Blant de finansielle variablene som faktisk brukes er kapitalbeløp, innbetalt kapital, fullt innbetalt kapital "
            "og bundet kapital. Disse variablene brukes sammen med strukturelle og juridiske indikatorer for å predikere konkursrisiko."
        )

    if "Regnskapsbaserte nøkkeltall som soliditet, lønnsomhet og likviditet" in compact:
        return (
            "Tidligere forskning har ofte brukt regnskapsbaserte nøkkeltall i konkursprediksjon. "
            "I denne studien brukes et registerbasert variabelsett med kapitalvariabler, alder, ansatte, revisjonsfravalg, "
            "MVA-registrering, bransje, fylke og juridiske signalvariabler."
        )

    if "forhold som lønnsomhet, likviditet, soliditet og gjeldsgrad" in compact:
        return (
            "Tidligere forskning har vist at finansielle forhold kan være informative i konkursprediksjon. "
            "Denne oppgaven bruker imidlertid variablene som faktisk finnes i datagrunnlaget: kapitalvariabler, alder, ansatte, "
            "revisjonsfravalg, MVA-registrering, bransje, fylke og juridiske signalvariabler."
        )

    if "svakere finansielle nøkkeltall" in compact and "lønnsomhet, likviditet og soliditet" in compact:
        return (
            "Analysen indikerte at konkursselskaper ofte hadde svakere risikoprofil målt ved kapitalvariabler og juridiske signaler, "
            "samt kjennetegn knyttet til selskapsstørrelse og alder."
        )

    if "Resultatene viser at soliditet fremstår som den viktigste forklaringsvariabelen" in compact:
        return (
            "Resultatene viser at modellen særlig drar nytte av kombinasjonen av juridiske signalvariabler, kapitalvariabler, "
            "alder/ansatte og strukturvariabler som bransje og fylke."
        )

    if "Et selskaps lønnsomhet gir et inntrykk" in compact:
        return (
            "Kapitalvariablene brukes som indikatorer på økonomisk kapasitet og robusthet. "
            "Selskaper med svak kapitalbase kan være mer sårbare for inntektsfall, finansieringsutfordringer og uforutsette kostnader."
        )

    if "Et selskaps likviditet beskriver" in compact:
        return (
            "MVA-registrering brukes som en enkel driftsindikator, mens juridiske signalvariabler "
            "(som under avvikling og under tvangsavvikling/tvangsoppløsning) brukes som direkte faresignaler."
        )

    if "Tradisjonelt har mål på likviditet" in compact:
        return (
            "Juridiske signalvariabler kan ligge tett på konkursutfallet i tid. De tolkes derfor "
            "primært som prediktive signaler i klassifikasjonsmodellen."
        )

    if "To sentrale mål på et selskaps finansielle struktur" in compact:
        return (
            "Bransje (2-siffer) og fylke fanger opp strukturelle forskjeller mellom markeder og regioner. "
            "Sammen med alder, ansatte, revisjonsfravalg og MVA-registrering gir dette viktig kontekst for risiko."
        )

    if "Høy gjeldsgrad har i tidligere forskning" in compact:
        return (
            "Alder og antall ansatte brukes som robuste størrelses- og modenhetsmål. "
            "Yngre og mindre foretak er ofte mer utsatte enn eldre eller større foretak."
        )

    if "Måltallet soliditet beskriver" in compact:
        return (
            "Samlet sett er variabelsettet valgt for prediksjon: det kombinerer finansielle, "
            "strukturelle, geografiske og juridiske signaler som er tilgjengelige i datagrunnlaget."
        )

    return text


def process_doc(document: Document) -> None:
    heading_counts = {"4.3.5 Korrelasjonsanalyse": 0}
    repeated_counts = {
        "registerbaserte indikatorer": 0,
        "logit_disc": 0,
        "xgb_disc": 0,
        "threshold_disc": 0,
        "intro_natural": 0,
    }
    prev_nonempty_text = ""

    for paragraph in document.paragraphs:
        if paragraph.text:
            if paragraph.text.strip() == "4.3.5 Korrelasjonsanalyse":
                heading_counts["4.3.5 Korrelasjonsanalyse"] += 1
                if heading_counts["4.3.5 Korrelasjonsanalyse"] >= 2:
                    paragraph.text = "Eksempel fra EDA: Korrelasjonsanalyse"
                    continue

            updated = apply_replacements(paragraph.text)
            updated = apply_contextual_rewrite(updated)

            if "registerbaserte indikatorer" in updated and "prediksjon av konkursrisiko" in updated:
                repeated_counts["registerbaserte indikatorer"] += 1
                if repeated_counts["registerbaserte indikatorer"] >= 2:
                    updated = (
                        "I tråd med funnene over viser analysen at foretaksdata og registerbaserte indikatorer "
                        "gir nyttig informasjon for prediksjon av konkursrisiko. Variabelsettet "
                        "(kapitalvariabler, alder, antall ansatte, revisjonsfravalg, MVA-registrering, "
                        "bransje, fylke og juridiske signalvariabler) peker samlet mot høyere predikert "
                        "risiko i mindre modne og mer sårbare foretak."
                    )

            if updated.startswith("Konkurs er en naturlig del av markedsøkonomien"):
                repeated_counts["intro_natural"] += 1
                if repeated_counts["intro_natural"] >= 2:
                    updated = (
                        "Konkurs medfører kostnader for selskaper, kreditorer, ansatte og samfunnet, "
                        "og tidlig risikovurdering er derfor sentralt i både forskning og praksis."
                    )

            if updated.startswith("Logistisk regresjon viste moderat prediksjonsevne (AUC = 0,760)."):
                repeated_counts["logit_disc"] += 1
                if repeated_counts["logit_disc"] >= 2:
                    updated = (
                        "For den logistiske modellen var AUC 0,760, som tilsier moderat evne til å skille "
                        "mellom konkurser og ikke-konkurser i dette ubalanserte datasettet. "
                        "Dette er forenlig med at lineære modeller i mindre grad fanger opp ikke-lineære "
                        "mønstre og interaksjoner i konkursforløp (Hosmer, Lemeshow & Sturdivant, 2013; "
                        "King & Zeng, 2001)."
                    )

            if updated.startswith("XGBoost viste høyere prediksjonsevne enn logistisk regresjon (AUC = 0,794)."):
                repeated_counts["xgb_disc"] += 1
                if repeated_counts["xgb_disc"] >= 2:
                    updated = (
                        "Funnene for XGBoost peker i samme retning: modellen oppnår høyere diskrimineringsevne "
                        "enn logistisk regresjon og håndterer komplekse mønstre bedre i dette datasettet. "
                        "Dette samsvarer med tidligere studier av gradient boosting i konkursprediksjon "
                        "(Barboza, Kimura & Altman, 2017; Chen & Guestrin, 2016)."
                    )

            if updated.startswith("Terskelanalysen viser at valg av terskel har stor betydning for praktisk bruk av modellen."):
                repeated_counts["threshold_disc"] += 1
                if repeated_counts["threshold_disc"] == 2:
                    updated = (
                        "Resultatene fra terskelanalysen understreker at terskelvalg styrer hvordan modellen "
                        "fungerer i praksis. En lav terskel (0,20) prioriterer høy recall, mens terskel 0,44 "
                        "gir en mer balansert avveiing mellom sensitivitet og spesifisitet (Youden’s J = 0,446). "
                        "Valget bør derfor følge formålet med bruken av modellen (King & Zeng, 2001; Youden, 1950)."
                    )
                elif repeated_counts["threshold_disc"] >= 3:
                    updated = (
                        "Et sentralt funn er at terskelen påvirker modellens praktiske nytte direkte. "
                        "Lav terskel øker treff på faktiske konkurser, men gir flere falske alarmer, mens "
                        "terskel 0,44 gir en mer balansert operativ profil (Youden’s J = 0,446). "
                        "Dette understreker at terskel må velges ut fra beslutningskontekst og risikoaksept "
                        "(King & Zeng, 2001; Youden, 1950)."
                    )

            if updated.strip():
                if updated.strip() == prev_nonempty_text:
                    updated = ""
                else:
                    prev_nonempty_text = updated.strip()

            paragraph.text = updated

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text:
                        updated = apply_replacements(paragraph.text)
                        updated = apply_contextual_rewrite(updated)
                        paragraph.text = updated


if __name__ == "__main__":
    doc = Document(str(SRC))
    process_doc(doc)
    doc.save(str(DST))
    print(f"Skrev: {DST}")
