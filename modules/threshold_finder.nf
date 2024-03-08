pythonScript = "${workflow.projectDir}/bin/threshold_finder.py"

process THRESHOLD_FINDER {

    input:
    path(starfish_tables)

    output:
    path('picked_threshold.txt')
    
    script:
    """
    python ${pythonScript} find_threshold $starfish_tables
    """
}
