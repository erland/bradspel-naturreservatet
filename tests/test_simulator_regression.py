import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.simulator.engine import (
    PlayerState, Placement, play_game, score_player
)

class RegressionTests(unittest.TestCase):
    def test_exactly_eight_turns_each(self):
        result = play_game(ROOT, 1001, ("balanced", "balanced"))
        counts = {p.name: 0 for p in result.players}
        for log in result.logs:
            counts[log.player] += 1
        self.assertEqual(counts["Spelare A"], 8)
        self.assertEqual(counts["Spelare B"], 8)

    def test_at_most_one_animal_per_turn(self):
        result = play_game(ROOT, 1002, ("balanced", "balanced"))
        for log in result.logs:
            self.assertIn(log.claimed_animal is None or isinstance(log.claimed_animal, str), [True])

    def test_no_duplicate_claims(self):
        result = play_game(ROOT, 1003, ("balanced", "balanced"))
        for player in result.players:
            self.assertEqual(len(player.claimed), len(set(player.claimed)))

    def test_bonus_scoring(self):
        player = PlayerState("Test")
        player.claimed = {"groda", "radjur", "baver", "trana"}
        player.board = {
            (0,0): "Skog", (1,0): "Skog", (2,0): "Skog", (3,0): "Skog",
            (0,1): "Sjö", (1,1): "Äng", (2,1): "Berg", (3,1): "Våtmark",
        }
        total, breakdown = score_player(player)
        self.assertEqual(breakdown["four_animals_bonus"], 3)
        self.assertEqual(breakdown["all_terrains_bonus"], 2)
        self.assertEqual(breakdown["area_bonus"], 1)
        self.assertEqual(total, breakdown["animal_score"] + 6)

    def test_start_player_can_switch(self):
        one = play_game(ROOT, 2222, ("balanced","balanced"), start_player_index=0)
        two = play_game(ROOT, 2222, ("balanced","balanced"), start_player_index=1)
        self.assertEqual(one.logs[0].player, "Spelare A")
        self.assertEqual(two.logs[0].player, "Spelare B")

if __name__ == "__main__":
    unittest.main()
