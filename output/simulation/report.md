# Simuleringsrapport

## Inställningar

- Partier: 250
- Profiler: balanced mot balanced
- Första seed: 20260710
- Tvåspelarläge: 16 unika brickor, 8 turer per spelare

## Resultat

- Genomsnittspoäng: 28.41
- Medianpoäng: 29.00
- Min/max: 19 / 31
- Oavgjorda partier: 32.0%
- Genomsnittligt antal djur: 5.89
- Genomsnittlig reservatstäthet: 0.847

## Djurandelar

- baver: 97.8%
- fiskgjuse: 99.2%
- groda: 95.0%
- lo: 97.4%
- radjur: 100.0%
- trana: 99.8%

## Spårbarhet

`example-game.json` innehåller en fullständig draglogg med öppna brickor,
valda brick-ID:n, koordinater, djur och återstående hög.

Motorn kontrollerar efter varje parti att:

- exakt 16 brickor användes
- alla 16 ID:n var unika
- de använda ID:na exakt motsvarar tvåspelaruppsättningen

Resultaten är balanshypoteser, inte ersättning för fysiska speltester.
