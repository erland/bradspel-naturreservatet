# Produktionsguide

## Utskriftsinställning

Skriv ut alla PDF-filer i **faktisk storlek (100 %)**. Använd inte ”anpassa till sida”.

## Landskapsbrickor

Fil:

`output/print/landskapsbrickor-70x35mm-aktuell build-version.pdf`

- Liggande A4
- 70 × 35 mm per bricka
- 35 × 35 mm per naturfält
- 32 brickor på tre sidor

### Brickuppsättningar

**2 spelare – 16 brickor**

NR-01, NR-02, NR-04, NR-05, NR-07, NR-08, NR-10, NR-12, NR-14, NR-15, NR-16, NR-18, NR-19, NR-22, NR-23, NR-24

**3 spelare – 24 brickor**

NR-01–NR-24

**4 spelare – 32 brickor**

NR-01–NR-32

## Referenskort

- Ett A6-kort: `output/print/reference-card-a6-v2-aktuell build-version.pdf`
- Fyra kort på A4: `output/print/reference-card-a6-v2-a4-4up-aktuell build-version.pdf`

## Poängblad

- Ett A6-poängblad: `output/print/score-sheet-a6.pdf`
- Fyra poängblad på A4: `output/print/score-sheets-a4.pdf`

## Bygga om filer

```bash
python scripts/build_landscape_tiles.py
python scripts/build_reference_card_v2.py
```

## Kontroll före speltest

- Kontrollera att rätt brickuppsättning används.
- Kontrollera att alla sidor skrivits ut i 100 %.
- Kontrollera att naturfältet mäter 35 × 35 mm efter utskrift.
- Lägg fram fyra öppna brickor.
- Ge varje spelare ett poängblad.
