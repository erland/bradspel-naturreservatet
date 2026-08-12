from __future__ import annotations

from pathlib import Path
from collections import Counter
import json
import statistics

from .engine import play_game

ROOT = Path(__file__).resolve().parents[2]

PROFILE_PAIRS = [
    ("balanced", "balanced"),
    ("greedy", "balanced"),
    ("balanced", "greedy"),
    ("random", "balanced"),
    ("balanced", "random"),
]

def run_batch(games: int = 300, seed: int = 20260710) -> dict:
    results = {}
    for profiles in PROFILE_PAIRS:
        rows = []
        winners = Counter()
        ties = 0
        for i in range(games):
            # Alternate physical start player each game.
            start_index = i % 2
            result = play_game(
                ROOT,
                seed + i,
                profiles,
                start_player_index=start_index,
            )
            scores = result.scores
            a = scores["Spelare A"]
            b = scores["Spelare B"]
            if a == b:
                ties += 1
            elif a > b:
                winners["Spelare A"] += 1
            else:
                winners["Spelare B"] += 1

            rows.append({
                "seed": seed + i,
                "start_player": "Spelare A" if start_index == 0 else "Spelare B",
                "score_a": a,
                "score_b": b,
                "animals_a": len(result.players[0].claimed),
                "animals_b": len(result.players[1].claimed),
            })

        start_wins = 0
        non_tie = 0
        for row in rows:
            if row["score_a"] == row["score_b"]:
                continue
            non_tie += 1
            winner = "Spelare A" if row["score_a"] > row["score_b"] else "Spelare B"
            if winner == row["start_player"]:
                start_wins += 1

        key = f"{profiles[0]}_vs_{profiles[1]}"
        results[key] = {
            "games": games,
            "profiles": list(profiles),
            "ties": ties,
            "tie_rate": ties / games,
            "winner_counts": dict(winners),
            "start_player_win_rate_non_ties": start_wins / non_tie if non_tie else None,
            "mean_score_a": statistics.mean(r["score_a"] for r in rows),
            "mean_score_b": statistics.mean(r["score_b"] for r in rows),
            "mean_animals_a": statistics.mean(r["animals_a"] for r in rows),
            "mean_animals_b": statistics.mean(r["animals_b"] for r in rows),
        }
    return results

if __name__ == "__main__":
    output = ROOT / "output/simulation-turordning"
    output.mkdir(parents=True, exist_ok=True)
    results = run_batch()
    (output / "profile-comparison.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = ["# Profil- och turordningsanalys", ""]
    for key, data in results.items():
        lines.extend([
            f"## {key}",
            f"- Partier: {data['games']}",
            f"- Oavgjort: {data['tie_rate']:.1%}",
            f"- Startspelarvinst bland icke-oavgjorda: {data['start_player_win_rate_non_ties']:.1%}",
            f"- Medelpoäng A/B: {data['mean_score_a']:.2f} / {data['mean_score_b']:.2f}",
            f"- Medeldjur A/B: {data['mean_animals_a']:.2f} / {data['mean_animals_b']:.2f}",
            "",
        ])
    (output / "profile-comparison.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
