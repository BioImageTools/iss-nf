#!/usr/bin/env nextflow

//params.inputMovImagesLearnPath = "/scratch/segonzal/Sergio/Matias/Stitched/r{2,3,4}_DAPI.tif"

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { LEARN_TRANSFORM; APPLY_TRANSFORM } from './modules/registration.nf'
include { TILING } from './modules/tiler.nf'

workflow {
    // Create tuple with round ID and channels to Register:
    movingLearn_ch = Channel
        .fromPath(params.inputMovImagesLearnPath)
        .map{ f ->
            sampleID = f.baseName
            return [sampleID[0,1], f]
         }

    // Learn transformations and save TXT files with output:
    learnTransformation_ch = LEARN_TRANSFORM(movingLearn_ch, params.inputRefImagePath)
    learnTransformation_ch.view()

    // Define the channel with data for which to apply found transformations:
    moving_ch = Channel
        .fromPath(params.movingImagesApplyPath)
        .map { it -> 
            [it.baseName[0,1], it]}


    // Use previous channel and LEARN_TRANSFORM output to apply transformations based on 
    // the SampleID for combining both channels:
    registered_out_ch = APPLY_TRANSFORM(learnTransformation_ch.combine(moving_ch, by:0))
    
    // Normalized the missing images:
    missing_round = Channel
        .fromPath(params.inputUntransformedImagesPath)
        .map { it ->
            [it.baseName, it]
        }

    missing_round_norm = NORMALIZE(missing_round)
    merged_channel = missing_round_norm.mix(registered_out_ch)

    // Next part will include the Tiling

    // Run the tiling:
    tiling_round_channel_ch = TILING(registered_out_ch, params.tile_size)
}