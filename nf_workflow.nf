#!/usr/bin/env nextflow

params.inputMovImagesLearnPath = "/scratch/segonzal/Sergio/Matias/Stitched/r{2,3,4}_DAPI.tif"

include { LEARN_TRANSFORM } from './modules/registration.nf'

workflow {
    movingLearn_ch = Channel
        .fromPath(params.inputMovImagesLearnPath)
        .map{ f ->
            sampleID = f.baseName
            return [sampleID[0,1], f]
         }

    // Learn transformations and save TXT files with output:
    LEARN_TRANSFORM(movingLearn_ch)
}