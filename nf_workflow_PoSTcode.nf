#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { REGISTER_QC } from './modules/register_qc.nf'
include { TILING } from './modules/tiler.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'
include { SPACETX } from './modules/spacetx.nf'
include { JOIN_JSON } from './modules/join_json.nf'
include { MAKE_EXP_JSON } from './modules/experiment_json.nf'
include { SPOT_FINDER as SPOT_FINDER_1 } from './modules/decoding.nf'
include { SPOT_FINDER as SPOT_FINDER_2 } from './modules/decoding.nf'
include { TILE_PICKER } from './modules/tile_picker.nf'
include { THRESHOLD_FINDER } from './modules/threshold_finder.nf'
include { POSTCODE_DECODER } from './modules/postcode_decoding.nf'
include { JOIN_COORDINATES } from './modules/join_coords.nf'
include { DECODER_QC as DECODER_QC_PoSTcode} from './modules/decoder_qc.nf'
include { DECODER_QC as DECODER_QC_Starfish} from './modules/decoder_qc.nf'
include { DECODER_QC as DECODER_QC_PoSTcodeFailed } from './modules/decoder_qc.nf'
include { MERGE_HTML } from './modules/merge_html.nf'
include { CONCAT_CSV } from './modules/concat_csv.nf'
include { CONCAT_NPY } from './modules/concat_npy.nf'


def filter_channel(image_id) {
    if (image_id.contains('anchor_dots')) {
        return 'anchor_dots'
    } else if (image_id.contains('anchor_nuclei')) {
        return 'anchor_nuclei'
    } else if (image_id.contains('nuclei')) {
        return 'nuclei'
    } else {
        return 'primary'
    }
}


workflow {

    // Create coordinates channel tuple for all channel types:
    coords_ch = Channel.fromPath(params.primary_coords)//.map { it -> ['primary', it]}

    all_channel_type_coords = coords_ch.map { it -> [filter_channel(it.baseName), it]}

    // CREATE CHANNEL FOR IMAGES TO COMBINE WITH COORDS:
    input_tiles_tuple = Channel.fromPath(params.tile_images)
        .map { it -> [filter_channel(it.baseName), it]}
    
    grouped_input = input_tiles_tuple
        .groupTuple()
        .combine(all_channel_type_coords, by: 0)
    
    spacetx_out_tuple = SPACETX(grouped_input)
    
    spacetx_out = spacetx_out_tuple[0]
    // Collect all the output from SpaceTx for feeding the following parts:
    
    all_spacetx_files = spacetx_out
        .map {it ->
            it[1]}
        .flatten()

    // Join all spacetx files with codebook and experiment JSONs:
    exp_json_ch = MAKE_EXP_JSON(params.ExpMetaJSON)
    
    exp_plus_codebook = Channel.fromPath(params.CodeJSON)
        .mix(exp_json_ch)

    tuple_with_all = all_spacetx_files
        .mix(exp_plus_codebook)
        .toList()
    
    // Automatic threshold detection:
    // Select random tiles:
    tile_picker = TILE_PICKER(tuple_with_all, Channel.of('5'))
    tiles = tile_picker
        .splitText()
        .map{it ->
            it[0..6]
            }
    
    // Generate Thresholds but first Define parameters
    def min_thr = 0.005
    def max_thr = 0.009
    def n_vals = 10

    def increment = (Math.log10(max_thr) - Math.log10(min_thr)) / (n_vals - 1)
    def thresholds = (0..<n_vals).collect { Math.pow(10, Math.log10(min_thr) + it * increment) }

    all_thresholds = Channel.of(thresholds)
                     .flatten()

    fov_and_threshold_ch = tiles.combine(thresholds)
    only_fov_ch = fov_and_threshold_ch.map{ it -> it[0] }
    only_thr_ch = fov_and_threshold_ch.map{ it -> it[1] }

    decoding_results = SPOT_FINDER_1(tuple_with_all, only_fov_ch, only_thr_ch)
    starfish_tables = decoding_results[1].toList()
    
    threshold_results = THRESHOLD_FINDER(starfish_tables) 
    picked_threshold = threshold_results[0].splitText()
    picked_threshold_html = threshold_results[1]

    total_fovs_ch = Channel.fromPath(params.fovs2decode).splitText().map { it -> it.trim()}
    fov_and_threshold_ch = total_fovs_ch.combine(picked_threshold)
    only_thr_ch = fov_and_threshold_ch.map{ it -> it[1] }

    spots_detected_ch = SPOT_FINDER_2(tuple_with_all, total_fovs_ch, only_thr_ch)

    sorted_detected_spots_ch = spots_detected_ch[0].toSortedList()
    
    sorted_starfish_tables = spots_detected_ch[1].toSortedList()
    starfish_table = CONCAT_CSV(sorted_starfish_tables)
    postCode_input = CONCAT_NPY(sorted_detected_spots_ch)

    if (params.PoSTcode){
        postcode_results = POSTCODE_DECODER(
            Channel.fromPath(params.CodeJSON),
            starfish_table,
            postCode_input
        ) 
        csv_name = postcode_results.collect {
            it -> it.baseName
        }      
        if (csv_name.contains("postcode_decoding_failed")==true){
            decoder_html = DECODER_QC_PoSTcodeFailed(starfish_table)
        }else{
             decoder_html = DECODER_QC_PoSTcode(postcode_results) 
        }      
    }else{
        decoder_html = DECODER_QC_Starfish(starfish_table)
    }
    
    // Concatenate HTML files from all processes
    // ch_all_html_files = reg_html.merge(tile_html).merge(decoder_html).merge(picked_threshold_html)
    // MERGE_HTML(ch_all_html_files) 
}
