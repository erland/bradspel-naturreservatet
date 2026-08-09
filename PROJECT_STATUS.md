# Projektstatus

## Version

v0.3.3

## Kort beskrivning

Naturreservatet är ett lätt tile-placement-spel där spelarna väljer öppna landskapsbrickor, bygger varsitt reservat och kryssar djur när nya brickor skapar rätt livsmiljöer.

## Klart

- Regelbok med 8 turer per spelare
- 32 unika landskapsbrickor
- Fasta uppsättningar för 2, 3 och 4 spelare
- Sex djurkrav med poäng
- Visuellt A6-referenskort
- A6-poängblad och A4-ark med fyra poängblad
- Återanvändbara SVG-ikoner
- Fungerande generatorer för brickor och referenskort
- Projektvalidering

## Aktuell teststatus

Redo för solo-genomgång och interna fysiska speltester.

## Kända designrisker

- Groda och Rådjur kan vara för lätta.
- Effektiva spelare kan möjligen nå för många djur.
- Bonuspoängen är ännu inte validerade genom fysiska tester.
- Sista valet när brickhögen tar slut kan missgynna spelaren sist i turordningen.
- Fyraspelarläget behöver testas för väntetid och brickkonkurrens.

## Viktiga beslut

- Ingen startbricka används.
- Första landskapsbrickan placeras fritt.
- Minst ett fält på den nyplacerade brickan måste ingå i djurkravet.
- Varje spelare får exakt 8 turer.
- 2/3/4 spelare använder 16/24/32 brickor.

## Rekommenderat nästa steg

1. Genomför ett fysiskt tvåspelartest.
2. Logga djur, poäng, speltid och regelfrågor.
3. Genomför därefter ett fyraspelartest.
4. Ändra högst 1–3 saker efter varje test.

## Spelmotor

- [SPELMOTORPLAN] finns i `docs/SPELMOTORPLAN.md`.
- Tvåspelarregelmotorn är implementerad.
- Slumpmässig, kortsiktig och balanserad AI finns.
- Seeds och fullständiga dragloggar stöds.
- Automatiska tester verifierar djurkrav, placering och unika brickor.
- En första körning med 250 partier finns i `output/simulation/`.

## Spelmotor v0.3.2

- Växlande startspelare.
- Profiljämförelser mellan random, greedy och balanced.
- 11 automatiska tester godkända.
- Motorn rekommenderas nu att frysas inför fysiskt speltest.

## Spelmotor v0.3.3

- Generellt stöd för 2–4 spelare.
- 24 respektive 32 unika brickor verifieras för 3 och 4 spelare.
- Åtta turer per spelare verifieras.
- Startspelaren roteras jämnt.
- Sittplatsstatistik och djurfrekvenser rapporteras.
- Motorn rekommenderas nu att frysas.
