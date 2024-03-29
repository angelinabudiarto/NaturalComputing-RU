/* Source the CPM module (cpm-cjs version because this is a node script).*/
let CPM = require("../../build/artistoo-cjs.js")

let config = {

    // Grid settings
    ndim: 2,
    field_size: [250, 250],

    // CPM parameters and configuration
    conf: {
        torus : [true, true],
        seed : 2021,
        T: 20,                                // CPM temperature

        // Adhesion parameters:
        J: [[0, 20, 20], [20, 0, 20], [20, 20, 0]],

        // VolumeConstraint parameters
        LAMBDA_V: [0, 50, 200],                // VolumeConstraint importance per cellkind
        V: [0, 500, 250],                    // Target volume of each cellkind

        LAMBDA_P: [0, 2, 100],
        P : [0, 340, 80],

        LAMBDA_ACT : [0,100,0],
        MAX_ACT : [0,80,0],
        ACT_MEAN : "geometric"


    },
    
    // Simulation setup and configuration
    simsettings: {
        // Cells on the grid
        NRCELLS: [5,5],                    // Number of cells to seed for all
        // non-background cellkinds.
        
        BURNIN : 50,
        RUNTIME: 5000,                  // Only used in node

        CANVASCOLOR: "eaecef",
        CELLCOLOR: ["000000", "FF0000"],
        ACTCOLOR: [true, false],
        SHOWBORDERS: [true, true],
        BORDERCOL: ["00FF00", "0000FF"],
        zoom: 2,                        // zoom in on canvas with this factor.
        
        SAVEIMG : true,
        IMGFRAMERATE: 1,
        SAVEPATH : "output/img/Obstacle-start-circular",    // ... And save the image in this folder.
        EXPNAME : "Obstacle-start-circular",                    // Used for the filename of output images.
        STATSOUT : { browser: true, node: true },
        LOGRATE : 10
    }
}

let sim = new CPM.Simulation( config )
sim.run()



