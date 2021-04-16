/* Source the CPM module (cpm-cjs version because this is a node script).*/
let CPM = require("../../build/artistoo-cjs.js")

let config = {

    // Grid settings
    ndim: 2,
    field_size: [250, 250],

    // CPM parameters and configuration
    conf: {
        torus : [true, true],
        seed : 21,
        T: 20,                                // CPM temperature

        // Adhesion parameters:
        J: [[0, 20, 20], [20, 0, 20], [20, 20, 0]],

        // VolumeConstraint parameters
        LAMBDA_V: [0, 50, 200],                // VolumeConstraint importance per cellkind
        V: [0, 500, 150],                    // Target volume of each cellkind

        LAMBDA_P: [0, 2, 500],
        P : [0, 340, 90],

        LAMBDA_ACT : [0,400,0],
        MAX_ACT : [0,80,0],
        ACT_MEAN : "geometric"


    },
    
    // Simulation setup and configuration
    simsettings: {
        // Cells on the grid
        NRCELLS: [0,0],                    // Number of cells to seed for all
        // non-background cellkinds.
        
        BURNIN : 5,
        RUNTIME: 500,                  // Only used in node

        CANVASCOLOR: "eaecef",
        CELLCOLOR: ["000000", "FF0000"],
        ACTCOLOR: [true, false],
        SHOWBORDERS: [true, true],
        BORDERCOL: ["00FF00", "0000FF"],
        zoom: 2,                        // zoom in on canvas with this factor.
        
        SAVEIMG : true,
        IMGFRAMERATE: 1,
        SAVEPATH : "output/img/Obstacle-tunnelspeed",    // ... And save the image in this folder.
        EXPNAME : "Obstacle-tunnelspeed",                    // Used for the filename of output images.
        STATSOUT : { browser: true, node: true },
        LOGRATE : 10
    }
}

let custommethods = {
    initializeGrid : initializeGrid
}

let sim = new CPM.Simulation( config , custommethods )

function initializeGrid(){
                // add the initializer if not already there
                if( !this.helpClasses["gm"] ){ this.addGridManipulator() }
                let step = 8
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [0,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [20,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [45,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [75,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [110,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [150,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [195,i] )
                }
                for( var i = 1 ; i < this.C.extents[0] ; i += step ){
                    this.gm.seedCellAt( 2, [245,i] )
                }
                this.gm.seedCellAt( 1, [10,this.C.extents[1]/2] )
                this.gm.seedCellAt( 1, [33,this.C.extents[1]/2] )
                this.gm.seedCellAt( 1, [60,this.C.extents[1]/2] )
                this.gm.seedCellAt( 1, [93,this.C.extents[1]/2] )
                this.gm.seedCellAt( 1, [130,this.C.extents[1]/2] )
                this.gm.seedCellAt( 1, [172,this.C.extents[1]/2] )
                this.gm.seedCellAt( 1, [220,this.C.extents[1]/2] )
}

sim.run()


