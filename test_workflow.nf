params.movingImagesApplyPath = "/scratch/segonzal/Sergio/Matias/Stitched/r{2,3,4}_*.tif"


moving_ch = Channel
    .fromPath(params.movingImagesApplyPath)
    .map { it -> 
        [it.baseName[0,1], it]}

moving_ch.view()