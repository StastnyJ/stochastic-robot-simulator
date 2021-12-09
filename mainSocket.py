#!/usr/bin/python3.7

import json
import socket
from sys import argv, exit
from Environment import Environment, Instruction
from Simulator import Simulator
from datetime import datetime
import json

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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 8080))

        start = datetime.now()
        s.sendall(b"INIT: " + bytes(str(env) + "\n", 'ascii'))
        res = s.recv(8).decode("ascii").strip()
        if res != "DONE":
            print("Wrong answer from the server")
            s.sendall(b"END")
            exit(1)
        end = datetime.now()

        if (end - start).total_seconds() > initLimit:
            print("Init timeout")
            s.sendall(b"END")
            exit(1)

        while not sim.isTerminated():
            sensor = sim.getSensorValues()

            start = datetime.now()
            if GPS_ONLY:
                s.sendall(b'STEP: ' + bytes(str(pos) + "\n", "ascii"))
            else:
                s.sendall(b'STEP: ' + bytes(str(sensor) + "\n", "ascii"))
            result = Instruction(int(s.recv(2).decode('ascii').strip()))
            end = datetime.now()

            if (end - start).total_seconds() > instructionLimit:
                print("Instruction timeout")
                s.sendall(b"END")
                exit(1)

            if type(result) == tuple:
                instruction, visData = result
            else:
                instruction = result
                visData = None
            (pos, realInstruction) = sim.makeInstruction(instruction)
            history.append((instruction, realInstruction, sensor, pos, sim.getScore(), visData))
            
        s.sendall(b"END")

    print("Solution found in " + str(len(history)) + " steps. Overall score: " + str(round(sim.getScore(), 3)))

    if not NO_VIS:
        from Visualization import Visualization
        vis = Visualization(env, startPos, history)
        vis.run()
