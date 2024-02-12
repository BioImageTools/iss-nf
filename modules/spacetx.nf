#!/usr/bin/env nextflow

params.outputDir_spaceTx = '/path/to/SpaceTx'

process SpaceTx {

    input:
    file image from params.imageDir
    file coordinates from params.imageDir

    output:
    path "${outputDir_spaceTx}/primary/" into primarySpaceTx,
    path "${outputDir_spaceTx}/anchor_nuclei/" into anchorNucleiSpaceTx
    path "${outputDir_spaceTx}/anchor_dots/" into anchorDapiSpaceTx
    path "${outputDir_spaceTx}/nuclei/" into dapiSpaceTx

    script:
    """
    if [ ! -d ${outputDir_spaceTx}/primary ]; then
        mkdir -p ${outputDir_spaceTx}/primary
    fi
    
    if [ ! -d ${outputDir_spaceTx}/anchor_nuclei ]; then
        mkdir -p ${outputDir_spaceTx}/anchor_nuclei
    fi
    
    if [ ! -d ${outputDir_spaceTx}/anchor_dots ]; then
        mkdir -p ${outputDir_spaceTx}/anchor_dots
    fi
    
    if [ ! -d ${outputDir_spaceTx}/nuclei ]; then
        mkdir -p ${outputDir_spaceTx}/nuclei
    fi

    if [[ ${image.name} =~ '_DAPI' ]]; then
        python spacetx.py ${image} ${} ${outputDir_spaceTx}/nuclei
    elif [[ ${image.name} =~ 'anchor_nuclei' ]]; then
        python spacetx.py ${image} ${tileSize} ${outputDir_spaceTx}/anchor_nuclei
    elif [[ ${image.name} =~ 'anchor_dots' ]]; then
        python spacetx.py ${image} ${tileSize} ${outputDir_spaceTx}/anchor_dots
    else
        python spacetx.py ${image} ${tileSize} ${outputDir_spaceTx}/primary
    fi
    """
}


workflow {
    SpaceTx(inputDir: params.imageDir, outputDir: params.outputDir)
}
