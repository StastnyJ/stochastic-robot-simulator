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

def buildTransitionMatrix(map, instruction):
    tmSize = len(map) * len(map[0])
    res = []
    for i in range(tmSize):
        actTMRow = [0.0] * tmSize
        actMapRow = i // len(map[0])
        actMapCol = i % len(map[0])

        if map[actMapRow][actMapCol][0] == SpotType.FREE_PLACE:
            if instruction == Instruction.UP:
                if map[actMapRow + 1][actMapCol][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow + 1) * len(map[0]) + actMapCol] += 0.8
                if map[actMapRow][actMapCol + 1][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol + 1] += 0.1
                if map[actMapRow][actMapCol - 1][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol - 1] += 0.1

                if map[actMapRow - 1][actMapCol][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.8
                if map[actMapRow][actMapCol + 1][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1
                if map[actMapRow][actMapCol - 1][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1            
             
            if instruction == Instruction.LEFT:
                if map[actMapRow ][actMapCol + 1][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow ) * len(map[0]) + actMapCol + 1] += 0.8
                if map[actMapRow - 1][actMapCol][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow - 1) * len(map[0]) + actMapCol] += 0.1
                if map[actMapRow + 1][actMapCol][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow + 1) * len(map[0]) + actMapCol] += 0.1

                if map[actMapRow][actMapCol - 1][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.8
                if map[actMapRow - 1][actMapCol][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1
                if map[actMapRow + 1][actMapCol][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1        
                    
            if instruction == Instruction.RIGHT:
                if map[actMapRow][actMapCol - 1][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow ) * len(map[0]) + actMapCol - 1] += 0.8
                if map[actMapRow - 1][actMapCol][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow - 1) * len(map[0]) + actMapCol] += 0.1
                if map[actMapRow + 1][actMapCol][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow + 1) * len(map[0]) + actMapCol] += 0.1

                if map[actMapRow][actMapCol + 1][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.8
                if map[actMapRow - 1][actMapCol][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1
                if map[actMapRow + 1][actMapCol][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1      
                    
            if instruction == Instruction.DOWN:
                if map[actMapRow - 1][actMapCol][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow - 1) * len(map[0]) + actMapCol] += 0.8
                if map[actMapRow][actMapCol + 1][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol + 1] += 0.1
                if map[actMapRow][actMapCol - 1][0] == SpotType.FREE_PLACE:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol - 1] += 0.1

                if map[actMapRow + 1][actMapCol][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.8
                if map[actMapRow][actMapCol + 1][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1
                if map[actMapRow][actMapCol - 1][0] == SpotType.WALL:
                    actTMRow[(actMapRow) * len(map[0]) + actMapCol] += 0.1      
        res.append(actTMRow[:])

    return np.array(res)

def buildObservationMatrix(map, observation):
    tmSize = len(map) * len(map[0])
    res = []
    for i in range(tmSize):
        actOMRow = [0.0] * tmSize
        row = i // len(map[0])
        col = i % len(map[0])

        if map[row][col][0] == SpotType.FREE_PLACE:
            falseWalls = 0
            falseFrees = 0

            if observation.up and map[row - 1][col] [0]!= SpotType.WALL:
                falseWalls += 1
            if not observation.up and map[row - 1][col][0] == SpotType.WALL:
                falseWalls += 1
            if observation.left and map[row][col - 1][0] != SpotType.WALL:
                falseWalls += 1
            if not observation.left and map[row][col - 1][0] == SpotType.WALL:
                falseWalls += 1
            if observation.right and map[row][col + 1][0] != SpotType.WALL:
                falseWalls += 1
            if not observation.right and map[row][col + 1][0] == SpotType.WALL:
                falseWalls += 1
            if observation.down and map[row + 1][col][0] != SpotType.WALL:
                falseWalls += 1
            if not observation.down and map[row + 1][col][0] == SpotType.WALL:
                falseWalls += 1

            trueWals = 4 - falseWalls
            trueFrees = 4 - falseFrees
            actOMRow[i] = 0.8 * trueWals + 0.2 * falseWalls + 0.9 * trueFrees + 0.1 * falseFrees
        res.append(actOMRow)
    return np.array(res)

def getInitialProbabilities(map, observation):
    return normalize(np.matmul(buildObservationMatrix(map, observation), np.array([[1.0] for _ in range(len(map) * len(map[0]))])))

def normalize(matrix):
    return matrix / sum(matrix)

def getExpectedTotalUtility(positionProbabilities, eus, instruction, mapWidth):
    res = 0
    for i, prob in enumerate(positionProbabilities):
        if prob > 0.05:
            res += prob * getExpectedUtility((i // mapWidth, i % mapWidth), instruction, eus)
    return res

def getBestTotalInstruction(positionProbabilities, eus, instructions, mapWidth):
    bestUtility = -inf
    bestInstruction = None
    for instr in instructions:
        actUtility = getExpectedTotalUtility(positionProbabilities, eus, instr, mapWidth)
        if actUtility > bestUtility:
            bestUtility = actUtility
            bestInstruction = instr
    return bestInstruction



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
        for _ in range(1000):
            self._expectedUtilities = bellmanUpdate(self._expectedUtilities, euNoUpdate, self._environment.stepPenalty, self._instructions)
        self._euStr = [["" if self._expectedUtilities[row][cell] == -inf else str(round(self._expectedUtilities[row][cell], 4)) + "\n" + (getBestInstruction((row, cell),self._expectedUtilities, self._instructions).name if not euNoUpdate[row][cell] else "") for cell in range(len(self._expectedUtilities[row]))] for row in range(len(self._expectedUtilities))]

    def getInstruction(self, sensorsData: SensorData) -> Union[Instruction, Tuple[Instruction, Optional[VisualizationData]]]:
        if self._lastInstruction is None:
            self._positionProbabilities = getInitialProbabilities(self._environment.map, sensorsData)
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
            self._positionProbabilities = normalize(np.matmul(observationMatrix, np.matmul(tm, self._positionProbabilities)))
        res = getBestTotalInstruction(self._positionProbabilities, self._expectedUtilities, self._instructions, len(self._environment.map[0]))
        self._lastInstruction = res
        return (
            res,
            VisualizationData(
                [
                    [
                        (int(255.0 * (1 - self._positionProbabilities[row * len(self._environment.map[0]) + col])),int(255.0 * (1 - self._positionProbabilities[row * len(self._environment.map[0]) + col])),255) if self._environment.map[row][col][0] == SpotType.FREE_PLACE else (255,0,0) 
                            for col in range(len(self._environment.map[row]))
                        ]
                    for row in range(len(self._environment.map))
                ],
                self._euStr
            )
        )

    def getInstructionGPS(self, position: Tuple[int, int]) ->  Union[Instruction, Tuple[Instruction, Optional[VisualizationData]]]:
        return (getBestInstruction(position, self._expectedUtilities, self._instructions), VisualizationData(None, self._euStr))