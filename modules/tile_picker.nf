pythonScript = "${workflow.projectDir}/bin/tile_picker2.py"

process TILE_PICKER {

    input:
    path("*")
    val(n_tilePicker)

    output:
    path('*.txt')
        
    script:
    """
    python ${pythonScript} tile_picker ./ $n_tilePicker
    """
   }