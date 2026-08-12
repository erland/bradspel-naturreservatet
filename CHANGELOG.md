# Changelog

## v0.2 - första projektpaketet

- Skapade projektstruktur.
- Fastställde 24 landskapsbrickor.
- Ersatte djurmarkörer med individuella poängblad.
- Förtydligade neutralt startfält.
- Skärpte kravet för Fiskgjuse.
- Skapade A6-referenskort.
- Skapade A6-poängblad och A4-ark med fyra poängblad.

- Korrigerade landskapsbrickorna till 2:1-format, 70 × 35 mm, med färgkodning och enkla symboler.

- Lade till två SVG-masterark för landskapsbrickorna.
- Lade till tydliga vektorikoner för alla fem naturtyper.
- Ändrade Våtmark till en blågrön bakgrund mellan Skog och Sjö.
- Regenererade landskapsbrickornas PDF från SVG-versionerna.

- Minskade terrängikonerna i båda SVG-arken för bättre luft och läsbarhet.
- Byggde om landskapsbrickornas PDF direkt från de korrigerade SVG-filerna.

## v0.2.1

- Verifierade att terrängikonerna i SVG-filerna använder skala 0,58.
- Skapade nya versionsmärkta SVG- och PDF-filer för att undvika cacheade länkar.
- Renderade PDF-filen till PNG för visuell kontroll.

## v0.2.2

- Minskade alla terrängikoner i SVG-filerna med 30 % jämfört med v0.2.1.
- Minskade Äng-ikonen ytterligare 10 % för bättre visuell balans.
- Regenererade PDF-filen från de uppdaterade SVG-filerna.
- Korrigerade Äng-ikonens SVG-transform så den extra minskningen gäller på båda sidor.

## v0.2.3

- Extraherade Skog, Sjö, Äng, Berg och Våtmark till separata SVG-masterfiler.
- Lade till `data/style.yaml` och `assets/style-guide.md`.
- Lade till återanvändbar brickmall.
- Ersatte platshållarscriptet med ett fungerande genereringsscript.
- Regenererade två SVG-ark och landskapsbrickornas PDF från källorna.

## v0.2.4

- Skapade visuellt A6-referenskort v2.
- Lade till färgkodade kombinationsexempel för alla sex djur.
- Återanvände terrängikonerna från `assets/icons/`.
- Lade till A4-ark med fyra referenskort.

## v0.2.5

- Justerade radhöjderna på A6-referenskortet efter exempelens antal rader.
- Standardiserade alla exempelbrickor till 9 × 9 mm.
- Regenererade A6- och A4-versionerna.

## v0.2.6

- Lade till `assets/icons/any-terrain.svg`.
- Uppdaterade Fiskgjusens exempel med tre valfria naturfält.
- Lade till förklaringen `? = valfri naturtyp`.
- Regenererade A6- och A4-referenskorten.

- Lade till neutral startbricka 35×35 mm.

- v0.2.8: Startbrickan har tagits bort. Den första landskapsbrickan utgör nu reservatets start.

## v0.2.9

- Tog bort alla kvarvarande hänvisningar till startfält/startbricka.
- Första brickan placeras fritt.
- Minst ett fält på den nyplacerade brickan måste ingå när ett djur kryssas.
- Standardiserade spelet till 8 turer per spelare.
- Använder 16/24/32 brickor vid 2/3/4 spelare.
- Lade till 8 balanserade brickor för fyraspelarläget.

## v0.3.0 – projektstädning och konsistenskontroll

- Rensade bort äldre landskaps- och referenskortsoutput.
- Synkade versionsnummer i regler och data.
- Skrev om README, projektstatus och produktionsguide.
- Ersatte referenskortets platshållarscript med en fungerande generator.
- Lade till automatisk projektvalidering.
- Tog bort ersatt textbaserat referenskort.
- Regenererade all aktuell SVG- och PDF-output från källorna.

## v0.3.1 – [SPELMOTORPLAN] steg 1–5

- Lade till dokumenterad spelmotorplan.
- Implementerade tvåspelarregelmotorn.
- Implementerade alla djurkrav och aktuell poängräkning.
- Lade till tre AI-profiler.
- Lade till reproducerbara seeds och full draglogg.
- Lade till automatiska tester.
- Kördes 250 verifierade balanserad-mot-balanserad-partier.

## v0.3.2 – sista fokuserade motoriteration

- Lade till växlande startspelare.
- Lade till profiljämförelser.
- Lade till fem regressionstester.
- Kördes 80 partier per profilpar.
- Lade till motoranalys och rekommendation att frysa motorn.

## v0.3.3 – fler­spelarstöd

- Generaliserade spelmotorn till 2–4 spelare.
- Lade till tester för tre och fyra spelare.
- Lade till roterande startspelare för fler spelare.
- Kördes 30 verifierade tre­spelarpartier och 30 verifierade fyr­spelarpartier.
- Lade till sittplats- och djurstatistik.

## v0.3.4 – GitHub Actions och print-release

- Införde `.github/workflows/` på samma nivå som `README.md`.
- Lade till Validate-workflow för projektvalidering och tester.
- Lade till Build Print Preview-workflow som publicerar ett samlat preview-artifact.
- Lade till Release Print Package-workflow för `v*`-taggar.
- Lade till `scripts/build_print.py`.
- Lade till `scripts/package_release.py`.
- Lade till `scripts/build_score_sheets.py`.
- Gjorde landskapsbyggaren versions- och datadriven.
- Utökade `scripts/validate_project.py` för CI.
- Lade till `requirements.txt` och dokumentation för lokalt/GitHub-bygge.
