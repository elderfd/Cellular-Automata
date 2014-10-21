#!/usr/bin/env python

import struct
import sys
import pygame
import datetime

#########################################################

# Gives the current number of milliseconds since epoch
def msecsSinceEpoch():
    epoch = datetime.datetime(1970, 1, 1)
    diff = datetime.datetime.now() - epoch
    return (diff.microseconds * 1000)

# Utility classes
class Grid:
    # Constructor
    def __init__(self, nRows, nCols, initialState, maxState):
        self.array = [[0 for x in range(nRows)] for x in range(nCols)]
        self.brray = [[0 for x in range(nRows)] for x in range(nCols)]
        self.useA = True
        self.nCols = nCols
        self.nRows = nRows
        self.maxState = maxState

        for key in initialState:
            self.array[key[0]][key[1]] = initialState[key]

    def getNeighbourStates(self, x, y, sizeOfNeighbourHood):
        retList = []
        xScan = []
        yScan = []

        for offSet in range(sizeOfNeighbourHood + 1):
            xScan.append(x - offSet)
            yScan.append(y - offSet)

            if offSet != 0:
                xScan.append(x + offSet)
                yScan.append(y + offSet)

        for i in xScan:
            for j in yScan:
                #Ignore self and cells outside the grid
                if not (i==x and j==y or i<0 or i>=self.nCols or j<0 or j>=self.nRows):
                    if(not self.useA):
                        retList.append(self.brray[i][j])
                    else:
                        retList.append(self.array[i][j])

        return retList

    # TODO: Need to check array/brray weirdness here
    def getState(self, x, y):
        x = int(x)
        y = int(y)
        if self.useA:
            return self.array[x][y]
        else:
            return self.brray[x][y]

    def setState(self, x, y, value):
        x = int(x)
        y = int(y)
        if self.useA:
            self.array[x][y] = value
        else:
            self.brray[x][y] = value

    def incrementState(self, x, y):
        if self.getState(x, y) != self.maxState:
            self.setState(x, y, self.getState(x, y) + 1)

    def decrementState(self, x, y):
        if self.getState(x, y) != 0:
            self.setState(x, y, self.getState(x, y) - 1)

    def applyRule(self, rule):
        for i in range(self.nCols):
            for j in range(self.nRows):
                # Assume for now the neighbourhood size is 1
                if(not self.useA):
                    self.array[i][j] = rule(self.brray[i][j],  self.getNeighbourStates(i, j, 1))
                else:
                    self.brray[i][j] = rule(self.array[i][j], self.getNeighbourStates(i, j, 1))

        self.useA = not self.useA


    # TODO: Fix this function
    def saveToFile(self, t, filePrefix, colourMap):
        fileName=str(filePrefix)+str(t)+".bmp"

        d = {
            'mn1':66,
            'mn2':77,
            'filesize':3*self.nCols*self.squareSize*self.nRows*self.squareSize+54,
            'undef1':0,
            'undef2':0,
            'offset':54,
            'headerlength':40,
            'width':self.nCols*self.squareSize,
            'height':self.nRows*self.squareSize,
            'colorplanes':1,
            'colordepth':24,
            'compression':0,
            'imagesize':0,
            'res_hor':0,
            'res_vert':0,
            'palette':0,
            'importantcolors':0
            }

        data=bytes()

        for row in range(self.nRows-1,-1,-1):# (BMPs are L to R from the bottom L row)
            line=bytes()

            for column in range(self.nCols):
                if(self.useA):
                    colourTuple=colourMap[self.array[column][row]]
                else:
                    colourTuple=colourMap[self.brray[column][row]]
                r = colourTuple[0]
                g = colourTuple[1]
                b = colourTuple[2]
                pixel = struct.pack('<BBB',b,g,r)

                for j in range(self.squareSize):
                    line = line + pixel
                row_mod = (d['width']*d['colordepth']/8) % 4
                if row_mod == 0:
                    padding = 0
                else:
                    padding = (4 - row_mod)
                padbytes = bytes()
                for i in range(int(padding)):
                    x = struct.pack('<B',0)
                    padbytes = padbytes + x
                line = line + padbytes

            for i in range(self.squareSize):
                data=data+line

        bmp_write(d, data, fileName)

class StartingState:
    def __init__(self, nrows, ncols):
        self.coordsToValue={}
        self.nrows=nrows
        self.ncols=ncols

    #Returns a boolean depending on whether the point was actually added
    def addPoint(self, x, y, value):
        if x>=0 and x<self.ncols and y>=0 and y<self.nrows:
            self.coordsToValue[(x, y)]=value
            return True
        else:
            return False

    #For iterating through the points
    def __iter__(self):
        return iter(self.coordsToValue)

    def __getitem__(self, key):
        return self.coordsToValue[key]


######################################################################

