#!/usr/bin/python3.7

import json
from sys import argv
from Environment import Environment
from Simulator import Simulator
# from Solution import Solution
from ExampleSolution import Solution

def loadData(file: str):
    data = None
    with open(file) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    # data = loadData(argv[1])
    data = loadData("environments/env0.json")
    startPos = tuple(data['position'])
    pos = startPos
    history = []
    env = Environment.build(data['map'], data['rewards'], data['stepPenalty'])
    sim = Simulator(env, startPos, 0.1, 0.2, 0.1, 5323)
    sol = Solution(env)
    while not sim.isTerminated():
        sensor = sim.getSensorValues()
        result = sol.getInstruction(sensor)
        # result = sol.getInstructionGPS(pos)
        if type(result) == tuple:
            instruction, visData = result
        else:
            instruction = result
            visData = None
        (pos, realInstruction) = sim.makeInstruction(instruction)
        history.append((instruction, realInstruction, sensor, pos, sim.getScore(), visData))

    from Visualization import Visualization
    vis = Visualization(env, startPos, history)
    vis.run()
