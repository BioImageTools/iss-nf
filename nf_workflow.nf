#!/usr/bin/env nextflow

//params.inputMovImagesLearnPath = "/scratch/segonzal/Sergio/Matias/Stitched/r{2,3,4}_DAPI.tif"

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'
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
    debug true

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

    // Estimate tile size based on the registered anchor image:
    tile_metadata_ch = TILE_SIZE_ESTIMATOR(Channel.fromPath(params.inputRefImagePath))
    size_ch = tile_metadata_ch[1]
        .splitJson()

    total_fovs_ch = tile_metadata_ch[0]
        .splitText()

    // Define the channel with data for which to apply found transformations:
    moving_ch = Channel
        .fromPath(params.movingImagesApplyPath)
        .map { it -> 
            [it.baseName[0,1], it]}

    // Use previous channel and LEARN_TRANSFORM output to apply transformations based on 
    // the SampleID for combining both channels:
    registered_out_ch = APPLY_TRANSFORM(learnTransformation_ch.combine(moving_ch, by:0))
    // Prepare data for tiling by taking the whole name as the sampleID:

    renamed_registered_out_ch = registered_out_ch
        .map{it -> [it[1].baseName, it[1]]}

    // Normalized the missing images:
    missing_round = Channel
        .fromPath(params.inputUntransformedImagesPath)
        .map { it ->
            [it.baseName, it]
        }

    missing_round_norm = NORMALIZE(missing_round)
    merged_channel = missing_round_norm.mix(renamed_registered_out_ch)

    // Use function 'filter_channel' to change 'merged_channel' id's and
    // identify path by image type (primary, nuclei, etc). 
    redefined_merged_ch = merged_channel
        .map { it ->
            [filter_channel(it[0]), it[1]]}

    // Add tile size as third argument for the input:
    redefined_merged_ch_tile = redefined_merged_ch
        .combine(size_ch)

    // TILING PART:
    tiled_ch = TILING(redefined_merged_ch_tile)

    joined_coords_ch = tiled_ch[1].groupTuple()

    coords4spacetx = JOIN_COORDINATES(joined_coords_ch)

    grouped_tiled_images = tiled_ch[0].groupTuple()

    // Flatten the files on the tuple so they can be seen by the SPACETX process
    // as a single folder with the working directory:
    grouped_tiled_images_flat = grouped_tiled_images
        .map { it ->
            [it[0], it[1].flatten()]}

    grouped_input = grouped_tiled_images_flat.combine(coords4spacetx, by: 0)
    
    spacetx_out = SPACETX(grouped_input)
    // Collect all the output from SpaceTx for feeding the following parts:
    
    all_spacetx_files = spacetx_out
        .map {it ->
            it[1]}
        .flatten()

    // Join all spacetx files with codebook and experiment JSONs:
    ex = Channel.fromPath(params.bothJSON)

    tuple_with_all = all_spacetx_files
        .mix(ex)
        .toList()

    spots_detected_ch = SPOT_FINDER(tuple_with_all, total_fovs_ch)
    spots_detected_ch.view()
}
