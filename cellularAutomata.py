#!/usr/bin/env python
# Import the neccesary modules
import struct
import CAUtilities
import sys
import os
import shutil

# User-input variables ###################################

# Simulation settings ------------------------------------
# Give the size of the grid to simulate on
numberOfRowsInGrid = 100
numberOfColumnsInGrid = 100

# Give the number of time steps to iterate the rule for
numberOfTimeSteps = 100

# Output settings -----------------------------------------
# Set a name for an output folder and a prefix for each output file
outputFolderName = "output"
filePrefix = "output"

# Set the number of frames per second for the produced video
videoFPS = 30

# Sets how many pixels a grid square is across in the produced images
gridSquareSize = 10

# Gives colouring rule for images
# This matches a cell state value to an RGB colour
colourRule = {
    # Syntax is cell value: (R, G, B)
    1: (0, 0, 0),
    0: (255, 255, 255)
}

# Initial state settings-----------------------------------
# Every points starts set to 0 except for coordinates set here
# Arguments are in the order - x, y, value
initialState = CAUtilities.StartingState(numberOfRowsInGrid, numberOfColumnsInGrid)
initialState.addPoint(10, 10, 1)
initialState.addPoint(12, 9, 1)
initialState.addPoint(12, 10, 1)
initialState.addPoint(11, 11, 1)
initialState.addPoint(12, 11, 1)


def addGlider(x, y, value, direction, state):
    # Default to southeast and then transform appropriately
    points={
        (1,-1),
        (-1,0),
        (1,0),
        (0,1),
        (1,1)
    }

    xMultiplier=1
    yMultiplier=1

    if direction=="northwest":
        yMultiplier=-1
        xMultiplier=-1
    elif direction=="northeast":
        yMultiplier=-1
    elif direction=="southwest":
        xMultiplier=-1
    elif direction=="southeast":
        pass
    else:
        raise Exception("Undefined direction chosen for glider. Options are northwest, northeast, southwest, southest.")

    success=1

    for point in points:
        success*=state.addPoint(x+point[0]*xMultiplier, y+point[1]*yMultiplier, value)

    return success

addGlider(50, 50, 1, "northeast", initialState)

#Rules to use in the model---------------------------------
#These functions determine the iteration rules that can be used for the system
def threshold(currentState, listOfNeighbourStates):
    #Changing this threshold does lots of differnt things
    thresholdValue=5

    if(sum(listOfNeighbourStates)>thresholdValue):
        return 0
    else:
        return 1

def twoWayThreshold(currentState, listOfNeighbourStates):
    upper=6
    lower=1

    sumOfList=sum(listOfNeighbourStates)

    if(sumOfList>=lower and sumOfList<=upper):
        return 1
    else:
        return 0

def spread(currentState, listOfNeighbourStates):
    if sum(listOfNeighbourStates)>0:
        return 1
    else:
        return 0

def gameOfLife(currentState, listOfNeighbourStates):
    total=sum(listOfNeighbourStates)

    if(currentState==0):
        if(total==3):
            return 1
        else:
            return 0
    else:
        if(total<2 or total>3):
            return 0
        else:
            return 1



# Set this equal to the name of the rule you want to use
rule=gameOfLife






###########################################################

# Main part of script #####################################

if __name__ == '__main__':
    # Just for now
    exit()

    # This class keeps track of the state of the system
    grid=CAUtilities.Grid(numberOfRowsInGrid, numberOfColumnsInGrid, initialState, gridSquareSize)

    # Check the output folder exists
    if(not os.path.isdir(outputFolderName)):
        os.mkdir(outputFolderName)

    # How often to report on output
    reportFrequency=10

    # Now run through time
    for t in range(numberOfTimeSteps + 1):
        if t % reportFrequency == 0:
            print("Time step "+str(t)+" of "+str(numberOfTimeSteps)+" done.")

        grid.saveToFile(t, outputFolderName+"/"+filePrefix, colourRule)
        grid.applyRule(rule)

    # Make output into a video
    os.chdir(outputFolderName)
    # command="ffmpeg -framerate "+str(videoFPS)+" -i "+filePrefix+"%d.bmp -crf 18 -vcodec mpeg4 -b:v 2000k -y "+filePrefix+".mp4 2> NUL"
    command = "convert -delay 1x"+str(videoFPS)+" "+str(filePrefix)+"%d.bmp[0-"+str(numberOfTimeSteps)+"] output.gif"
    os.system(command)
