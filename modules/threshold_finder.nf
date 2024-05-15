pythonScript = "${workflow.projectDir}/bin/threshold_finder.py"

process THRESHOLD_FINDER {

    input:
    path(exp_metadata_json)
    path(starfish_tables)

    output:
    path('picked_threshold.txt')
    path("4-thresh_qc.html")
    
    script:
    """
<<<<<<< HEAD
    python ${pythonScript} autocompute_thr $exp_metadata_json $starfish_tables 
=======
    python ${pythonScript} autocompute_thr ${params.n_gene_panel} ${params.empty_barcodes} ${params.remove_genes} ${params.invalid_codes} $starfish_tables 
>>>>>>> iss-nf-emptyBarcodes
    """
}
