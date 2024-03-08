pythonScript = "${workflow.projectDir}/bin/data_collect4threshold.py"

process DATA_COLLECT4THRESHOLD {

    input:
    path(starfish_tables)

    output:
    path('*.csv')
    
    script:
    """
    python ${pythonScript} data_collect $starfish_tables
    """
}
