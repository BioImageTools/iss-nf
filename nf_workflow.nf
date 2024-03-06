#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { TILING } from './modules/tiler.nf'
include { SPACETX } from './modules/spacetx.nf'
include { JOIN_JSON } from './modules/join_json.nf'
include { SPOT_FINDER } from './modules/decoding.nf'
include { TILE_PICKER } from './modules/tile_picker.nf'
include { THRESHOLD_FINDER } from './modules/threshold_finder.nf'
include { TILE_INTENSITY } from './modules/tile_intensity.nf'


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

    all_spacetx_tiff = spacetx_out
        .map {it ->
            it[2]}
        //.collect()
        .flatten()
    //all_spacetx_tiff.view()

    
    all_spacetx_anchorDots = all_spacetx_tiff
        //.filter (~/^anchor_dots-fov.*/ )
        //.flatten()
        //.filter { file ->
        //file.contains("anchor_dots-fov")
        //}
        .filter { file -> file =~ /anchor_dots/ }
        .flatten()
        //.groupTuple()
    //all_spacetx_anchorDots.view()
    
    
    // Merge json files
    //merge_json = JOIN_JSON(all_spacetx_json)
    //merge_json.view()
    
    // Tile Picker
    rnd_tiles = all_spacetx_anchorDots.randomSample(5)
    //rnd_fov = rnd_tiles
    //    .filter { file ->
    //    def match = file =~ /anchor_dots-fov_([0-9]+)-/
    //    if (match) {
    //        return match[0][1]
    //    }
    //    return null
    //}.collect().first()
    //println rnd_fov

    intensities = TILE_INTENSITY(rnd_tiles)
    //intensities.view()
    
    max_intensity = intensities.map { file ->
        script:
        """
        content = cat ${file}
        number = content.toInteger()
        println number
        """
        }
    max_intensity.view()
    
                    //.max {  }
    //max_intensity.view()
    
    
    //all_tilePicker = TILE_PICKER(all_spacetx_anchorDots)
    
    /*   
    // Auto Threshold finder
    thresholds = all_tilePicker
    .map {it ->
        it[1]}
    .toList()  
    thresholds.view()
    
    picked_tile = all_tilePicker
    .map {it ->
        it[0]}
    .toList()  
    picked_tile.view()
    

    //SPOT_FINDER ...
    tuple_with_all = all_spacetx_files
    .mix(ex)
    .toList()
    spots_detected_ch = SPOT_FINDER(tuple_with_all, picked_tile, thresholds)
    sorted_detected_spots_ch = spots_detected_ch[0].toSortedList()
    
    sorted_starfish_tables = spots_detected_ch[1].toSortedList()
    //sorted_starfish_tables.view()
    picked_threshold = THRESHOLD_FINDER(thresholds, sorted_starfish_tables)
    
    spots_detected_ch = SPOT_FINDER(tuple_with_all, total_fovs_ch, picked_threshold)
    //spots_detected_ch[1].view()
    sorted_detected_spots_ch = spots_detected_ch[0].toSortedList()
    
    sorted_starfish_tables = spots_detected_ch[1].toSortedList()
    //sorted_starfish_tables.view()
    
    postcode_results = POSTCODE_DECODER(
        Channel.fromPath(params.CodeJSON),
        sorted_detected_spots_ch
    )
    */
}