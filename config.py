# User-input variables ###################################

# Simulation settings ------------------------------------
# Give the size of the grid to simulate on
numberOfRowsInGrid = 100
numberOfColumnsInGrid = 100

# The maximum FPS the simulation will be displayed at
videoFPS = 30

# Gives colouring rule for images
# This matches a cell state value to an RGB colour
colourRule = {
    # Syntax is - cell value: (R, G, B)
    1: (0, 0, 0),
    0: (255, 255, 255)
}
# ------------------------------------------------------

# Rules to use in the model
def ruleSet(currentState, listOfNeighbourStates):
    total = sum(listOfNeighbourStates)

    if(currentState == 0):
        if(total == 3):
            return 1
        else:
            return 0
    else:
        if(total < 2 or total > 3):
            return 0
        else:
            return 1
