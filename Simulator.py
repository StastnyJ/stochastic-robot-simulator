from Environment import Environment, Instruction, SensorData, SpotType
from random import Random
from typing import Tuple, Optional


class Simulator:
    def __init__(self, environment: Environment, position: Tuple[int, int],
                 wrongActionProbability: float, falseWallProbability: float, 
                 falseFreeProbability: float, seed: int):

        self._env = environment
        self._pos = position
        self._score = 0

        self._wrongActionProb = wrongActionProbability
        self._falseWallProb = falseWallProbability
        self._falseFreeProb = falseFreeProbability

        self._rnd = Random(seed)
        self._terminated = False

    def _getTrueWithProb(self, trueProb: float) -> float:
        return self._rnd.random() < trueProb

    def _isWall(self, pos: Tuple[int, int]) -> bool:
        row, col = pos
        return self._env.map[row][col][0] == SpotType.WALL

    def getSensorValues(self) -> SensorData:
        upRes = self._getTrueWithProb(1 - self._falseWallProb) if self._isWall((self._pos[0] - 1, self._pos[1])) else self._getTrueWithProb(self._falseFreeProb)
        leftRes = self._getTrueWithProb(1 - self._falseWallProb) if self._isWall((self._pos[0], self._pos[1] - 1)) else self._getTrueWithProb(self._falseFreeProb)
        rightRes = self._getTrueWithProb(1 - self._falseWallProb) if self._isWall((self._pos[0], self._pos[1] + 1)) else self._getTrueWithProb(self._falseFreeProb)
        downRes = self._getTrueWithProb(1 - self._falseWallProb) if self._isWall((self._pos[0] + 1, self._pos[1])) else self._getTrueWithProb(self._falseFreeProb)

        return SensorData(upRes, leftRes, rightRes, downRes)

    @staticmethod
    def _leftInstruction(instruction: Instruction) -> Instruction:
        if instruction == Instruction.LEFT:
            return Instruction.DOWN
        if instruction == Instruction.DOWN:
            return Instruction.RIGHT
        if instruction == Instruction.RIGHT:
            return Instruction.UP
        if instruction == Instruction.UP:
            return Instruction.LEFT

    @staticmethod
    def _rightInstruction(instruction: Instruction) -> Instruction:
        return Simulator._leftInstruction(Simulator._leftInstruction(Simulator._leftInstruction(instruction)))

    def _makeDeterministicInstruction(self, instruction: Instruction) -> Tuple[int, int]:
        prevPos = self._pos
        if instruction == Instruction.UP:
            self._pos = (self._pos[0] - 1, self._pos[1])
        if instruction == Instruction.LEFT:
            self._pos = (self._pos[0], self._pos[1] - 1)
        if instruction == Instruction.RIGHT:
            self._pos = (self._pos[0], self._pos[1] + 1)
        if instruction == Instruction.DOWN:
            self._pos = (self._pos[0] + 1, self._pos[1])

        self._score -= self._env.stepPenalty
        posType, posScore = self._env.map[self._pos[0]][self._pos[1]]
        if posType == SpotType.TERMINAL:
            self._score += posScore
            self._terminated = True
        if posType == SpotType.WALL:
            self._pos = prevPos
        return self._pos

    def makeInstruction(self, instruction: Instruction) -> Tuple[Tuple[int, int], Instruction]:
        if self._terminated:
            return self._pos
        rand = self._rnd.random()
        instr = instruction
        if rand < self._wrongActionProb:
            instr = Simulator._leftInstruction(instruction)
        elif rand < 2 * self._wrongActionProb:
            instr = Simulator._rightInstruction(instruction)
        return (self._makeDeterministicInstruction(instr), instr)

    def isTerminated(self) -> bool:
        return self._terminated

    def getScore(self) -> float:
        return self._score
