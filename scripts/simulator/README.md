# Naturreservatets spelmotor

Kör tester:

```bash
python -m unittest discover -s tests -v
```

Kör simulering:

```bash
python -m scripts.simulator.simulate   --games 250   --seed 20260710   --profile-a balanced   --profile-b balanced
```

Profiler:

- `random`
- `greedy`
- `balanced`

Output:

- `output/simulation/summary.json`
- `output/simulation/games.csv`
- `output/simulation/example-game.json`
- `output/simulation/report.md`

Varje parti verifierar att de 16 tvåspelarbrickorna används exakt en gång.
