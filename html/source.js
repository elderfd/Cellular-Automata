function Simulation(nRows, nCols)
{
    this.nRows = nRows;
    this.nCols = nCols;

    // Double-buffered system
    this.array = [];
    this.brray = [];

    for(i = 0; i < nCols; i++)
    {
        this.array[i] = [];
        this.brray[i] = [];

        for(j = 0; j < nRows; j++)
        {
            // Zero-initialise
            this.array[i][j] = 0;
            this.brray[i][j] = 0;
        }
    }

    this.useA = true;

    // For getting the states of neighbours around x, y
    this.getNeighbourStates = function(x, y, sizeOfNeighbourhood)
    {
        retList = [];
        xScan = [];
        yScan = [];

        for(offSet = 1; offSet < sizeOfNeighbourhood; offSet++)
        {
            
        }
    }
}

function go()
{
    // Grab the current parameter values
    var nRows = document.getElementById("parameterForm").elements["nRows"].value;
    var nCols = document.getElementById("parameterForm").elements["nCols"].value;

    // Set up a simulation object
    var sim = new Simulation(nRows, nCols);
}

function drawToCanvas(nRows, nCols)
{
    var canvas = document.getElementById("display");
    var context = canvas.getContext("2d");

    // Draw some random squares
    var squareXSize = canvas.width / nCols;
    var squareYSize = canvas.height / nRows;

    for(i = 0; i < nCols; i++)
    {
        for(j = 0; j < nRows; j++)
        {
            var squareColour = "#FC0808";
            if(Math.random() < 0.5)
            {
                squareColour = "#2DFC08";
            }

            context.fillStyle = squareColour;
            context.fillRect(i * squareXSize, j * squareYSize, squareXSize, squareYSize);
        }
    }
}
