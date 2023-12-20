from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Deque, Iterator


class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0

    @property
    def is_horizontal(self) -> bool:
        return self.value[1] == 0

    @property
    def is_vertical(self) -> bool:
        return self.value[0] == 0

    def reflect_diagonally(self, *, reverted: bool = False) -> 'Direction':
        if reverted:
            return DIRECTIONS_BY_VECTOR[-1 * self.value[1], -1 * self.value[0]]
        else:
            return DIRECTIONS_BY_VECTOR[self.value[1], self.value[0]]


DIRECTIONS_BY_VECTOR = {direction.value: direction for direction in Direction}


class TileType(Enum):
    EMPTY_SPACE = '.'
    MIRROR = '\\'
    REVERSE_MIRROR = '/'
    VERTICAL_SPLITTER = '|'
    HORIZONTAL_SPLITTER = '-'

    def get_outgoing_directions(self, entry_direction: Direction) -> Iterator['Direction']:
        if self == TileType.EMPTY_SPACE:
            yield entry_direction
        elif self in {TileType.MIRROR, TileType.REVERSE_MIRROR}:
            yield entry_direction.reflect_diagonally(reverted=self == TileType.REVERSE_MIRROR)
        elif self in {TileType.HORIZONTAL_SPLITTER, TileType.VERTICAL_SPLITTER}:
            if entry_direction.is_horizontal == (self == TileType.HORIZONTAL_SPLITTER):
                yield entry_direction
            else:
                yield entry_direction.reflect_diagonally()
                yield entry_direction.reflect_diagonally(reverted=True)


TILE_BY_SYMBOL = {tile.value: tile for tile in TileType}


@dataclass
class Tile:
    type: TileType

    energized: bool = False

    # directional vectors of beams previously emitted from this tile
    previous_entry_directions: set[Direction] = field(default_factory=set)


@dataclass
class Grid:
    tiles: list[list[Tile]]

    width: int
    height: int

    scheduled_beams: Deque[tuple[int, int, Direction]]  # tile coordinates + entry direction

    def __init__(self, tile_contents: list[list[TileType]]):
        self.tiles = [[Tile(tile_type) for tile_type in row] for row in tile_contents]

        self.height = len(self.tiles)

        widths = {len(row) for row in self.tiles}
        self.width = next(iter(widths), None)

        if self.height == 0 or self.width == 0 or len(widths) != 1:
            raise ValueError("Malformed grid")

        self.scheduled_beams = deque()

    @classmethod
    def parse(cls, raw_grid: str) -> 'Grid':
        return cls([
            [TILE_BY_SYMBOL[symbol] for symbol in line.strip()]
            for line in raw_grid.strip().splitlines()
        ])

    def render_grid(self) -> str:
        return "\n".join("".join(tile.type.value for tile in row) for row in self.tiles)

    def render_energization_grid(self) -> str:
        return "\n".join("".join("#" if tile.energized else "." for tile in row) for row in self.tiles)

    def run_scheduled_beams(self) -> None:
        while self.scheduled_beams:
            x, y, entry_direction = self.scheduled_beams.popleft()

            if not 0 <= x < self.width or not 0 <= y < self.height:
                # Skip beams that run off the grid
                continue

            tile = self.tiles[y][x]

            if entry_direction in tile.previous_entry_directions:
                # Skip beams if the current tile has already been entered by a beam from the same direction
                continue

            tile.energized = True
            tile.previous_entry_directions.add(entry_direction)

            for outgoing_direction in tile.type.get_outgoing_directions(entry_direction=entry_direction):
                self.scheduled_beams.append((
                    x + outgoing_direction.value[0],
                    y + outgoing_direction.value[1],
                    outgoing_direction,
                ))

    def send_beam(self, x: int, y: int, direction: Direction) -> None:
        self.scheduled_beams.append((x, y, direction))
        self.run_scheduled_beams()

    def get_energized_tile_count(self) -> int:
        return sum(1 for row in self.tiles for status in row if status.energized)

    def reset(self) -> None:
        for row in self.tiles:
            for tile in row:
                tile.energized = False
                tile.previous_entry_directions = set()


def get_part1_solution(raw_grid: str) -> int:
    grid = Grid.parse(raw_grid)
    grid.send_beam(0, 0, Direction.RIGHT)
    return grid.get_energized_tile_count()


def get_part2_solution(raw_grid: str) -> int:
    grid = Grid.parse(raw_grid)

    scores = []

    for y in range(grid.height):
        grid.send_beam(0, y, Direction.RIGHT)
        scores.append(grid.get_energized_tile_count())
        grid.reset()

        grid.send_beam(grid.width - 1, y, Direction.LEFT)
        scores.append(grid.get_energized_tile_count())
        grid.reset()

    for x in range(grid.width):
        grid.send_beam(x, 0, Direction.DOWN)
        scores.append(grid.get_energized_tile_count())
        grid.reset()

        grid.send_beam(x, grid.height - 1, Direction.UP)
        scores.append(grid.get_energized_tile_count())
        grid.reset()

    return max(scores)
