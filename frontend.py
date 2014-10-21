import backend
import pygame
import datetime

# Gives the current number of milliseconds since epoch
def msecsSinceEpoch():
    epoch = datetime.datetime(1970, 1, 1)
    diff = datetime.datetime.now() - epoch
    return (diff.microseconds * 1000)

# Provides the display for the simulation and allows interaction
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

        self.borderThickness = 2

        self.screenOptions = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
        pygame.display.set_caption("Cellular Automata")
        self.screen = pygame.display.set_mode([nRows * self.squareYSize + self.borderThickness, nCols * self.squareXSize + self.borderThickness], self.screenOptions)
        self.rule = ruleSet
        self.colourRule = colourRule

        # Work out the number of states there are
        maxState = 0
        for key in colourRule:
             if key > maxState:
                 maxState = key

        self.grid = backend.Grid(nRows, nCols, maxState, True)
        self.inSetUpMode = True
        self.buttonPressedInWindow = False
        self.simulating = False
        self.minTimeBetweenFrames = 1 / maxFPS
        self.timeOfLastDraw = 0


    # Returns a Rect which matches the given grid x, y coordinates
    def gridCoordsToDisplayRect(self, x, y):
        left = self.gridXToDisplayX(x)
        top = self.gridYToDisplayY(y)
        width = self.squareXSize + 2 * self.borderThickness
        height = self.squareYSize + 2 * self.borderThickness
        return pygame.Rect(left, top, width, height)

    def gridXToDisplayX(self, x):
        return x * self.squareXSize + self.borderThickness

    def gridYToDisplayY(self, y):
        return y * self.squareYSize + self.borderThickness

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

        x = 1
        while x < self.grid.nCols:
            startCoords = (self.gridXToDisplayX(x) , self.gridYToDisplayY(0))
            endCoords = (self.gridXToDisplayX(x), self.gridYToDisplayY(self.grid.nRows))
            pygame.draw.line(self.screen, black, startCoords, endCoords)
            x += 1

        y = 1
        while y < self.grid.nRows:
            startCoords = (self.gridXToDisplayX(0), self.gridYToDisplayY(y))
            endCoords = ( self.gridXToDisplayX(self.grid.nCols), self.gridYToDisplayY(y))
            pygame.draw.line(self.screen, black, startCoords, endCoords)
            y += 1

        # Special coloured grid lines around edge to show play/ pause
        topLeft = (0, 0)
        topRight = (self.squareXSize * self.grid.nCols, 0)
        bottomRight = (self.squareXSize * self.grid.nCols, self.squareYSize * self.grid.nRows)
        bottomLeft=(0, self.squareYSize * self.grid.nRows)

        if self.simulating:
            borderColour = (0, 255, 0)
        else:
            borderColour = (255, 0, 0)

        # Maybe should use draw.lines in future but this won't
        # be a rate-limiting step and some issues with joins
        # apparently
        pygame.draw.line(self.screen, borderColour, topLeft, topRight)
        pygame.draw.line(self.screen, borderColour, topRight, bottomRight)
        pygame.draw.line(self.screen, borderColour, bottomRight, bottomLeft)
        pygame.draw.line(self.screen, borderColour, bottomLeft, topLeft)

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
                    self.squareXSize = (newRes[0] - self.borderThickness) / self.grid.nCols
                    self.squareYSize = (newRes[1] - self.borderThickness) / self.grid.nRows
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
                    self.render()

            if self.simulating:
                # Make sure we don't render too quickly
                if msecsSinceEpoch() - self.timeOfLastDraw > self.minTimeBetweenFrames:
                    self.grid.applyRule(self.rule)
                    self.render()
