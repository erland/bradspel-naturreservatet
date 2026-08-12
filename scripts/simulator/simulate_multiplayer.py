from __future__ import annotations

from pathlib import Path
from collections import Counter, defaultdict
import json
import statistics

from .engine import play_game

ROOT = Path(__file__).resolve().parents[2]

def run_player_count(player_count: int, games: int, seed: int) -> dict:
    profiles = tuple("balanced" for _ in range(player_count))
    seat_scores = defaultdict(list)
    seat_animals = defaultdict(list)
    seat_wins = Counter()
    start_wins = 0
    non_tie_games = 0
    ties = 0
    animal_counts = Counter()

    for i in range(games):
        start_index = i % player_count
        result = play_game(
            ROOT,
            seed + i,
            profiles,
            start_player_index=start_index,
        )

        max_score = max(result.scores.values())
        winners = [name for name, score in result.scores.items() if score == max_score]
        if len(winners) > 1:
            ties += 1
        else:
            non_tie_games += 1
            winner = winners[0]
            seat_wins[winner] += 1
            starting_player = f"Spelare {chr(65+start_index)}"
            if winner == starting_player:
                start_wins += 1

        for idx, player in enumerate(result.players):
            seat = player.name
            seat_scores[seat].append(result.scores[seat])
            seat_animals[seat].append(len(player.claimed))
            for animal in player.claimed:
                animal_counts[animal] += 1

    player_results = games * player_count
    return {
        "player_count": player_count,
        "games": games,
        "tie_rate": ties / games,
        "start_player_win_rate_non_ties": start_wins / non_tie_games if non_tie_games else None,
        "seat_win_counts": dict(seat_wins),
        "seat_mean_scores": {
            seat: statistics.mean(values) for seat, values in seat_scores.items()
        },
        "seat_mean_animals": {
            seat: statistics.mean(values) for seat, values in seat_animals.items()
        },
        "animal_rates": {
            animal: count / player_results
            for animal, count in sorted(animal_counts.items())
        },
        "overall_mean_score": statistics.mean(
            score for values in seat_scores.values() for score in values
        ),
        "overall_mean_animals": statistics.mean(
            n for values in seat_animals.values() for n in values
        ),
    }

if __name__ == "__main__":
    output = ROOT / "output/simulation-multiplayer"
    output.mkdir(parents=True, exist_ok=True)

    results = {
        "three_players": run_player_count(3, 30, 20260710),
        "four_players": run_player_count(4, 30, 20261710),
    }

    (output / "multiplayer-summary.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = ["# Fler­spelar­analys", ""]
    for key, data in results.items():
        lines += [
            f"## {key.replace('_', ' ')}",
            f"- Partier: {data['games']}",
            f"- Oavgjort: {data['tie_rate']:.1%}",
            f"- Startspelarvinst bland avgjorda: {data['start_player_win_rate_non_ties']:.1%}",
            f"- Genomsnittspoäng: {data['overall_mean_score']:.2f}",
            f"- Genomsnittligt antal djur: {data['overall_mean_animals']:.2f}",
            f"- Sittplatsers medelpoäng: {data['seat_mean_scores']}",
            f"- Sittplatsers medeldjur: {data['seat_mean_animals']}",
            "",
        ]

    (output / "multiplayer-report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(json.dumps(results, ensure_ascii=False, indent=2))
