pythonScript = "${workflow.projectDir}/bin/tile_picker2.py"

process TILE_PICKER {

    input:
    path("*")

    output:
    tuple val('picked_tile.txt'), val('thresholds.txt')
        
    script:
    """
    python ${pythonScript} tile_picker ./
    """
   }