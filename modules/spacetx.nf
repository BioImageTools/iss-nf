process SPACETX {

    //debug true
    label 'beast'
    container "nimavakili/starfish:latest"

    input:
    tuple val(imageType), path('*'), path(coords)
    //file coordinates from params.imageDir

    output:
    tuple val(imageType), path("${imageType}*"), path("${imageType}*.tif*")

    script:
    """
    python /scripts/spacetx.py run_formatting ./ $coords ./
    """
   }