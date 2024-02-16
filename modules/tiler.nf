// params.imageDir = '/path/to/images'
params.outputDir = '/scratch/segonzal/TiledOutput'
pythonScript = "${workflow.projectDir}/bin/tiler.py"

process TILING {
    publishDir "Tiled", mode: 'copy', overwrite: true
    debug true

    input:
    tuple val(sampleID), path(transformedImage)

    output:
    tuple val(sampleID), path("*.tiff")
    path("*.csv")
    //path("*")
    //path "${outputDir}/anchor_nuclei/${image.baseName}_tiled.tif" into anchorNucleiTiled
    //path "${outputDir}/anchor_dots/${image.baseName}_tiled.tif" into anchorDapiTiled
    //path "${outputDir}/nuclei/${image.baseName}_tiled.tif" into dapiTiled

    script:
    """
    python ${pythonScript} run_tiling $transformedImage 200 ./
    """
}

//workflow {
//    TILING(inputDir: params.imageDir, outputDir: params.outputDir, tileSize: params.tileSize)
//}
