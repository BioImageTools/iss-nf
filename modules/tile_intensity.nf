pythonScript = "${workflow.projectDir}/bin/tile_intensity.py"

process TILE_INTENSITY {

    input:
    path(all_anchorDots)

    output:
    path('*.txt')
        
    script:
    """
    python ${pythonScript} intensity_measurement $all_anchorDots
    """
   }