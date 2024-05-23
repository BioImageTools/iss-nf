pythonScript = "${workflow.projectDir}/bin/decoder_qc.py"

process DECODER_QC {
    
    debug true
    label 'long'

    input:
    path(decoded_csv)
    path(exp_metadata_json_file)

    output:
    path("decoding_plots.html")

    script:
    """
    python ${pythonScript} create_qc $decoded_csv $exp_metadata_json_file ${params.PoSTcode}
    """
}
