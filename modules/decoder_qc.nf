pythonScript = "${workflow.projectDir}/bin/decoder_qc.py"

process DECODER_QC {
    //debug true
    label 'long'

    input:
    path(postcode_csv)

    output:
    path("3-decoding_plots.html")

    script:
    """
    python ${pythonScript} $postcode_csv
    """
}
