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
    } else if (image_id.contains('_DAPI')) {
        return 'nuclei'
    } else {
        return 'primary'
    }
}

workflow {
    
/*     println "PoSTcode activation: ${params.PoSTcode}"

    // Define tuple of round ID and file path for moving images:
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

    regImg_path = registered_out_ch
        .map{it -> [it[1]]}
        .collect()

    anch_path = missing_round_norm
        .map{it -> [it[1]]}
        .collect()

    reg_qc_inputs = regImg_path.combine(
        Channel.fromPath(params.inputMovImagesLearnPath).toList())
        .combine(Channel.fromPath(params.inputRefImagePath).combine(anch_path))

    reg_html = REGISTER_QC(reg_qc_inputs)
 
    // Estimate tile size based on the registered anchor image:
    tile_metadata_ch = TILE_SIZE_ESTIMATOR(Channel.fromPath(params.inputRefImagePath))
    tile_html = tile_metadata_ch[2]
    size_ch = tile_metadata_ch[1]
            .map { it ->
        it.baseName}

    // To use later for the DECODING_POSTCODE process:
    // coordinates_csv = tile_metadata_ch[2]

    total_fovs_ch = tile_metadata_ch[0]
        .splitText()
        .map { it -> it.trim() }
 
    // Add tile size as third argument for the input:
    redefined_merged_ch_tile = redefined_merged_ch
        .combine(size_ch)
        .combine(Channel.fromPath(params.ExpMetaJSON))

    // TILING PART:
    tiled_ch = TILING(redefined_merged_ch_tile)

    // To do: merge 'coordinates-fov*'
    joined_coords_ch = tiled_ch[1].groupTuple()
    
    coords4spacetx = JOIN_COORDINATES(joined_coords_ch)

    grouped_tiled_images = tiled_ch[0].groupTuple()
    
    // Flatten the files on the tuple:
    grouped_tiled_images_flat = grouped_tiled_images
        .map { it ->
            [it[0], it[1].flatten()]}
    
    //grouped_tiled_images_flat.view()
    grouped_input = grouped_tiled_images_flat.combine(coords4spacetx, by: 0)
    
    spacetx_out = SPACETX(grouped_input)
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
    
    tile_picker = TILE_PICKER(tuple_with_all, Channel.of('5'))
    tiles = tile_picker
            .splitText()
            .map{it ->
                it[0..6]
                }
    
    // Generate Thresholds but first Define parameters
    def min_thr = 0.008
    def max_thr = 0.01
    def n_vals = 3
    def increment = (Math.log10(max_thr) - Math.log10(min_thr)) / (n_vals - 1)
    def thresholds = (0..<n_vals).collect { Math.pow(10, Math.log10(min_thr) + it * increment) }
        
    merge_tiles_thresh = tiles.combine(thresholds)
    merge_tiles_thresh_tile = merge_tiles_thresh.map{
                    it -> it[0]
                }
    merge_tiles_thresh_thresh = merge_tiles_thresh.map{
                    it -> it[1]
                }
    
    spots_detected_ch = SPOT_FINDER_1(tuple_with_all, merge_tiles_thresh_tile, merge_tiles_thresh_thresh)
        
    starfish_tables = spots_detected_ch[1].toList() 

    threshold_results = THRESHOLD_FINDER(starfish_tables)
   picked_threshold = threshold_results[0].splitText()
    picked_threshold_html = threshold_results[1]

    fov_and_threshold_ch = total_fovs_ch.combine(picked_threshold)

    only_thr_ch = fov_and_threshold_ch.map{ it -> it[1] }
    spots_detected_ch = SPOT_FINDER_2(tuple_with_all, total_fovs_ch, only_thr_ch)
    sorted_detected_spots_ch = spots_detected_ch[0].toSortedList() 

    sorted_starfish_tables = spots_detected_ch[1].toSortedList()
    postCode_input = CONCAT_NPY(sorted_detected_spots_ch)
    // postCode.view()
    starfish_table = CONCAT_CSV(sorted_starfish_tables)
    
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
    ch_all_html_files = reg_html.merge(tile_html).merge(decoder_html).merge(picked_threshold_html)
    MERGE_HTML(ch_all_html_files)  */
    postcode_results = Channel.fromPath('/hpc/scratch/hdd3/nv066607/work2/f2/a1a4dfdb790ba8d80c406613b464da/postcode_starfish_output.csv')
    DECODER_QC_PoSTcode(postcode_results)
}
