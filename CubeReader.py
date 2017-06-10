from pynq import Overlay
from Cube import Cube
from CubeSolver import CubeSolver
import cv2
import numpy as np
from pynq.board import Button
from pynq.board import LED
from pynq.board import RGBLED

Overlay("base.bit").download()


button = Button(0)
led_0 = RGBLED(4)
led_1 = RGBLED(5)


IMAGE_PATH = "cube.png"


class CubeReader:

    def readCube(self):
        cube = Cube()
        
        for i in range(6):
            cube.face[i] = self._readFace(i)
        #cube.face[0] = self._readFace(0)

        return cube


    def _readFace(self, middle_color):
        face = []
        for i in range(3):
            face.append([None]*3)

        led_0.on(3)
        while (button.read() != 1):
            pass
        led_0.off()
        led_1.off()
        
        self._takePicture()
        led_1.on(5)
        colors = self._getColors(middle_color)

        for x in range(3):
            for y in range(3):
                face[x][y] = colors[x + 3*y]

        return face
                

    def _getColors(self, middle_color):
        colors = [None]*9
        img = cv2.imread(IMAGE_PATH, 1)
        coords = self._getCoords()

        for i in range(9):
            if i == 4:
                colors[i] = middle_color
            else:
                colors[i] = self._analyzeColor(img[tuple(coords[i])])

        return colors


    def _analyzeColor(self, value):
        B, G, R = value
        if R == 0:
            R = 1
        if G == 0:
            G = 1
        if B == 0:
            B = 1

        print(R, G, B)

        if (0.8 < R/G < 1.2) and (0.8 < R/B < 1.2) and (0.8 < G/B < 1.2):
            # WHITE
            color = 5
        elif (R/G > 4) and (R/B > 4) and G < 30:
            # RED
            color = 3
        elif (B/R > 1.5) and (B/G > 1):
            # BLUE
            color = 2
        elif (G/R > 1.5) and (G/B > 1):
            # GREEN
            color = 0
        elif (R/G > 1.5) and (R/B > 1.5):
            # ORANGE
            color = 1
        elif (0.8 < R/G < 1.2) and (R/B > 1.2) and (G/B > 1.2):
            # YELLOW
            color = 4
            

        # WHITE:  R/G = 1  R/B = 1  G/B = 1     (255, 255, 255)
        # YELLOW: R/G = 1  R/B = 2  G/B = 2     (255, 255, 0  )
        # RED:    R/G = 3  R/B = 3  G/B = 1     (255, 0  , 0  )
        # ORANGE: R/G = 2  R/B = 3  G/B = 3     (255, 128, 0  )
        # BLUE:   R/G = 1  R/B = 0  G/B = 0     (0  , 0  , 255)
        # GREEN:  R/G = 0  R/B = 1  G/B = 3     (0  , 255, 0  )

        print(color)
        return color
    

    def _takePicture(self):
        cam = cv2.VideoCapture(0)

        if cam.isOpened():
            ret, image = cam.read()
            cv2.imwrite(IMAGE_PATH, image)

        del(cam)


    def _binaryImage(self):
        img = cv2.imread(IMAGE_PATH, 0)
        img = cv2.medianBlur(img, 5)
        ret, bin_img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)

        # cv2.imwrite("cube_binary.png", bin_img)

        return bin_img


    def _getCoords(self):
        bin_img = self._binaryImage()
        corners = [None]*4
        for i in range(4):
            corners[i] = self._getCorner(bin_img, i)
            #print(corners[i])

        print()

        coords = [None]*9
        diag1 = subCoords(corners[2], corners[0])
        diag2 = subCoords(corners[1], corners[3])

        coords[0] = addCoords(corners[0], divCoords(diag1, 6))
        coords[2] = subCoords(corners[1], divCoords(diag2, 6))
        coords[4] = addCoords(corners[0], divCoords(diag1, 2))
        coords[6] = addCoords(corners[3], divCoords(diag2, 6))
        coords[8] = subCoords(corners[2], divCoords(diag1, 6))
        coords[1] = avgCoords(coords[0], coords[2])
        coords[3] = avgCoords(coords[0], coords[6])
        coords[5] = avgCoords(coords[2], coords[8])
        coords[7] = avgCoords(coords[6], coords[8])

        for i in range(9):
            bin_img[tuple(coords[i])] = 0
            #print(coords[i])

        # cv2.imwrite("cube_coords.png", bin_img)

        return coords

        
    def _getCorner(self, bin_img, corner):
        height, width = bin_img.shape
        
        if corner == 0:
            for x in range(width):
                for y in range(x+1):
                    if y >= height:
                        y = height-1
                    pixel = y, x-y
                    if bin_img[pixel] == 0:
                        return pixel
        elif corner == 1:
            for x in range(width):
                for y in range(x+1):
                    if y >= height:
                        y = height-1
                    pixel = y, width-x-1+y
                    if bin_img[pixel] == 0:
                        return pixel
                    
        elif corner == 2:
            for x in range(width):
                for y in range(x+1):
                    if y >= height:
                        y = height-1
                    pixel = height-1-y, width-x-1+y
                    if bin_img[pixel] == 0:
                        return pixel
        else:
            for x in range(width):
                for y in range(x+1):
                    if y >= height:
                        y = height-1
                    pixel = height-1-y, x-y
                    if bin_img[pixel] == 0:
                        return pixel


def addCoords(list1, list2):
    return [list1[0] + list2[0], list1[1] + list2[1]]


def subCoords(list1, list2):
    return [list1[0] - list2[0], list1[1] - list2[1]]


def divCoords(list1, den):
    return [list1[0]//den, list1[1]//den]


def avgCoords(list1, list2):
    return divCoords(addCoords(list1, list2), 2)
    

if __name__ == '__main__':
    reader = CubeReader()
    solver = CubeSolver(reader.readCube())
    solver.print()
    solver.solve()
    print(solver.moves)
    print(len(solver.moves))

#if __name__ == '__main__':
    #reader = CubeReader()
    #reader._takePicture()
    #cv2.imwrite("cube_binary.png", reader._binaryImage())
    #reader._getCoords()
