#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { TILING } from './modules/tiler.nf'
include { SPACETX } from './modules/spacetx.nf'
include { JOIN_JSON } from './modules/join_json.nf'
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
         
     // Combine the elastix parameter files
     txt_files = Channel.fromPath("${params.elastix_parameter_files}/*.txt")
     txt_combined = txt_files.flatten().toList()
     //txt_combined.view()

    // Learn transformations and save TXT files with output:
    learnTransformation_ch = LEARN_TRANSFORM(movingLearn_ch, params.inputRefImagePath, txt_combined)

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
    //renamed_registered_out_ch.view()

    // Normalized the missing images:
    missing_round = Channel
        .fromPath(params.inputUntransformedImagesPath)
        .map { it ->
            [it.baseName, it]
        }

    missing_round_norm = NORMALIZE(missing_round)
    merged_channel = missing_round_norm.mix(renamed_registered_out_ch)

    // Make function to redefine sampleID:

    // Use function 'filter_channel' to change 'merged_channel' ids:
    redefined_merged_ch = merged_channel
        .map { it ->
            [filter_channel(it[0]), it[1]]}

    //redefined_merged_ch.view()
    // TILING PART:
    tiled_ch = TILING(redefined_merged_ch)
    //tiled_ch[0].view()

    // To do: merge 'coordinates-fov*'
    joined_coords_ch = tiled_ch[1].groupTuple()

    //joined_coords_ch.view()

    /*
    joined_coords_ch
        .collectFile(keepHeader: true)
        .view()
    */

    // joined_coords_ch.collect().view()
    //joined_coords_ch.view()
    coords4spacetx = JOIN_COORDINATES(joined_coords_ch)
    //coords4spacetx.view()

    //collected_tiles = tiled_ch[0].collect()
    //collected_tiles.view()
    grouped_tiled_images = tiled_ch[0].groupTuple()
    //grouped_tiled_images.view()
    // Flatten the files on the tuple:
    grouped_tiled_images_flat = grouped_tiled_images
        .map { it ->
            [it[0], it[1].flatten()]}
    //grouped_tiled_images_flat.view()
    grouped_input = grouped_tiled_images_flat.combine(coords4spacetx, by: 0)
    //grouped_input.view()
    spacetx_out = SPACETX(grouped_input)
    // Collect all the output from SpaceTx for feeding the following parts:
    all_spacetx_files = spacetx_out
        .map {it ->
            it[1]}
        .flatten()
    //all_spacetx_files.view()

    all_spacetx_json = spacetx_out
        .map {it ->
            it[2]}
        .toList()     
    //all_spacetx_json.view()
    
    // Merge json files
    merge_json = JOIN_JSON(all_spacetx_json)
    merge_json.view()
    
    /*
    ex = Channel.fromPath(params.bothJSON)

    tuple_with_all = all_spacetx_files
        .mix(ex)
        .toList()
    //    .flatten()
    //    .toList()

    //tuple_with_all.view()
    spots_detected_ch = SPOT_FINDER(tuple_with_all, params.fov)
    spots_detected_ch.view()
    */
}