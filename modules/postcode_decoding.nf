pythonScript = "${workflow.projectDir}/bin/postcode_decoder.py"

process POSTCODE_DECODER {
    label 'beast'

    input:
    path(exp_meta_json)
    path(codebook_json)
    path(postcode_input)

    //file coordinates from params.imageDir

    output:
    path("*.csv")
    //tuple val(fov_id), path("*.npy")
    //tuple val(fov_id), path ("*.csv")

    script:
    """
    python ${pythonScript} run $exp_meta_json $codebook_json $postcode_input
    """
   }
