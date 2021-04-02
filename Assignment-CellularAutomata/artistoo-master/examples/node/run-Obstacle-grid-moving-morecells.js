/* Source the CPM module (cpm-cjs version because this is a node script).*/
let CPM = require("../../build/artistoo-cjs.js")

let config = {

    // Grid settings
    ndim: 2,
    field_size: [250, 250],

    // CPM parameters and configuration
    conf: {
        torus : [true, true],
        seed : 10,
        T: 20,                                // CPM temperature

        // Adhesion parameters:
        J: [[0, 20, 20], [20, 0, 20], [20, 20, 0]],

        // VolumeConstraint parameters
        LAMBDA_V: [0, 50, 50],                // VolumeConstraint importance per cellkind
        V: [0, 500, 500],                    // Target volume of each cellkind

        LAMBDA_P: [0, 2, 2],
        P : [0, 300, 300],

        LAMBDA_ACT : [0,400,0],
        MAX_ACT : [0,50,0],
        ACT_MEAN : "geometric"


    },
    
    // Simulation setup and configuration
    simsettings: {
        // Cells on the grid
        NRCELLS: [1,1],                    // Number of cells to seed for all
        // non-background cellkinds.
        
        BURNIN : 500,
        RUNTIME: 1000,                  // Only used in node

        CANVASCOLOR: "eaecef",
        CELLCOLOR: ["000000", "FF0000"],
        ACTCOLOR: [true, false],
        SHOWBORDERS: [true, true],
        BORDERCOL: ["00FF00", "0000FF"],
        zoom: 2,                        // zoom in on canvas with this factor.
        
        SAVEIMG : true,
        IMGFRAMERATE: 1,
        SAVEPATH : "output/img/Obstacle-grid-moving-morecells",    // ... And save the image in this folder.
        EXPNAME : "Obstacle-grid-moving-morecells",                    // Used for the filename of output images.
        STATSOUT : { browser: true, node: true },
        LOGRATE : 10
    }
}

let custommethods = {
    initializeGrid : initializeGrid
}

let sim = new CPM.Simulation( config, custommethods)
sim.run()

function initializeGrid(){

    // add the GridManipulator if not already there and if you need it
    if( !this.helpClasses["gm"] ){ this.addGridManipulator() }

    let num_cells = 75

    var ni = 0
    for(ni = 0; ni < num_cells; ni++){this.gm.seedCell(1)}

    let radius = 5
    let num_obstacles = 4

    let side_i = 250
    let side_j = 250
    var i = 0
    var j = 0

    for(i = side_i/num_obstacles; i < side_i; i += (side_i/num_obstacles)){
        for(j = side_i/num_obstacles; j < side_j; j += (side_j/num_obstacles)){
            let circ = this.gm.makeCircle( [Math.round(i),Math.round(j)], radius )
            this.gm.assignCellPixels( circ, 2)
        }
    }
}