# Function to write a bmp file.  It takes a dictionary (d) of
# header values and the pixel data (bytes) and writes them
# to a file.
def bmp_write(d, byte, fileName):
    mn1 = struct.pack('<B',d['mn1'])
    mn2 = struct.pack('<B',d['mn2'])
    filesize = struct.pack('<L',d['filesize'])
    undef1 = struct.pack('<H',d['undef1'])
    undef2 = struct.pack('<H',d['undef2'])
    offset = struct.pack('<L',d['offset'])
    headerlength = struct.pack('<L',d['headerlength'])
    width = struct.pack('<L',d['width'])
    height = struct.pack('<L',d['height'])
    colorplanes = struct.pack('<H',d['colorplanes'])
    colordepth = struct.pack('<H',d['colordepth'])
    compression = struct.pack('<L',d['compression'])
    imagesize = struct.pack('<L',d['imagesize'])
    res_hor = struct.pack('<L',d['res_hor'])
    res_vert = struct.pack('<L',d['res_vert'])
    palette = struct.pack('<L',d['palette'])
    importantcolors = struct.pack('<L',d['importantcolors'])
    # create the outfile
    outfile = open(fileName,'wb')
    # write the header + the bytes
    outfile.write(mn1 + mn2 + filesize + undef1 + undef2 + offset + headerlength + width + height + colorplanes + colordepth + compression + imagesize + res_hor + res_vert + palette + importantcolors + byte)
    outfile.close()

class Display:
    def __init__(self, nRows, nCols, maxFPS, colourRule, ruleSet):
        # Set up pygame stuff first
        pygame.init()

        # Some defaults
        # TODO: This should probably scale inversely with number of squares
        defaultSquareXSize = 10
        defaultSquareYSize = 10

        self.squareXSize = defaultSquareXSize
        self.squareYSize = defaultSquareYSize

        self.screenOptions = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
        pygame.display.set_caption("Cellular Automata")
        self.screen = pygame.display.set_mode([nRows * self.squareYSize, nCols * self.squareXSize], self.screenOptions)
        initialState = StartingState(nRows, nCols)
        self.rule = ruleSet
        self.colourRule = colourRule

        # Work out the number of states there are
        maxState = 0
        for key in colourRule:
             if key > maxState:
                 maxState = key

        self.grid = Grid(nRows, nCols, initialState, maxState)
        self.inSetUpMode = True
        self.buttonPressedInWindow = False
        self.simulating = False
        self.minTimeBetweenFrames = 1 / maxFPS
        self.timeOfLastDraw = 0


    # Returns a Rect which matches the given grid x, y coordinates
    def gridCoordsToDisplayRect(self, x, y):
        left = x * self.squareXSize
        top = y * self.squareYSize
        width = self.squareXSize
        height = self.squareYSize
        return pygame.Rect(left, top, width, height)

    def render(self):
        # Draw the coloured squares
        for x in range(self.grid.nCols):
            for y in range(self.grid.nRows):
                # Grab the value in the grid, choose the right colour
                # Then draw a box to match
                colour = self.colourRule[self.grid.getState(x, y)]
                rect = self.gridCoordsToDisplayRect(x, y)
                pygame.draw.rect(self.screen, colour, rect)

        # Whack in some grid lines
        black = (0, 0, 0)

        x = 0
        while x <= self.grid.nCols * self.squareXSize:
            startCoords = (x, 0)
            endCoords = (x, self.grid.nRows * self.squareYSize)
            pygame.draw.line(self.screen, black, startCoords, endCoords)
            x += self.squareXSize

        y = 0
        while y <= self.grid.nRows * self.squareYSize:
            startCoords = (0, y)
            endCoords = (self.grid.nCols * self.squareXSize, y)
            pygame.draw.line(self.screen, black, startCoords, endCoords)
            y += self.squareYSize


        pygame.display.update()

    def run(self):
        stop = False

        # Initial draw
        self.render()

        while not stop:
            # Deal with any queued events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    # Rescale to match new size
                    newRes = event.dict['size']
                    self.squareXSize = newRes[0] / self.grid.nCols
                    self.squareYSize = newRes[1] / self.grid.nRows
                    screen = pygame.display.set_mode(newRes, self.screenOptions)

                    self.render()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.buttonPressed = event.button
                    self.buttonPressedInWindow = True
                    self.buttonPressCoords = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.buttonPressedInWindow:
                        self.buttonPressedInWindow = False
                        gridX = self.buttonPressCoords[0] / self.squareXSize
                        gridY = self.buttonPressCoords[1] / self.squareYSize

                        if self.buttonPressed == 1:
                            # LMB
                            self.grid.incrementState(gridX, gridY)
                        elif self.buttonPressed == 3:
                            # RMB
                            self.grid.decrementState(gridX, gridY)

                        self.render()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # If running then pause, otherwise start running
                    self.simulating = not self.simulating

            if self.simulating:
                # Make sure we don't render too quickly
                if msecsSinceEpoch() - self.timeOfLastDraw > self.minTimeBetweenFrames:
                    self.grid.applyRule(self.rule)
                    self.render()
