process POSTCODE_DECODER {
    
    publishDir "ISS-reports", mode: 'copy', overwrite: true
    label 'decoding_postcode'
    container "nimavakili/postcode:latest"

    input:
    path(exp_metadata_json_file)
    path(codebook_json)
    path(starfish_table)
    path(postcode_input)

    //file coordinates from params.imageDir

    output:
    path("*.csv")

    script:
    """
    python /scripts/postcode_decoder.py run $exp_metadata_json_file $codebook_json $starfish_table $postcode_input
    """
   }
