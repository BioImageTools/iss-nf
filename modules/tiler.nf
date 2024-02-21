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
    tuple val(sampleID), path("*.csv")

    script:
    """
    python ${pythonScript} run_tiling $transformedImage 200 ./
    """
}
