pythonScript = "${workflow.projectDir}/bin/decoder_starfish.py"

process SPOT_FINDER {

    input:
    path('*')
    val(fov_id)
    val(all_thresholds)
    //file coordinates from params.imageDir

    output:
    path("*.npy")
    path ("*.csv")

    script:
    """
    python ${pythonScript} decode_fov ./ $fov_id $threshold
    """
   }