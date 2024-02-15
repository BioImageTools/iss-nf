// params.imageDir = '/path/to/images'
params.outputDir = '/scratch/segonzal/TiledOutput'
pythonScript = "${workflow.projectDir}/bin/tiler.py"

process TILING {

    input:
    tuple val(roundID), path(transformedImage)
    // file image from params.imageDir
    val tileSize
    // val tileSize

    output:
    path("${params.outputDir}/primary")
    path("coordinates*.csv")
    //path "${outputDir}/anchor_nuclei/${image.baseName}_tiled.tif" into anchorNucleiTiled
    //path "${outputDir}/anchor_dots/${image.baseName}_tiled.tif" into anchorDapiTiled
    //path "${outputDir}/nuclei/${image.baseName}_tiled.tif" into dapiTiled

    script:
    """
    if [ ! -d ${outputDir}/primary ]; then
        mkdir -p ${outputDir}/primary
    fi
    
    if [ ! -d ${outputDir}/anchor_nuclei ]; then
        mkdir -p ${outputDir}/anchor_nuclei
    fi
    
    if [ ! -d ${outputDir}/anchor_dots ]; then
        mkdir -p ${outputDir}/anchor_dots
    fi
    
    if [ ! -d ${outputDir}/nuclei ]; then
        mkdir -p ${outputDir}/nuclei
    fi

    if [[ ${image.name} =~ '_DAPI' ]]; then
        python tiler.py ${image} ${tileSize} ${outputDir}/nuclei
        
    elif [[ ${image.name} =~ 'anchor_nuclei' ]]; then
        python tiler.py ${image} ${tileSize} ${outputDir}/anchor_nuclei
        
    elif [[ ${image.name} =~ 'anchor_dots' ]]; then
        python tiler.py ${image} ${tileSize} ${outputDir}/anchor_dots
        
    else
        python tiler.py ${image} ${tileSize} ${outputDir}/primary
    fi
    """
}

//workflow {
//    TILING(inputDir: params.imageDir, outputDir: params.outputDir, tileSize: params.tileSize)
//}
