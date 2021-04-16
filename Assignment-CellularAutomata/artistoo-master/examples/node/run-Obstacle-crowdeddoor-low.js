/* Source the CPM module (cpm-cjs version because this is a node script).*/
let CPM = require("../../build/artistoo-cjs.js")

let config = {

    // Grid settings
    ndim: 2,
    field_size: [350, 250],

    // CPM parameters and configuration
    conf: {
        torus: [false, false],
        seed: 10,
        T: 20,                                // CPM temperature

        // Adhesion parameters:
        J: [[0, 0, 0], [0, 0, 0], [0, 20, 0]],

        // VolumeConstraint parameters
        LAMBDA_V: [0, 50, 200],                // VolumeConstraint importance per cellkind
        V: [0, 300, 200],                    // Target volume of each cellkind
        LAMBDA_P: [0, 2, 100],
        P : [0, 250, 170],
        LAMBDA_ACT : [0,100,0],
        MAX_ACT : [0,80,0],
        ACT_MEAN : "geometric"
    },
    // Simulation setup and configuration
    simsettings: {
        // Cells on the grid
        NRCELLS: [0,0],                    // Number of cells to seed for all
        // non-background cellkinds.
        
        BURNIN : 500,
        RUNTIME: 5000,                  // Only used in node

        CANVASCOLOR: "eaecef",
        CELLCOLOR: ["000000", "FF0000"],
        ACTCOLOR: [true, false],
        SHOWBORDERS: [true, true],
        BORDERCOL: ["00FF00", "0000FF"],
        zoom: 2,                        // zoom in on canvas with this factor.
        
        SAVEIMG : true,
        IMGFRAMERATE: 1,
        SAVEPATH : "output/img/Obstacle-crowdeddoor-low",    // ... And save the image in this folder.
        EXPNAME : "Obstacle-crowdeddoor-low",                    // Used for the filename of output images.
        STATSOUT : { browser: true, node: true },
        LOGRATE : 10
    }
}

let custommethods = {
    initializeGrid : initializeGrid
}

let sim = new CPM.Simulation( config , custommethods )

let Cdir = new CPM.AttractionPointConstraint({
    LAMBDA_ATTRACTIONPOINT: [0, 100, 0],
    ATTRACTIONPOINT: [[0, 0], [sim.C.extents[0] / 3 + sim.C.extents[0] / 2, sim.C.extents[1] / 2]]
})
sim.C.add(Cdir)

function initializeGrid() {

    // add the initializer if not already there
    if (!this.helpClasses["gm"]) { this.addGridManipulator() }
    let step = 8
    for (var i = 1; i < this.C.extents[1]; i += step) {
        if (i < this.C.extents[1] / 2 - 12 || i > this.C.extents[1] / 2 + 12) {
            this.gm.seedCellAt(2, [this.C.extents[0] / 2, i])
        }
    }
    this.gm.seedCellAt(1, [10, 90])
    this.gm.seedCellAt(1, [20, 90])
    this.gm.seedCellAt(1, [30, 90])
    this.gm.seedCellAt(1, [40, 90])
    this.gm.seedCellAt(1, [50, 90])
    this.gm.seedCellAt(1, [60, 90])
    this.gm.seedCellAt(1, [10, 110])
    this.gm.seedCellAt(1, [20, 110])
    this.gm.seedCellAt(1, [30, 110])
    this.gm.seedCellAt(1, [40, 110])
    this.gm.seedCellAt(1, [50, 110])
    this.gm.seedCellAt(1, [60, 110])
    this.gm.seedCellAt(1, [10, 100])
    this.gm.seedCellAt(1, [20, 100])
    this.gm.seedCellAt(1, [30, 100])
    this.gm.seedCellAt(1, [40, 100])
    this.gm.seedCellAt(1, [50, 100])
    this.gm.seedCellAt(1, [60, 100])
}



sim.run()


