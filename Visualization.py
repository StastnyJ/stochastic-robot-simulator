import pygame as pg
from Environment import Environment, Instruction, SensorData, SpotType, VisualizationData
from typing import Tuple, List, Optional
from datetime import datetime
import os

class Visualization():
    def __init__(self, env: Environment, position: Tuple[int, int], history: List[Tuple[Instruction, Instruction, SensorData, Tuple[int,int], float, Optional[VisualizationData]]]):
        self._env = env
        self._startPosition = position
        self._actStep = 0
        self._history = history

        self._screenWidth = 0
        self._screenHeight = 0
        self._cellSize = 0
        self._autorun = False
        self._screen = None
        self._speed = 200000

    def _pygame_init(self):
        pg.init()
        infoObject = pg.display.Info()
        self._screenWidth, self._screenHeight = (infoObject.current_w, infoObject.current_h)
        self._screenHeight = int(0.9 * self._screenHeight)
        self._cellSize = min((4*self._screenWidth // 5) // (len(self._env.map[0]) - 2), self._screenHeight // (len(self._env.map) - 2))
        pg.display.set_caption("Robot")
        self._setDimensions()

    def _setDimensions(self):
        self._screenHeight = self._cellSize * (len(self._env.map) - 2)
        self._screenWidth = 5 * self._cellSize * (len(self._env.map[0]) - 2) // 4
        self._screen = pg.display.set_mode((self._screenWidth, self._screenHeight))

    def _makeStep(self):
        self._actStep = min(self._actStep + 1, len(self._history))

    def _getPosCoords(self, pos):
        x, y = pos
        return x * self._cellSize, y * self._cellSize

    def _getCustomColor(self, i, j):
        if self._history[self._actStep % len(self._history)][-1] == None:
            return None
        colors = self._history[self._actStep % len(self._history)][-1].colors 
        if colors == None:
            return None
        return colors[i][j]

    def _drawPlane(self):
        for i in range(1, len(self._env.map) -1):
            for j in range(1, len(self._env.map[i]) - 1):
                x, y = self._getPosCoords((j - 1, i - 1))
                color = self._getCustomColor(i, j)
                if self._env.map[i][j][0] == SpotType.WALL:
                    pg.draw.rect(self._screen, (0,0,0), pg.Rect(x,y,self._cellSize, self._cellSize))
                elif self._env.map[i][j][0] == SpotType.TERMINAL:
                    pg.draw.rect(self._screen, (255,0,0) if color is None else color, pg.Rect(x,y,self._cellSize, self._cellSize))
                elif color is not None:
                    pg.draw.rect(self._screen, color, pg.Rect(x,y,self._cellSize, self._cellSize))
                pg.draw.rect(self._screen, (0,0,0), pg.Rect(x,y,self._cellSize, self._cellSize), 1)

    def _drawBot(self):
        if self._actStep == 0:
            pos = self._startPosition
        else:
            _,_,_,pos,_,_ = self._history[self._actStep - 1]
        x, y = self._getPosCoords((pos[1] - 1, pos[0] - 1))
        pg.draw.circle(self._screen, (140, 140, 140), (x + self._cellSize // 2, y + self._cellSize // 2),  self._cellSize // 5)


    def _drawText(self, text: str, size, position, color):
        font = pg.font.Font(pg.font.match_font('Droid Sans Mono'), size)
        lines = text.split("\n")
        for i, l in enumerate(lines):
            textSurface = font.render(l, True, color)
            textRect = textSurface.get_rect()
            textRect.midtop = (position[0], position[1] + i * size)
            self._screen.blit(textSurface, textRect)


    def _drawTexts(self):
        texts = self._history[self._actStep % len(self._history)][-1].texts
        if texts == None:
            return
        for i in range(1, len(texts) -1):
            for j in range(1, len(texts[i]) - 1):
                x, y = self._getPosCoords((j - 1, i - 1))
                self._drawText(texts[i][j], 20, (x + self._cellSize // 2,y + self._cellSize // 2), (0,0,0))

    def _drawHistory(self):
        controlsText = "\n\n----------------\n\nCONTROLS\n\nNext step: SPACE\nPrev step: B\nAutorun: A\nAutorun speed: +/-\nresize window: L/S"
        if self._actStep >= len(self._history):
            _,_,_,_,score,_  = self._history[-1]
            text = 'Score: %.2f\nSteps: %d' % (score, self._actStep)
        else:
            instr,realInstr,sensor,_,_,_  = self._history[self._actStep]
            _,_,_,_,score,_  = self._history[self._actStep-1]
            if self._actStep == 0:
                score = 0
            text = 'Command: %s\nExecuted com.: %s\n\nSensor data\n\nUp: %s\nLeft: %s\nRight: %s\nBottom: %s\n\nScore: %.2f\nStep: %d' % (instr.name, realInstr.name, sensor.up, sensor.left, sensor.right, sensor.down, score, self._actStep)
        self._drawText(text + controlsText, 22, (9 * self._screenWidth // 10, 32), (0,0,0))

    def _draw(self):
        self._screen.fill((255,255,255))
        self._drawPlane()
        self._drawBot()
        if self._history[self._actStep % len(self._history)][-1] != None:
            self._drawTexts()
        self._drawHistory()

    def run(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        self._pygame_init()
        exit = False
        lastAutostep = datetime.now()
        while not exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if not self._autorun:
                            self._makeStep()
                    if event.key == pg.K_b:
                        if self._actStep == 0 or self._autorun:
                            continue
                        self._actStep -= 1
                    if event.key == pg.K_a:
                        self._autorun = not self._autorun
                    if event.key == pg.K_PLUS:
                        self._speed *= 0.8
                    if event.key == pg.K_MINUS:
                        self._speed /= 0.8
                    if event.key == pg.K_l:
                        self._cellSize = int(self._cellSize * 1.1)
                        self._setDimensions()
                    if event.key == pg.K_s:
                        self._cellSize = int(self._cellSize * 0.9)
                        self._setDimensions()
            if self._autorun:
                if (datetime.now() - lastAutostep).microseconds > self._speed:
                    lastAutostep = datetime.now()
                    self._makeStep()
            self._draw()
            pg.display.flip()