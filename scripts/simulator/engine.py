from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional
import copy
import random
import yaml

Coord = tuple[int, int]
Board = dict[Coord, str]

DIRECTIONS: tuple[Coord, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
ANIMAL_POINTS = {
    "groda": 2,
    "radjur": 2,
    "baver": 4,
    "trana": 4,
    "lo": 5,
    "fiskgjuse": 6,
}

@dataclass(frozen=True)
class Tile:
    id: str
    a: str
    b: str

@dataclass(frozen=True)
class Placement:
    tile_id: str
    cells: tuple[tuple[Coord, str], tuple[Coord, str]]

    @property
    def coords(self) -> set[Coord]:
        return {self.cells[0][0], self.cells[1][0]}

@dataclass
class PlayerState:
    name: str
    board: Board = field(default_factory=dict)
    claimed: set[str] = field(default_factory=set)
    placements: list[Placement] = field(default_factory=list)

@dataclass
class TurnLog:
    turn_number: int
    player: str
    open_before: list[str]
    selected_tile: str
    placement: dict
    claimed_animal: Optional[str]
    open_after: list[str]
    deck_remaining: int

@dataclass
class GameResult:
    seed: int
    players: list[PlayerState]
    used_tile_ids: list[str]
    logs: list[TurnLog]
    scores: dict[str, int]
    score_breakdown: dict[str, dict]

def load_tiles(root: Path, set_name: str = "2_players") -> list[Tile]:
    data = yaml.safe_load((root / "data/tiles.yaml").read_text(encoding="utf-8"))
    by_id = {t["id"]: Tile(t["id"], t["a"], t["b"]) for t in data["tiles"]}
    ids = data["player_count_sets"][set_name]["tile_ids"]
    return [by_id[i] for i in ids]

def add(c1: Coord, c2: Coord) -> Coord:
    return c1[0] + c2[0], c1[1] + c2[1]

def neighbors(c: Coord) -> Iterable[Coord]:
    for d in DIRECTIONS:
        yield add(c, d)

def placements_for_tile(board: Board, tile: Tile) -> list[Placement]:
    seen: set[tuple] = set()
    result: list[Placement] = []

    if not board:
        # Translation is irrelevant for the first tile. Four rotations suffice.
        for d in DIRECTIONS:
            c1 = (0, 0)
            c2 = add(c1, d)
            key = ((c1, tile.a), (c2, tile.b))
            if key not in seen:
                seen.add(key)
                result.append(Placement(tile.id, key))
        return result

    frontier: set[Coord] = set()
    for occupied in board:
        for n in neighbors(occupied):
            if n not in board:
                frontier.add(n)

    for c1 in frontier:
        for d in DIRECTIONS:
            c2 = add(c1, d)
            if c2 in board:
                continue
            cells = ((c1, tile.a), (c2, tile.b))
            if not any(n in board for c, _ in cells for n in neighbors(c)):
                continue
            key = tuple(sorted(cells))
            if key not in seen:
                seen.add(key)
                result.append(Placement(tile.id, cells))

            # 180-degree rotation swaps which terrain occupies each coordinate.
            swapped = ((c1, tile.b), (c2, tile.a))
            key2 = tuple(sorted(swapped))
            if key2 not in seen:
                seen.add(key2)
                result.append(Placement(tile.id, swapped))
    return result

def apply_placement(board: Board, placement: Placement) -> Board:
    new_board = board.copy()
    for coord, terrain in placement.cells:
        if coord in new_board:
            raise ValueError(f"Overlap at {coord}")
        new_board[coord] = terrain
    return new_board

def _edge(board: Board, c1: Coord, c2: Coord, t1: str, t2: str) -> bool:
    return board.get(c1) == t1 and board.get(c2) == t2 and c2 in set(neighbors(c1))

def animal_witnesses(board: Board, animal: str) -> list[set[Coord]]:
    witnesses: list[set[Coord]] = []

    if animal == "groda":
        for c, t in board.items():
            if t == "Sjö":
                for n in neighbors(c):
                    if board.get(n) == "Våtmark":
                        witnesses.append({c, n})

    elif animal == "radjur":
        for c, t in board.items():
            if t == "Äng":
                for n in neighbors(c):
                    if board.get(n) == "Skog":
                        witnesses.append({c, n})

    elif animal == "baver":
        lakes = [c for c, t in board.items() if t == "Sjö"]
        for c in lakes:
            for n in neighbors(c):
                if board.get(n) != "Sjö":
                    continue
                pair = {c, n}
                if any(board.get(x) == "Skog" for lake in pair for x in neighbors(lake)):
                    forests = {
                        x for lake in pair for x in neighbors(lake)
                        if board.get(x) == "Skog"
                    }
                    for f in forests:
                        witnesses.append(pair | {f})

    elif animal == "trana":
        for c, t in board.items():
            if t != "Våtmark":
                continue
            meadows = [n for n in neighbors(c) if board.get(n) == "Äng"]
            lakes = [n for n in neighbors(c) if board.get(n) == "Sjö"]
            for m in meadows:
                for l in lakes:
                    witnesses.append({c, m, l})

    elif animal == "lo":
        for c, t in board.items():
            if t != "Berg":
                continue
            forests = [n for n in neighbors(c) if board.get(n) == "Skog"]
            for i in range(len(forests)):
                for j in range(i + 1, len(forests)):
                    witnesses.append({c, forests[i], forests[j]})

    elif animal == "fiskgjuse":
        for c, t in board.items():
            if t != "Sjö":
                continue
            adjacent = list(neighbors(c))
            if all(n in board for n in adjacent) and any(board[n] == "Skog" for n in adjacent):
                witnesses.append({c, *adjacent})
    else:
        raise KeyError(animal)

    return witnesses

def newly_claimable_animals(
    board: Board,
    claimed: set[str],
    new_coords: set[Coord],
) -> list[str]:
    result: list[str] = []
    for animal in ANIMAL_POINTS:
        if animal in claimed:
            continue
        if any(witness & new_coords for witness in animal_witnesses(board, animal)):
            result.append(animal)
    return result

def connected_regions(board: Board, terrain: str) -> list[set[Coord]]:
    remaining = {c for c, t in board.items() if t == terrain}
    regions: list[set[Coord]] = []
    while remaining:
        start = remaining.pop()
        region = {start}
        stack = [start]
        while stack:
            c = stack.pop()
            for n in neighbors(c):
                if n in remaining and board.get(n) == terrain:
                    remaining.remove(n)
                    region.add(n)
                    stack.append(n)
        regions.append(region)
    return regions

def score_player(player: PlayerState) -> tuple[int, dict]:
    animal_score = sum(ANIMAL_POINTS[a] for a in player.claimed)
    four_animals = 3 if len(player.claimed) >= 4 else 0
    all_terrains = 2 if len(set(player.board.values())) >= 5 else 0
    area_bonus = 0
    for terrain in {"Skog", "Sjö", "Äng", "Berg", "Våtmark"}:
        area_bonus += sum(1 for r in connected_regions(player.board, terrain) if len(r) >= 4)
    total = animal_score + four_animals + all_terrains + area_bonus
    return total, {
        "animal_score": animal_score,
        "four_animals_bonus": four_animals,
        "all_terrains_bonus": all_terrains,
        "area_bonus": area_bonus,
        "animals": sorted(player.claimed),
        "width": board_dimensions(player.board)[0],
        "height": board_dimensions(player.board)[1],
        "density": board_density(player.board),
    }

def board_dimensions(board: Board) -> tuple[int, int]:
    if not board:
        return 0, 0
    xs = [c[0] for c in board]
    ys = [c[1] for c in board]
    return max(xs)-min(xs)+1, max(ys)-min(ys)+1

def board_density(board: Board) -> float:
    w, h = board_dimensions(board)
    return len(board)/(w*h) if w and h else 0.0

def clone_player(player: PlayerState) -> PlayerState:
    return PlayerState(
        name=player.name,
        board=player.board.copy(),
        claimed=set(player.claimed),
        placements=list(player.placements),
    )

class AI:
    name = "base"

    def choose(
        self,
        player: PlayerState,
        open_tiles: list[Tile],
        rng: random.Random,
    ) -> tuple[Tile, Placement, Optional[str]]:
        raise NotImplementedError

class RandomAI(AI):
    name = "random"

    def choose(self, player, open_tiles, rng):
        moves = []
        for tile in open_tiles:
            for placement in placements_for_tile(player.board, tile):
                board = apply_placement(player.board, placement)
                claimable = newly_claimable_animals(board, player.claimed, placement.coords)
                choices = claimable or [None]
                for animal in choices:
                    moves.append((tile, placement, animal))
        if not moves:
            raise RuntimeError("No legal moves")
        return rng.choice(moves)

class GreedyAI(AI):
    name = "greedy"

    def choose(self, player, open_tiles, rng):
        scored = []
        for tile in open_tiles:
            for placement in placements_for_tile(player.board, tile):
                board = apply_placement(player.board, placement)
                claimable = newly_claimable_animals(board, player.claimed, placement.coords)
                animal = max(claimable, key=lambda a: ANIMAL_POINTS[a], default=None)
                temp = clone_player(player)
                temp.board = board
                if animal:
                    temp.claimed.add(animal)
                score, _ = score_player(temp)
                scored.append((score, rng.random(), tile, placement, animal))
        _, _, tile, placement, animal = max(scored)
        return tile, placement, animal

class BalancedAI(AI):
    name = "balanced"

    def choose(self, player, open_tiles, rng):
        scored = []
        for tile in open_tiles:
            for placement in placements_for_tile(player.board, tile):
                board = apply_placement(player.board, placement)
                claimable = newly_claimable_animals(board, player.claimed, placement.coords)
                claim_options = claimable or [None]
                for animal in claim_options:
                    temp = clone_player(player)
                    temp.board = board
                    if animal:
                        temp.claimed.add(animal)
                    immediate, breakdown = score_player(temp)

                    # Simple human-like one-step heuristic, not perfect play.
                    unclaimed = set(ANIMAL_POINTS) - temp.claimed
                    future = sum(
                        min(len(animal_witnesses(board, a)), 2) * 0.35
                        for a in unclaimed
                    )
                    terrain_variety = len(set(board.values())) * 0.18
                    compactness = board_density(board) * 1.25
                    width, height = board_dimensions(board)
                    extreme_shape_penalty = max(0, max(width, height)-6) * 0.25

                    value = (
                        immediate
                        + future
                        + terrain_variety
                        + compactness
                        - extreme_shape_penalty
                    )
                    scored.append((value, rng.random(), tile, placement, animal))
        _, _, tile, placement, animal = max(scored)
        return tile, placement, animal

AI_TYPES = {
    "random": RandomAI,
    "greedy": GreedyAI,
    "balanced": BalancedAI,
}

def play_game(
    root: Path,
    seed: int,
    profiles: tuple[str, ...] = ("balanced", "balanced"),
    start_player_index: int = 0,
) -> GameResult:
    player_count = len(profiles)
    if player_count not in (2, 3, 4):
        raise ValueError("Naturreservatet supports 2-4 players")

    set_name = f"{player_count}_players"
    rng = random.Random(seed)
    deck = load_tiles(root, set_name)

    if len({t.id for t in deck}) != len(deck):
        raise ValueError(f"Duplicate tile IDs in {set_name} set")

    rng.shuffle(deck)
    open_tiles = [deck.pop() for _ in range(4)]

    players = [PlayerState(f"Spelare {chr(65+i)}") for i in range(player_count)]
    ais = [AI_TYPES[p]() for p in profiles]
    logs: list[TurnLog] = []
    used: list[str] = []

    total_turns = player_count * 8
    for turn in range(total_turns):
        idx = (turn + start_player_index) % player_count
        player = players[idx]
        ai = ais[idx]
        open_before = [t.id for t in open_tiles]
        tile, placement, animal = ai.choose(player, open_tiles, rng)

        if tile.id in used:
            raise AssertionError(f"Tile reused: {tile.id}")

        player.board = apply_placement(player.board, placement)
        player.placements.append(placement)
        if animal:
            player.claimed.add(animal)

        used.append(tile.id)
        open_tiles = [t for t in open_tiles if t.id != tile.id]
        if deck:
            open_tiles.append(deck.pop())

        logs.append(TurnLog(
            turn_number=turn + 1,
            player=player.name,
            open_before=open_before,
            selected_tile=tile.id,
            placement={
                "cells": [
                    {"x": c[0], "y": c[1], "terrain": terrain}
                    for c, terrain in placement.cells
                ]
            },
            claimed_animal=animal,
            open_after=[t.id for t in open_tiles],
            deck_remaining=len(deck),
        ))

    expected = {t.id for t in load_tiles(root, set_name)}
    expected_count = player_count * 8
    if len(used) != expected_count or len(set(used)) != expected_count or set(used) != expected:
        raise AssertionError("Unique tile invariant failed")

    scores = {}
    breakdowns = {}
    for player in players:
        scores[player.name], breakdowns[player.name] = score_player(player)

    return GameResult(
        seed=seed,
        players=players,
        used_tile_ids=used,
        logs=logs,
        scores=scores,
        score_breakdown=breakdowns,
    )
