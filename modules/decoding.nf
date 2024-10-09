process SPOT_FINDER {
    
    //debug true
    label 'decoding_starfish'
    container "nimavakili/starfish:latest"

    input:
    path('*')
    val(fov_id)
    val(threshold)
    //file coordinates from params.imageDir

    output:
    path("*.npy")
    path ("*.csv")
    val(threshold)

    script:
    """
    python /scripts/decoder_starfish.py decode_fov ./ ${fov_id} ${threshold} 
    """
   }