#!/usr/bin/python3.7

import json
from sys import argv
from Environment import Environment
from Simulator import Simulator
from Solution import Solution
from datetime import datetime
# from ExampleSolution import Solution
import sys

def loadData(file: str):
    data = None
    with open(file) as f:
        data = json.load(f)
    return data

NO_VIS = False
GPS_ONLY = False

initLimit = 10
instructionLimit = 0.5

if __name__ == "__main__":
    data = loadData(argv[1])
    for arg in argv[1:]:
        if arg.lower() == "novis":
            NO_VIS = True
        if arg.lower() == "gps":
            GPS_ONLY = True

    startPos = tuple(data['position'])
    pos = startPos
    history = []
    env = Environment.build(data['map'], data['rewards'], data['stepPenalty'])
    sim = Simulator(env, startPos, 0.1, 0.2, 0.1, 5323)

    start = datetime.now()
    sol = Solution(env)
    end = datetime.now()
    if (end - start).total_seconds() > initLimit:
        print("Init timeout")
        sys.exit(1)

    while not sim.isTerminated():
        sensor = sim.getSensorValues()

        start = datetime.now()
        result = sol.getInstructionGPS(pos) if GPS_ONLY else sol.getInstruction(sensor)
        end = datetime.now()
        if (end - start).total_seconds() > instructionLimit:
            print("Instruction timeout")
            sys.exit(1)

        if type(result) == tuple:
            instruction, visData = result
        else:
            instruction = result
            visData = None
        (pos, realInstruction) = sim.makeInstruction(instruction)
        history.append((instruction, realInstruction, sensor, pos, sim.getScore(), visData))
        
    print("Solution found in " + str(len(history)) + " steps. Overall score: " + str(round(sim.getScore(), 3)))

    if not NO_VIS:
        from Visualization import Visualization
        vis = Visualization(env, startPos, history)
        vis.run()
