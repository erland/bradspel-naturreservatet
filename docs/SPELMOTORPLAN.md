# [SPELMOTORPLAN]

## Syfte

Bygg en reproducerbar spelmotor för Naturreservatet som kan verifiera regler,
köra AI-spelare och sammanställa balanshypoteser utan att ersätta fysiska speltester.

## Steg 1 – Regelmotor

- Läs brickor och spelaruppsättningar från YAML.
- Blanda unika brick-ID:n.
- Hantera fyra öppna brickor.
- Rotera och placera dominobrickor på koordinatnät.
- Förhindra överlapp.
- Kräv anslutning efter första brickan.
- Ge exakt åtta turer per spelare.

## Steg 2 – Djur och poäng

- Implementera alla sex djurkrav.
- Kräv att den nyplacerade brickan ingår i livsmiljön.
- Tillåt högst ett nytt djur per tur.
- Beräkna djurpoäng och bonuspoäng.

## Steg 3 – AI-profiler

- Slumpmässig AI.
- Kortsiktig AI.
- Balanserad AI med enkel ett-dragsvärdering.

## Steg 4 – Simulering

- Kör många reproducerbara partier.
- Mät djur, poäng, turordning, brickval och reservatsform.

## Steg 5 – Spårbarhet

- Seed för varje parti.
- Full draglogg.
- Kontroll att varje fysisk bricka används högst en gång.

## Steg 6 – Projektintegration

- Simulator i `scripts/simulator/`.
- Automatiska tester i `tests/`.
- Profiler i `data/simulation-profiles.yaml`.
- Rapporter i `output/simulation/`.

## Status

Första tvåspelarversionen implementeras i v0.3.1.
