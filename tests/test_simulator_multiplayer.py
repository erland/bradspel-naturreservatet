import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.simulator.engine import play_game

class MultiplayerTests(unittest.TestCase):
    def test_three_players_eight_turns_each_and_unique_tiles(self):
        result = play_game(ROOT, 3001, ("balanced","balanced","balanced"))
        counts = {p.name: 0 for p in result.players}
        for log in result.logs:
            counts[log.player] += 1
        self.assertEqual(counts, {"Spelare A":8,"Spelare B":8,"Spelare C":8})
        self.assertEqual(len(result.used_tile_ids), 24)
        self.assertEqual(len(set(result.used_tile_ids)), 24)

    def test_four_players_eight_turns_each_and_unique_tiles(self):
        result = play_game(
            ROOT, 4001,
            ("balanced","balanced","balanced","balanced")
        )
        counts = {p.name: 0 for p in result.players}
        for log in result.logs:
            counts[log.player] += 1
        self.assertEqual(
            counts,
            {"Spelare A":8,"Spelare B":8,"Spelare C":8,"Spelare D":8}
        )
        self.assertEqual(len(result.used_tile_ids), 32)
        self.assertEqual(len(set(result.used_tile_ids)), 32)

    def test_rotating_start_player_three_players(self):
        result = play_game(
            ROOT, 3002,
            ("balanced","balanced","balanced"),
            start_player_index=2
        )
        self.assertEqual(result.logs[0].player, "Spelare C")

    def test_rotating_start_player_four_players(self):
        result = play_game(
            ROOT, 4002,
            ("balanced","balanced","balanced","balanced"),
            start_player_index=3
        )
        self.assertEqual(result.logs[0].player, "Spelare D")

if __name__ == "__main__":
    unittest.main()
