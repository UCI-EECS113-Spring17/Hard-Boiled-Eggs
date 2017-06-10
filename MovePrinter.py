from pynq import Overlay
from pynq.board import RGBLED
from pynq.board import LED
from pynq.board import Button
from pynq.board import Switch
from pynq.iop import Arduino_IO
from Cube import Cube
from CubeSolver import CubeSolver

import time
import datetime

Overlay("base.bit").download()

class MovePrinter:

    def __init__(self, cube):
        CLEAR = 0
        BLUE = 1
        GREEN = 2
        CYAN = 3
        RED = 4
        MAGENTA = 5
        YELLOW = 6
        WHITE = 7
        self.rgb_led = [RGBLED(4), RGBLED(5)]
        self.led = [LED(3), LED(2), LED(1), LED(0)]
        self.button = [Button(index) for index in range(4)]
        self.switch = [Switch(0), Switch(1)]
        self.colors = {"D": WHITE, "F":GREEN, "U":YELLOW, "L":RED, "R":MAGENTA, "B":BLUE}
        self.faces = {"D": 5, "F":0, "U":4, "L":3, "R":1, "B":2}
        self.speed = 3
        self.cube = cube
        self.address_ports = [Arduino_IO(3, i, 'out') for i in reversed(range(6))]
        self.address_clock = Arduino_IO(3, 6, 'out')
        self.color_clock = Arduino_IO(3, 7, 'out')
        
    def turnOnLEDs(self, move):
        self.rgb_led[1].on(self.colors[move[0]])
        self.rgb_led[0].on(2)
        if len(move) == 2:
            if move[1] == "'":
                self.rgb_led[0].on(4)
            else:
                t_end = time.time() + self.speed
                if self.switch[1].read():
                    while time.time() < t_end:
                        if self.isButtonPressed():
                            self.setSpeed()
                        self.rgb_led[1].on(self.colors[move[0]])
                        time.sleep(.1)
                        self.rgb_led[1].off()
                        time.sleep(.1)
                else:
                    while not self.isButtonPressed():   
                        self.rgb_led[1].on(self.colors[move[0]])
                        time.sleep(.1)
                        self.rgb_led[1].off()
                        time.sleep(.1)
                        if self.switch[1].read():                         
                            break
    def turnOnCube(self):
        #1ms delay between times
        #t0: addr set
        #t1: addr clk up
        #t2: 1: addr clk down
        #    2: color set
        #t3: color clk up
        #t4: 1: color clk down
        #    2: addr set
        #loops
        colors = self.cube.index_colors()
        for i in range(54):
            binary = "{0:06b}".format(i)
            index = 0
            print(binary)
            for j in binary:
                if j == '1':
                    self.address_ports[index].write(1)
                else:
                    self.address_ports[index].write(0)

                index+=1
            time.sleep(.001)
            self.address_clock.write(1)
            time.sleep(.001)
            self.address_clock.write(0)
            binary = "{0:06b}".format(colors[i])
            print(binary)
            index = 0
            for j in binary:
                if j == '1':
                    self.address_ports[index].write(1)
                else:
                    self.address_ports[index].write(0)
                index+=1
            time.sleep(.001)
            self.color_clock.write(1)
            time.sleep(.001)
            self.color_clock.write(0)
            
    def turnOffCube(self):
        for port in self.address_ports:
            port.write(0)
                    
    def turnOnProgress(self, num_moves, index):
        progress = int(index/(num_moves/4))
        for i in range(len(self.led)):
            if(i <= progress):
                self.led[i].on()
            else:
                self.led[i].off()

    def turnOffLEDs(self):
        for l in self.rgb_led:
            l.off()
        for l in self.led:
            l.off()

    def isButtonPressed(self):
        return self.button[0].read() or self.button[1].read() or self.button[2].read() or self.button[3].read()
    
    def setSpeed(self):
        if self.button[0].read():
            self.speed = .2
        elif self.button[1].read():
            self.speed = 1
        elif self.button[2].read():
            self.speed = 2
        elif self.button[3].read():
            self.speed = 3

    def isSwitchOn(self):
        return self.switch[0].read()

    def congratulations(self):
        while not self.isButtonPressed():
            for l in self.led:
                if self.isButtonPressed():
                    break
                l.on()
                time.sleep(.1)
                l.off()
                time.sleep(.1)

    def print_moves(self, moves):
        print(moves)
        index = 0
        num_moves = len(moves)
        self.justFlashed = False
        while index < num_moves:
            if index < 0:
                index = 0
            if self.switch[1].read() and self.isButtonPressed():
                self.setSpeed()
            if len(moves[index]) == 2:
                if moves[index][1] == "'":
                    self.cube.rotate(self.faces[moves[index][0]], -1)
                else:
                    self.cube.rotate(self.faces[moves[index][0]], 1)
                    self.cube.rotate(self.faces[moves[index][0]], 1)
            self.turnOnCube()
            self.turnOnLEDs(moves[index])
            self.turnOnProgress(num_moves, index)
            if index == num_moves-1:
                self.congratulations()
            while True:
                if self.switch[1].read() and self.isButtonPressed():
                    self.setSpeed()
                
                if self.switch[1].read():
                    t_end = time.time() + self.speed
                    while time.time() < t_end:
                        if self.switch[1].read() and self.isButtonPressed():
                            self.setSpeed()
                        if not self.switch[1].read():
                            break
                    if not self.switch[1].read():
                        index-=1
                    break
                if self.isButtonPressed() and not self.switch[1].read():
                    break
            if not self.switch[0].read():
                index+=1
            else:
                index-=1
            while True:
                if self.switch[1].read() and self.isButtonPressed():
                    self.setSpeed()
                if self.switch[1].read():
                    break
                if not self.isButtonPressed():
                    break
            
        self.turnOffLEDs()
        self.turnOffCube()