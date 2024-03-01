pythonScript = "${workflow.projectDir}/bin/postcode_decoder.py"

process POSTCODE_DECODER {
    input:
    path(codebook_json)
    path(starfish_output_files)
    //file coordinates from params.imageDir

    output:
    path("*.csv")
    //tuple val(fov_id), path("*.npy")
    //tuple val(fov_id), path ("*.csv")

    script:
    """
    python ${pythonScript} run $codebook_json $starfish_output_files
    """
   }