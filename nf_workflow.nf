#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { MAKE_EXP_JSON } from './modules/experiment_json.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'
include { TILING } from './modules/tiler.nf'
include { SPACETX } from './modules/spacetx.nf'
include { TILE_PICKER } from './modules/tile_picker.nf'
include { SPOT_FINDER as SPOT_FINDER1 } from './modules/decoding.nf'
include { THRESHOLD_FINDER } from './modules/threshold_finder.nf'
include { SPOT_FINDER as SPOT_FINDER2 } from './modules/decoding.nf'
include { POSTCODE_DECODER } from './modules/postcode_decoding.nf'
include { JOIN_COORDINATES } from './modules/join_coords.nf'

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

workflow {
    // Create tuple with round ID and channels to Register:
    
    movingLearn_ch = Channel
        .fromPath(params.inputMovImagesLearnPath)
        .map{ f ->
            sampleID = f.baseName
            return [sampleID[0,1], f]
         }

    // Learn transformations and save TXT files with output;
    // Make parameter metadata channel:
    params_reg_ch = Channel.fromPath(params.elastix_parameter_files)
        .toSortedList()
    learnTransformation_ch = LEARN_TRANSFORM(movingLearn_ch, params.inputRefImagePath, params.rescale_factor, params_reg_ch)

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

    // Estimate tile size based on the registered anchor image:
    tile_metadata_ch = TILE_SIZE_ESTIMATOR(Channel.fromPath(params.inputRefImagePath))
    size_ch = tile_metadata_ch[1]
        .map { it ->
            it.baseName}

    // To use later for the DECODING_POSTCODE process:
    coordinates_csv = tile_metadata_ch[2]

    total_fovs_ch = tile_metadata_ch[0]
        .splitText()
        .map { it -> it.trim() }

    // Add tile size as third argument for the input:
    redefined_merged_ch_tile = redefined_merged_ch
        .combine(size_ch)
        .combine(Channel.fromPath(params.ExpMetaJSON))

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
    //grouped_input.view()
    
    spacetx_out_tuple = SPACETX(grouped_input)
    //spacetx_out_tuple[1].view()
    spacetx_out = spacetx_out_tuple[0]
    // Collect all the output from SpaceTx for feeding the following parts:
    
    all_spacetx_files = spacetx_out
        .map {it ->
            it[1]}
        .flatten()

    //redefined_merged_ch_tile.view()

    // Join all spacetx files with codebook and experiment JSONs:
    exp_json_ch = MAKE_EXP_JSON(params.ExpMetaJSON)

    exp_plus_codebook = Channel.fromPath(params.CodeJSON)
        .mix(exp_json_ch)

    tuple_with_all = all_spacetx_files
        .mix(exp_plus_codebook)
        .toList()

    //tuple_with_all.view()
    // Automatic threshold detection:
    // Select random tiles:
    tile_picker = TILE_PICKER(tuple_with_all, Channel.of('5'))
    tiles = tile_picker
        .splitText()
        .map{it ->
            it[0..6]
            }
    // Generate Thresholds but first Define parameters
    def min_thr = 0.08
    def max_thr = 0.1
    def n_vals = 2

    def increment = (Math.log10(max_thr) - Math.log10(min_thr)) / (n_vals - 1)
    def thresholds = (0..<n_vals).collect { Math.pow(10, Math.log10(min_thr) + it * increment) }

    all_thresholds = Channel.of(thresholds)
                     .flatten()

    fov_and_threshold_ch = tiles.combine(thresholds)
    only_fov_ch = fov_and_threshold_ch.map{ it -> it[0] }
    only_thr_ch = fov_and_threshold_ch.map{ it -> it[1] }

    decoding_results = SPOT_FINDER1(tuple_with_all, only_fov_ch, only_thr_ch)
    starfish_tables = decoding_results[1].toList()
    //detected_spots_ch = spots_detected_ch[0].toList()
    
    //starfish_tables = spots_detected_ch[1].toList()
    //starfish_tables.view()
    // starfish_tables.view()
    
    // starfish_thresh = spots_detected_ch[2].toList()
    // starfish_thresh.view()
    
    picked_threshold = THRESHOLD_FINDER(starfish_tables).splitText().map{ it -> it.trim()}

    spots_detected_ch = SPOT_FINDER2(tuple_with_all, total_fovs_ch, picked_threshold)
    //spots_detected_ch[1].view()
    sorted_detected_spots_ch = spots_detected_ch[0].toSortedList()
    
    sorted_starfish_tables = spots_detected_ch[1].toSortedList()
    //sorted_starfish_tables.view()
    
    postcode_results = POSTCODE_DECODER(
        Channel.fromPath(params.ExpMetaJSON),
        Channel.fromPath(params.CodeJSON),
        sorted_detected_spots_ch
    )
}
