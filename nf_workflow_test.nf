#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { TILING } from './modules/tiler.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'
include { SPACETX } from './modules/spacetx.nf'
include { JOIN_JSON } from './modules/join_json.nf'
include { MAKE_EXP_JSON } from './modules/experiment_json.nf'
include { SPOT_FINDER as SPOT_FINDER1 } from './modules/decoding.nf'
include { SPOT_FINDER as SPOT_FINDER2 } from './modules/decoding.nf'
include { TILE_PICKER } from './modules/tile_picker.nf'
include { THRESHOLD_FINDER } from './modules/threshold_finder.nf'
include { POSTCODE_DECODER } from './modules/postcode_decoding.nf'


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
    
    // Join all spacetx files with codebook and experiment JSONs:
    exp_json_ch = MAKE_EXP_JSON(params.ExpMetaJSON)

    exp_plus_codebook = Channel.fromPath(params.CodeJSON)
        .mix(exp_json_ch)

    tuple_with_all = all_spacetx_files
        .mix(exp_plus_codebook)
        .toList()
    
    tile_picker = TILE_PICKER(tuple_with_all, Channel.of('5'))
    tiles = tile_picker
            .splitText()
            .map{it ->
                it[0..6]
                }
    //        .view()
    
    // Generate Thresholds but first Define parameters
    def min_thr = 0.08
    def max_thr = 0.1
    def n_vals = 2 //10

    def increment = (Math.log10(max_thr) - Math.log10(min_thr)) / (n_vals - 1)
    def thresholds = (0..<n_vals).collect { Math.pow(10, Math.log10(min_thr) + it * increment) }

    all_thresholds = Channel.of(thresholds)
                     .flatten()
    //                .view()
       
    // Estimate tile size based on the registered anchor image:
    tile_metadata_ch = TILE_SIZE_ESTIMATOR(Channel.fromPath(params.inputRefImagePath))
    size_ch = tile_metadata_ch[1]
        .splitText()

    total_fovs_ch = tile_metadata_ch[0]
        .splitText()
        .map{
            it -> it.replaceAll("\\s", "")
        }
        
    merge_tiles_thresh = tiles.combine(thresholds)//.view()
    merge_tiles_thresh_tile = merge_tiles_thresh.map{
                    it -> it[0]
                }//.view()
    merge_tiles_thresh_thresh = merge_tiles_thresh.map{
                    it -> it[1]
                }//.view()
    
    spots_detected_ch = SPOT_FINDER1(tuple_with_all, merge_tiles_thresh_tile, merge_tiles_thresh_thresh)
    
    //detected_spots_ch = spots_detected_ch[0].toList()
    
    starfish_tables = spots_detected_ch[1].toList()
    // starfish_tables.view()
    
    // starfish_thresh = spots_detected_ch[2].toList()
    // starfish_thresh.view()
        
    picked_threshold = THRESHOLD_FINDER(starfish_tables).splitText()

    spots_detected_ch = SPOT_FINDER2(tuple_with_all, total_fovs_ch, picked_threshold)
    spots_detected_ch[1].view()
    sorted_detected_spots_ch = spots_detected_ch[0].toSortedList()
    
    sorted_starfish_tables = spots_detected_ch[1].toSortedList()
    sorted_starfish_tables.view() 
    
    postcode_results = POSTCODE_DECODER(
        Channel.fromPath(params.ExpMetaJSON),
        Channel.fromPath(params.CodeJSON),
        sorted_detected_spots_ch
     )
}