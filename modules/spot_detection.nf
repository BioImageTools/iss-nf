#!/usr/bin/env nextflow

params.imageDir = '/path/to/Tiledimages'
params.outputDir = '/path/to/SpotDetection_results'

process SpotDetection {

    input:
    file image from "${params.imageDir}/anchor_dots/*_tiled.tif"

    output:
    path "${params.outputDir}/coordinates.csv" into spotDetectionOutput

    script:
    """
    mkdir -p ${params.outputDir}

    python spot_detection.py ${image} ${params.outputDir}/coordinates.csv
    """
}

workflow {
    TILING(inputDir: params.imageDir, outputDir: params.outputDir, tileSize: params.tileSize)
    SpotDetection(imageDir: params.outputDir)
}

