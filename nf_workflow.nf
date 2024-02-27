#!/usr/bin/env nextflow
nextflow.enable.dsl=2


include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { TILING } from './modules/tiler.nf'
include { SPACETX } from './modules/spacetx.nf'
include { SPOT_FINDER } from './modules/decoding.nf'

def filter_channel(image_id) {
    if (image_id.contains('anchor_dots')) {
        return 'anchor_dots'
    } else if (image_id.contains('anchor_nuclei')) {
        return 'anchor_nuclei'
    } else if (image_id.contains('_DAPI')) {
        return 'nuclei'
    } else {
        return 'primary'
    }
}

process JOIN_COORDINATES {
    //publishDir "JoinedCoords", mode: "copy", overwrite: true
    //debug true

    input:
    tuple val(image_type), path(x)

    output:
    //stdout
    tuple val(image_type), file("*.csv")

    script:
    """
    python ${workflow.projectDir}/bin/join_coordinates.py join $x
    """
}

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

    // Define the channel with data for which to apply found transformations:
    moving_ch = Channel
        .fromPath(params.movingImagesApplyPath)
        .map { it -> 
            [it.baseName[0,1], it]
            }


}
