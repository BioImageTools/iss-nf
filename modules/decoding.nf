pythonScript = "${workflow.projectDir}/bin/decoder_starfish.py"

process SPOT_FINDER {

    input:
    path('*')
    val(fov_id)
    //file coordinates from params.imageDir

    output:
    tuple val(fov_id), path("*.npy")

    script:
    """
    python ${pythonScript} decode_fov ./ $fov_id
    """
   }