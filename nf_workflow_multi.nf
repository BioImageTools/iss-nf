#!/usr/bin/env nextflow

//include { LEARN_TRANSFORM; APPLY_TRANSFORMS; NORMALIZE } from './modules/registration_module_phase_cross_correlation.nf'
include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { SPOT_DETECTOR } from './modules/spot_detector_module.nf'
include { NUCLEI_SEGMENTATION } from './modules/segmentation.nf'
include { ASSIGN_SPOTS } from './modules/spot_assignment_module.nf'

process JOIN_RESULTS {
    publishDir "Final_Results", mode: 'copy', overwrite: true
    debug true 

    input:
    file x

    output:
    file("combined_results.csv")

    script:
    """
    touch combined_results.csv
    echo y,x,r,gene > combined_results.csv
    cat $x >> combined_results.csv
    """
}

workflow {
    // The following channel creates a tuple of sampleID, samplePATH for the moving images to find the registration:
    movingLearn_ch = Channel
        .fromPath(params.inputMovImagesLearnPath)
        .map{ f ->
            sampleID = f.baseName
            return [sampleID[0,1], f]
         }

    // The transformations are learned and and saved:
    // Make parameter metadata channel:
    params_reg_ch = Channel.fromPath(params.elastix_parameter_files)
        .toSortedList()
    //params_reg_ch.view()
    learnTransformation_ch = LEARN_TRANSFORM(movingLearn_ch, params.inputRefImagePath, params_reg_ch)
    learnTransformation_ch.view()
    
    // Define the channel with data for which to apply found transformations:
    moving_ch = Channel
        .fromPath(params.movingImagesApplyPath)
        .map { it -> 
            [it.baseName[0,1], it]}

    // Use previous channel and LEARN_TRANSFORM output to apply transformations based on 
    // the SampleID for combining both channels:

    registered_out_ch = APPLY_TRANSFORM(moving_ch.combine(learnTransformation_ch, by:0))
    /*
    // Filter the primary channels for spot detection from the APPLY_TRANSFORM output:
    onlyTransformedPrimary_ch = registered_out_ch
        .map { it -> 
            def channel = it[1].baseName.split('_')[2]
            if (channel != 'DAPI') {
                return [it[0] + '_' + channel, it[1]]
            }
        }

    // Create sampleID, samplePATH for images that were not transformed (in this case round 1):
    missing_round = Channel
        .fromPath(params.inputUntransformedImagesPath)
        .map { it ->
            [it.baseName, it]
        }


    missing_round_norm = NORMALIZE(missing_round)
    merged_channel = missing_round_norm.mix(onlyTransformedPrimary_ch)

 
    detectedSpots_ch = SPOT_DETECTOR(merged_channel, params.log_threshold)

    // Following lines merge the CSV results from the detection process:
    detectedSpotsFiles = detectedSpots_ch
        .map { it -> 
                it[1]
        }

    merged_ch = detectedSpotsFiles
        .collectFile(name: "final_results.csv")


    spots_coordinates_ch = JOIN_RESULTS(merged_ch)

    // Do DAPI segmentation and expansion using Stardist:
    expanded_mask_ch = NUCLEI_SEGMENTATION(params.inputRefImagePath)

    // Finally, assign spots to individual Nuclei:
    assigned_ch = ASSIGN_SPOTS(spots_coordinates_ch, expanded_mask_ch)
    */
}
