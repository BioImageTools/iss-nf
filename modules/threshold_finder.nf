pythonScript = "${workflow.projectDir}/bin/threshold_finder_new2.py"

process THRESHOLD_FINDER {

    label 'small'
    
    input:
    path(exp_metadata_json)
    path(starfish_tables)

    output:
    path('picked_threshold.txt')
    path("4-thresh_qc.html")
    
    script:
    """
    python ${pythonScript} autocompute_thr $exp_metadata_json $starfish_tables 
    """
}