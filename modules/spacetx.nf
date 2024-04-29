pythonScript = "${workflow.projectDir}/bin/spacetx.py"

process SPACETX {

    //debug true
    label 'beast'
    
    input:
    tuple val(imageType), path('*'), path(coords)
    //file coordinates from params.imageDir

    output:
    tuple val(imageType), path("${imageType}*"), path("${imageType}*.tif*")

    script:
    """
    python ${pythonScript} run_formatting ./ $coords ./
    """
   }