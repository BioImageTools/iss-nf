pythonScript = "${workflow.projectDir}/bin/tile_picker.py"

process TILE_PICKER {

    input:
    path('*')

    output:
    tuple val(tile), val(thresholds)
    
    script:
    """
    python ${pythonScript} tile_picker ./
    """
   }