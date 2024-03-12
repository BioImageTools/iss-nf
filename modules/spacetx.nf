pythonScript = "${workflow.projectDir}/bin/spacetx.py"

process SPACETX {
    
    // label "process_high"
    
    input:
    tuple val(imageType), path('*'), path(coords)
    //file coordinates from params.imageDir

    output:
    tuple val(imageType), path("${imageType}*"), path("${imageType}*.tiff")

    script:
    """
    python ${pythonScript} run_formatting ./ $coords ./
    """
   }