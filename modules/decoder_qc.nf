//pythonScript = "${workflow.projectDir}/bin/decoder_qc.py"
pythonScript = "${workflow.projectDir}/bin/decoder_qc_interactive.py"


process DECODER_QC {
    //debug true
    label 'long'

    input:
    path(decoded_csv)

    output:
    path("decoding_plots.html")

    script:
    """
    python ${pythonScript} $decoded_csv ${params.PoSTcode}
    """
}
