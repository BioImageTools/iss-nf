pythonScript = "${workflow.projectDir}/bin/spacetx.py"

process SPACETX {
    label 'beast'

    //debug true
    label 'beast'
    
    input:
    tuple val(imageType), path('*'), path(coords)
    //file coordinates from params.imageDir

    output:
    tuple val(imageType), path("*${imageType}*")
    tuple val(imageType), path("*${imageType}.json")

    script:
    """
    python ${pythonScript} run_formatting ./ $coords ./
    """
   }