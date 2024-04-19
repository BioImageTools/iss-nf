pythonScript = "${workflow.projectDir}/bin/test_postcode_decoder.py"

process POSTCODE_DECODER {
    label 'decoding_postcode'

    input:
    
    path(codebook_json)
    path(starfish_table)
    path(postcode_input)

    //file coordinates from params.imageDir

    output:
    path("*.csv")

    script:
    """
    python ${pythonScript} run $codebook_json $starfish_table $postcode_input
    """
   }
