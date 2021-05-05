from Environment import Environment, SensorData, Instruction, VisualizationData, SpotType
from typing import Tuple, Union, Optional
from math import inf
import numpy as np

def getLeftInstruction(instruction: Instruction) -> Instruction:
    if instruction == Instruction.LEFT:
        return Instruction.DOWN
    if instruction == Instruction.DOWN:
        return Instruction.RIGHT
    if instruction == Instruction.RIGHT:
        return Instruction.UP
    if instruction == Instruction.UP:
        return Instruction.LEFT

def getRightInstruction(instruction: Instruction) -> Instruction:
    return getLeftInstruction(getLeftInstruction(getLeftInstruction(instruction)))

def getDeterministicUtility(pos, instruction, eus) -> float:
    row,col = pos
    if instruction == Instruction.UP:
        row -= 1
    if instruction == Instruction.LEFT:
        col -= 1
    if instruction == Instruction.RIGHT:
        col += 1
    if instruction == Instruction.DOWN:
        row += 1
    if eus[row][col] == -inf:
        row,col = pos
    return eus[row][col]

def getExpectedUtility(pos, instruction, eus) -> float:
    return  0.8 * getDeterministicUtility(pos, instruction, eus) + \
            0.1 * getDeterministicUtility(pos, getLeftInstruction(instruction), eus) + \
            0.1 * getDeterministicUtility(pos, getRightInstruction(instruction), eus)

def bellmanUpdate(lastEus, noUpdate, stepPenalty, instructions):
    new = [[-inf] * len(row) for row in lastEus]
    for i in range(1, len(new) - 1):
        for j in range(1, len(new[i]) - 1):
            new[i][j] = lastEus[i][j] if noUpdate[i][j] else max([getExpectedUtility((i,j), inst, lastEus) for inst in instructions]) - stepPenalty
    return new

def getBestInstruction(position: Tuple[int, int], eus, instructions) -> Instruction:
    bestEU = -inf
    bestInstruction = None
    for instr in instructions:
        actEU = getExpectedUtility(position, instr, eus)
        if actEU > bestEU:
            bestEU = actEU
            bestInstruction = instr
    return bestInstruction

def printNumMatrix(arr, prec):
    for row in arr[1:-1]:
        for cell in row[1:-1]:
            if len(cell) > 0:
                print(str(round(float(cell), prec))[::-1].zfill(prec + 3)[::-1], end=" ")
            else:
                print(" " * (prec + 3), end=" ")
        print()

def buildTransitionMatrix(map, instruction):
    return np.array([[0]])

def buildObservationMatrix(map, observation):
    return np.array([[0]])

def getInitialProbabilitiesMatrix(map, observation):
    return np.array([[0]])

def normalizeMatrix(matrix):
    return matrix

def getBestInstruction(positionProbabilities, eus):
    return Instruction.UP


class Solution:
    def __init__(self, environment: Environment):
        self._environment = environment
        self._instructions = [Instruction.UP, Instruction.LEFT, Instruction.RIGHT, Instruction.DOWN]

        self._transitionMatrixUp = buildTransitionMatrix(environment.map, Instruction.UP)
        self._transitionMatrixLeft = buildTransitionMatrix(environment.map, Instruction.LEFT)
        self._transitionMatrixRight = buildTransitionMatrix(environment.map, Instruction.RIGHT)
        self._transitionMatrixDown = buildTransitionMatrix(environment.map, Instruction.DOWN)

        self._positionProbabilities = None
        self._lastInstruction = None

        self._expectedUtilities = [[0 if cellType == SpotType.FREE_PLACE else (-inf if cellType == SpotType.WALL else cellVal) for (cellType, cellVal) in row] for row in environment.map]
        euNoUpdate = [[False if cellType == SpotType.FREE_PLACE else True for (cellType, cellVal) in row] for row in environment.map]
        for _ in range(10000):
            self._expectedUtilities = bellmanUpdate(self._expectedUtilities, euNoUpdate, self._environment.stepPenalty, self._instructions)
        self._euStr = [["" if self._expectedUtilities[row][cell] == -inf else str(round(self._expectedUtilities[row][cell], 4)) + "\n" + (getBestInstruction((row, cell),self._expectedUtilities, self._instructions).name if not euNoUpdate[row][cell] else "") for cell in range(len(self._expectedUtilities[row]))] for row in range(len(self._expectedUtilities))]

    def getInstruction(self, sensorsData: SensorData) -> Union[Instruction, Tuple[Instruction, Optional[VisualizationData]]]:
        if self._lastInstruction is None:
            self._positionProbabilities = getInitialProbabilitiesMatrix(self._environment.map, sensorsData)
        else:
            if self._lastInstruction == Instruction.UP:
                tm = self._transitionMatrixUp
            elif self._lastInstruction == Instruction.LEFT:
                tm = self._transitionMatrixLeft
            elif self._lastInstruction == Instruction.RIGHT:
                tm = self._transitionMatrixRight
            else:
                tm = self._transitionMatrixDown
            observationMatrix = buildObservationMatrix(self._environment.map, sensorsData)
            self._positionProbabilities = normalizeMatrix(np.matmul(observationMatrix, np.matmul(tm, self._positionProbabilities)))
        res = getBestInstruction(self._positionProbabilities)
        self._lastInstruction = res
        return (res, VisualizationData([[(0,0,255) if cell[0] == SpotType.FREE_PLACE else (255,0,0) for cell in row] for row in self._environment.map], self._euStr))

    def getInstructionGPS(self, position: Tuple[int, int]) ->  Union[Instruction, Tuple[Instruction, Optional[VisualizationData]]]:
        return (getBestInstruction(position, self._expectedUtilities, self._instructions), VisualizationData(None, self._euStr))