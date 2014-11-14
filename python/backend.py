# The field that the simulation occurs on
class Grid:
    # Constructor
    def __init__(self, nRows, nCols, maxState, allowWrap):
        self.array = [[0 for x in range(nRows)] for x in range(nCols)]
        self.brray = [[0 for x in range(nRows)] for x in range(nCols)]
        self.useA = True
        self.nCols = nCols
        self.nRows = nRows
        self.maxState = maxState
        self.allowWrap = allowWrap

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
                # Ignore self
                if not (i == x and j == y):
                    # Decide what to do with cells off the grid
                    if i < 0 or i >= self.nCols or j < 0 or j >= self.nRows:
                        if self.allowWrap:
                            # Convert the i and j values to wrap
                            if i < 0:
                                i = self.nCols + i
                            elif i >= self.nCols:
                                i = i - self.nCols

                            if j < 0:
                                j = self.nRows + j
                            elif j >= self.nRows:
                                j = j - self.nRows
                        else:
                            continue

                    if(not self.useA):
                        retList.append(self.brray[i][j])
                    else:
                        retList.append(self.array[i][j])

        return retList

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
