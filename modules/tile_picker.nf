pythonScript = "${workflow.projectDir}/bin/tile_picker.py"

process TILE_PICKER {

    input:
    path('*')

    output:
    tuple val('picked_tile.txt'), val('thresholds.txt')
        
    script:
    """
    python ${pythonScript} tile_picker ./
    """
   }