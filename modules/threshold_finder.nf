pythonScript = "${workflow.projectDir}/bin/threshold_finder.py"

process THRESHOLD_FINDER {

    input:
    val(tilePicker_thresholds)
    val(sorted_starfish_tables)

    output:
    val(threshold)
    
    script:
    """
    python ${pythonScript} run_threshold ${thresholds} ${tables} 
    """
}
