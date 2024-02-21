pythonScript = "${workflow.projectDir}/bin/spacetx.py"

process SPACETX {

    input:
    tuple val(imageType), path('*'), path(coords)
    //file coordinates from params.imageDir

    output:
    tuple val(imageType), path('*.json')

    script:
    """
    python ${pythonScript} run_formating ./ $coords ./
    """
   }


//workflow {
//    SpaceTx(inputDir: params.imageDir, outputDir: params.outputDir_spaceTx)
//}
