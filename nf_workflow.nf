#!/usr/bin/env nextflow

//params.inputMovImagesLearnPath = "/scratch/segonzal/Sergio/Matias/Stitched/r{2,3,4}_DAPI.tif"

include { LEARN_TRANSFORM; APPLY_TRANSFORM } from './modules/registration.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'

workflow {
    movingLearn_ch = Channel
        .fromPath(params.inputMovImagesLearnPath)
        .map{ f ->
            sampleID = f.baseName
            return [sampleID[0,1], f]
         }

    // Learn transformations and save TXT files with output:
    learnTransformation_ch = LEARN_TRANSFORM(movingLearn_ch)

    // Estimate tile size based on the registered anchor image:
    size_ch = TILE_SIZE_ESTIMATOR(params.inputRefImagePath)

    // Define the channel with data for which to apply found transformations:
    moving_ch = Channel
        .fromPath(params.movingImagesApplyPath)
        .map { it -> 
            [it.baseName[0,1], it]}

    // Use previous channel and LEARN_TRANSFORM output to apply transformations based on 
    // the SampleID for combining both channels:
    registered_out_ch = APPLY_TRANSFORM(learnTransformation_ch.combine(moving_ch, by:0))

}
