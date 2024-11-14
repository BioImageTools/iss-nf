process TILE_PICKER {
    label 'small'
    container "nimavakili/tiling:latest"

    input:
    path("*")
    val(n_tilePicker)

    output:
    path('*.txt')
        
    script:
    """
    python /scripts/tile_picker.py tile_picker ./ $n_tilePicker
    """
   }