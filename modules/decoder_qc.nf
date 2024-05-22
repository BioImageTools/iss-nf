pythonScript = "${workflow.projectDir}/bin/decoder_qc.py"

process DECODER_QC {
    
    debug true
    label 'long'

    input:
    path(decoded_csv)

    output:
    path("decoding_plots.html")

    script:
    """
    python ${pythonScript} $decoded_csv ${params.PoSTcode} ${params.n_gene_panel} ${params.empty_barcodes} ${params.remove_genes} ${params.invalid_codes} ${params.MICROM_PER_PX} ${params.desired_genes} ${params.housekeepers}
    """
}
