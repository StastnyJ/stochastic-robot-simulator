from Environment import Environment, SensorData, Instruction, VisualizationData
from typing import Tuple, Union, Optional

class Solution:
    # Implement this if you want to do some precalculations
    def __init__(self, environment: Environment):
        self._environment = environment

    # Implement this function if you want to solve the second easier variation or the complete task
    def getInstruction(self, sensorsData: SensorData) -> Union[Instruction, Tuple[Instruction, Optional[VisualizationData]]]:
        return Instruction.UP

    # Implement this function if you want to solve only first easier variation of the task
    def getInstructionGPS(self, position: Tuple[int, int]) ->  Union[Instruction, Tuple[Instruction, Optional[VisualizationData]]]:
        return Instruction.UP