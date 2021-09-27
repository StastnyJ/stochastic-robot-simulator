from enum import IntEnum
from typing import List, Tuple, Optional
import json

class SpotType(IntEnum):
    FREE_PLACE = 0
    WALL = 1
    TERMINAL = 2

class Instruction(IntEnum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

class VisualizationData:
    def __init__(self, colors: Optional[List[List[Optional[Tuple[int, int, int]]]]], texts: Optional[List[List[str]]]):
        self.colors = colors
        self.texts = texts

class SensorData:
    def __init__(self, up: bool, left: bool, right: bool, down: bool):
        self.up = up
        self.left = left
        self.right = right
        self.down = down

    def __str__(self):
        return str.join(";", [str(self.up), str(self.left), str(self.right), str(self.down)])

class Environment:
    def __init__(self, map: List[List[Tuple[SpotType, float]]], stepPenalty: float):
        self.map = map
        self.stepPenalty = stepPenalty

    def __str__(self):
        return str.join(';', [
            str(self.stepPenalty),
            str(len(self.map)),
            str(len(self.map[0])),
            str.join(',', [
                str.join(',', [
                   str(int(cell[0])) + ("" if int(cell[0]) < 2 else str(cell[1])) for cell in row
                ]) for row in self.map
            ])
        ])

    @staticmethod
    def build(rawMap: List[str], rewards: List[float], stepPenalty: float):
        res = []
        for row in rawMap:
            actRow = []
            for act in row:
                if act == "#":
                    actRow.append((SpotType.WALL,0))
                elif act == "T":
                    actRow.append((SpotType.TERMINAL, rewards.pop(0)))
                else:
                    actRow.append((SpotType.FREE_PLACE, 0))
            res.append(actRow)
            
        return Environment(res, stepPenalty)

    def toJson(self):
        return '{"map": ' + json.dumps(self.map) + ', "stepPenalty": ' + str(self.stepPenalty) + '}'
