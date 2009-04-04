# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but without any warranty; without even the implied warranty of
# merchantability or fitness for a particular purpose.  see the
# gnu library general public license for more details.
# 
#you should have received a copy of the gnu general public license
#along with this program; if not, write to the free software
#foundation, inc., 51 franklin street, fifth floor boston, ma 02110-1301,  usa

import threading
import random
import gobject
from Consts import *

class SnakeModel (threading.Thread):
    def __init__ (self, snake, maxX, maxY):
        threading.Thread.__init__ (self)
        self.snake = snake
        self.maxX = maxX
        self.maxY = maxY
        self.paused = False
        self.direction = UP
        self.timeInterval = 200
        self.speedChangeRate = .75
        self.score = 0
        self.countMove = 0
        self.matrix = [[0 for col in range (self.maxY)] for row in range (self.maxX)]
        initlength = self.maxX / 2 > 5 and 5 or self.maxX / 2
        # snake nodes store in a list
        self.nodes = [(x, self.maxY - 2) for x in range (self.maxX / 2, self.maxX / 2 + initlength)]
        for x, y in self.nodes:
            self.matrix [x][y] = 1
        self.createfood()
        
    def run (self):
        # move on per timeInterval until lose
        gobject.timeout_add (self.timeInterval, self.moveon)
                    
    def moveon (self):
        # create new node
        x, y = self.nodes [0]
        directiondict = {UP : "y -= 1", DOWN : "y += 1", LEFT : "x -= 1", RIGHT : "x += 1"}
        exec (directiondict [self.direction])
        # continue when paused
        if (self.paused):
            return True
        if (x in range (self.maxX) and y in range (self.maxY)):
            if (self.matrix [x][y] == 0):
                # meets nothing
                self.countMove += 1
                self.matrix [x][y] = 1
                # move
                x1, y1 = self.nodes [-1]
                self.matrix [x1][y1] = 0
                self.nodes = [(x, y)] + self.nodes [:-1]
            elif ([x, y] == self.food):
                # meets food
                self.nodes = [(x, y)] + self.nodes
                scoregot = (10000 - 200 * self.countMove) / self.timeInterval
                self.score += scoregot < 10 and 10 or scoregot
                self.countMove = 0
                self.createfood ()
            else:
                # meets snake itself
                gobject.idle_add (self.snake.game_over)
                return False
            # refresh 
            self.snake.repaint ()
            return True
        else:
            # meets the walls
            gobject.idle_add (self.snake.game_over)
            return False
        
    def createfood (self):
        x, y = [random.randint (0, i - 1) for i in (self.maxX, self.maxY)]
        while (self.matrix [x][y]):
            x, y = [random.randint (0, i - 1) for i in (self.maxX, self.maxY)]
        self.food = [x, y]
        self.matrix [x][y] = 1
                
    def changedirection (self, newdirection):
        # only change when rotate 90 degrees
        if ((newdirection - self.direction) % 2):
            self.direction = newdirection
            
    def changespeed (self, key):
        # do not work
        print key, PGUP, PGDOWN, self.timeInterval
        if key == PGUP:
            self.timeInterval *= self.speedChangeRate
        elif key == PGDOWN:
            self.timeInterval /= self.speedChangeRate
            pass
        
    def pause (self, key = SPACE):
        self.paused = not self.paused

    def stop (self):
        # create a illegal node
        self.nodes [0] = (-1, -1)
