# Projektstatus

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
- Fungerande generatorer för print-PDF:er
- Pandoc-bygge av regelbok
- GitHub Actions för validering, preview och release
- Spelmotor för 2–4 spelare
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
- `output/` och `release/` är genererade artefakter.
- Fallback-version finns i `data/game.yaml`; releaseversion kan komma från git-taggen.

## Rekommenderat nästa steg

1. Genomför ett fysiskt två- eller trespelartest.
2. Logga djur, poäng, speltid och regelfrågor.
3. Genomför därefter ett fyraspelarstresstest.
4. Ändra högst 1–3 saker efter varje test.
