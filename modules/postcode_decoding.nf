pythonScript = "${workflow.projectDir}/bin/postcode_decoder.py"

process POSTCODE_DECODER {
    
    publishDir "ISS-QC", mode: 'copy', overwrite: true
    label 'decoding_postcode'

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
    python ${pythonScript} run $exp_metadata_json_file $codebook_json $starfish_table $postcode_input
    """
   }
