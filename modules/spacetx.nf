#!/usr/bin/env nextflow

params.imageDir = '/path/to/images'
params.outputDir = '/path/to/Tiled_images'

process TILING_SpaceTx {

    input:
    file image from params.imageDir
    val outputDir
    val tileSize

    output:
    path "${outputDir}/primary/${image.baseName}_tiled.tif" into primaryTiled,
    path "${outputDir}/anchor_nuclei/${image.baseName}_tiled.tif" into anchorNucleiTiled
    path "${outputDir}/anchor_dots/${image.baseName}_tiled.tif" into anchorDapiTiled
    path "${outputDir}/nuclei/${image.baseName}_tiled.tif" into dapiTiled

    script:
    """
    mkdir -p ${outputDir}/primary
    mkdir -p ${outputDir}/anchor_nuclei
    mkdir -p ${outputDir}/anchor_dots
    mkdir -p ${outputDir}/nuclei

    if [[ ${image.name} =~ '_DAPI' ]]; then
        python tiler_spacetx.py ${image} ${tileSize} ${outputDir}/nuclei
        
    elif [[ ${image.name} =~ 'anchor_nuclei' ]]; then
        python tiler_spacetx.py ${image} ${tileSize} ${outputDir}/anchor_nuclei
        
    elif [[ ${image.name} =~ 'anchor_dots' ]]; then
        python tiler_spacetx.py ${image} ${tileSize} ${outputDir}/anchor_dots
        
    else
        python tiler_spacetx.py ${image} ${tileSize} ${outputDir}/primary
    fi
    """
}

workflow {
    TILING_SpaceTx(inputDir: params.imageDir, outputDir: params.outputDir, tileSize: params.tileSize)
}
