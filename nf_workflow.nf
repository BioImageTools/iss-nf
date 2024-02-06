#!/usr/bin/env nextflow

//params.inputMovImagesLearnPath = "/scratch/segonzal/Sergio/Matias/Stitched/r{2,3,4}_DAPI.tif"

<<<<<<< HEAD
include { LEARN_TRANSFORM } from './modules/registration.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'

=======
include { LEARN_TRANSFORM; APPLY_TRANSFORM } from './modules/registration.nf'
>>>>>>> 601180358f3b66f20d171fa1ebd72cfd447e4f2a

workflow {
    movingLearn_ch = Channel
        .fromPath(params.inputMovImagesLearnPath)
        .map{ f ->
            sampleID = f.baseName
            return [sampleID[0,1], f]
         }

    // Learn transformations and save TXT files with output:
<<<<<<< HEAD
    LEARN_TRANSFORM(movingLearn_ch)
    
    // Estimate tile size based on the registered anchor image:
    TILE_SIZE_ESTIMATOR APPLY_TRANSFORM.out
=======
    learnTransformation_ch = LEARN_TRANSFORM(movingLearn_ch)
    learnTransformation_ch.view()

    // Define the channel with data for which to apply found transformations:
    moving_ch = Channel
        .fromPath(params.movingImagesApplyPath)
        .map { it -> 
            [it.baseName[0,1], it]}

    // Use previous channel and LEARN_TRANSFORM output to apply transformations based on 
    // the SampleID for combining both channels:
    registered_out_ch = APPLY_TRANSFORM(learnTransformation_ch.combine(moving_ch, by:0))
>>>>>>> 601180358f3b66f20d171fa1ebd72cfd447e4f2a

}