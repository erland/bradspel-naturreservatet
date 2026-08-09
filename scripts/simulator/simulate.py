from __future__ import annotations

from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import asdict
import argparse
import csv
import json
import statistics

from .engine import play_game

ROOT = Path(__file__).resolve().parents[2]

def run(games: int, seed: int, profiles: tuple[str, str]) -> dict:
    rows = []
    animal_counts = Counter()
    winners = Counter()
    ties = 0
    example = None

    for index in range(games):
        game_seed = seed + index
        result = play_game(ROOT, game_seed, profiles)
        if example is None:
            example = result

        a = result.scores["Spelare A"]
        b = result.scores["Spelare B"]
        if a == b:
            ties += 1
        elif a > b:
            winners["Spelare A"] += 1
        else:
            winners["Spelare B"] += 1

        for player in result.players:
            score = result.scores[player.name]
            breakdown = result.score_breakdown[player.name]
            for animal in player.claimed:
                animal_counts[animal] += 1
            rows.append({
                "game": index + 1,
                "seed": game_seed,
                "player": player.name,
                "profile": profiles[0] if player.name == "Spelare A" else profiles[1],
                "score": score,
                "animals": len(player.claimed),
                "animal_ids": ",".join(sorted(player.claimed)),
                "area_bonus": breakdown["area_bonus"],
                "width": breakdown["width"],
                "height": breakdown["height"],
                "density": round(breakdown["density"], 4),
            })

    scores = [r["score"] for r in rows]
    summary = {
        "games": games,
        "player_results": len(rows),
        "seed_start": seed,
        "profiles": list(profiles),
        "mean_score": statistics.mean(scores),
        "median_score": statistics.median(scores),
        "min_score": min(scores),
        "max_score": max(scores),
        "tie_rate": ties / games,
        "winner_counts": dict(winners),
        "animal_rates": {
            animal: count / len(rows)
            for animal, count in sorted(animal_counts.items())
        },
        "mean_animals": statistics.mean(r["animals"] for r in rows),
        "mean_density": statistics.mean(r["density"] for r in rows),
    }
    return {"summary": summary, "rows": rows, "example": example}

def save(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(
        json.dumps(result["summary"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with (output / "games.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=result["rows"][0].keys())
        writer.writeheader()
        writer.writerows(result["rows"])

    example = result["example"]
    example_data = {
        "seed": example.seed,
        "used_tile_ids": example.used_tile_ids,
        "scores": example.scores,
        "score_breakdown": example.score_breakdown,
        "turns": [asdict(log) for log in example.logs],
    }
    (output / "example-game.json").write_text(
        json.dumps(example_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    s = result["summary"]
    animal_lines = "\n".join(
        f"- {name}: {rate:.1%}" for name, rate in s["animal_rates"].items()
    )
    report = f"""# Simuleringsrapport

## Inställningar

- Partier: {s['games']}
- Profiler: {s['profiles'][0]} mot {s['profiles'][1]}
- Första seed: {s['seed_start']}
- Tvåspelarläge: 16 unika brickor, 8 turer per spelare

## Resultat

- Genomsnittspoäng: {s['mean_score']:.2f}
- Medianpoäng: {s['median_score']:.2f}
- Min/max: {s['min_score']} / {s['max_score']}
- Oavgjorda partier: {s['tie_rate']:.1%}
- Genomsnittligt antal djur: {s['mean_animals']:.2f}
- Genomsnittlig reservatstäthet: {s['mean_density']:.3f}

## Djurandelar

{animal_lines}

## Spårbarhet

`example-game.json` innehåller en fullständig draglogg med öppna brickor,
valda brick-ID:n, koordinater, djur och återstående hög.

Motorn kontrollerar efter varje parti att:

- exakt 16 brickor användes
- alla 16 ID:n var unika
- de använda ID:na exakt motsvarar tvåspelaruppsättningen

Resultaten är balanshypoteser, inte ersättning för fysiska speltester.
"""
    (output / "report.md").write_text(report, encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20260710)
    parser.add_argument("--profile-a", choices=["random", "greedy", "balanced"], default="balanced")
    parser.add_argument("--profile-b", choices=["random", "greedy", "balanced"], default="balanced")
    parser.add_argument("--output", type=Path, default=ROOT / "output/simulation")
    args = parser.parse_args()

    result = run(args.games, args.seed, (args.profile_a, args.profile_b))
    save(result, args.output)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
