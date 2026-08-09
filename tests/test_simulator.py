import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.simulator.engine import (
    Tile, Placement, PlayerState, apply_placement, animal_witnesses,
    newly_claimable_animals, placements_for_tile, play_game, score_player
)

class EngineTests(unittest.TestCase):
    def test_first_tile_has_rotations(self):
        moves = placements_for_tile({}, Tile("T", "Skog", "Sjö"))
        self.assertEqual(len(moves), 4)

    def test_overlap_rejected(self):
        board = {(0,0): "Skog"}
        p = Placement("T", (((0,0),"Sjö"),((1,0),"Äng")))
        with self.assertRaises(ValueError):
            apply_placement(board, p)

    def test_groda_requires_new_tile_in_witness(self):
        board = {(0,0): "Sjö", (1,0): "Våtmark", (5,5): "Skog"}
        claimable = newly_claimable_animals(board, set(), {(5,5)})
        self.assertNotIn("groda", claimable)
        claimable = newly_claimable_animals(board, set(), {(1,0)})
        self.assertIn("groda", claimable)

    def test_all_animals_true_examples(self):
        examples = {
            "groda": {(0,0):"Sjö",(1,0):"Våtmark"},
            "radjur": {(0,0):"Äng",(1,0):"Skog"},
            "baver": {(0,0):"Sjö",(1,0):"Sjö",(1,1):"Skog"},
            "trana": {(0,0):"Våtmark",(1,0):"Äng",(0,1):"Sjö"},
            "lo": {(0,0):"Berg",(1,0):"Skog",(-1,0):"Skog"},
            "fiskgjuse": {
                (0,0):"Sjö",(1,0):"Skog",(-1,0):"Äng",
                (0,1):"Berg",(0,-1):"Våtmark"
            },
        }
        for animal, board in examples.items():
            with self.subTest(animal=animal):
                self.assertTrue(animal_witnesses(board, animal))

    def test_unique_tiles_full_game(self):
        result = play_game(ROOT, 12345, ("balanced","balanced"))
        self.assertEqual(len(result.used_tile_ids), 16)
        self.assertEqual(len(set(result.used_tile_ids)), 16)

    def test_reproducible_seed(self):
        one = play_game(ROOT, 999, ("greedy","balanced"))
        two = play_game(ROOT, 999, ("greedy","balanced"))
        self.assertEqual(one.used_tile_ids, two.used_tile_ids)
        self.assertEqual(one.scores, two.scores)
        self.assertEqual(
            [l.selected_tile for l in one.logs],
            [l.selected_tile for l in two.logs],
        )

if __name__ == "__main__":
    unittest.main()
