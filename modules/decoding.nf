pythonScript = "${workflow.projectDir}/bin/decoder_starfish.py"

process SPOT_FINDER {
    
    //debug true
    label 'decoding_starfish'

    input:
    path('*')
    val(fov_id)
    val(threshold)
    val(radius)
    //file coordinates from params.imageDir

    output:
    path("*.npy")
    path ("*.csv")
    val(threshold)

    script:
    """
    python ${pythonScript} decode_fov ./ ${fov_id} ${threshold} ${radius}

    """
   }