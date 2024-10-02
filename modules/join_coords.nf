process JOIN_COORDINATES {
    
    label 'concat'
    
    input:
    tuple val(image_type), path(x)

    output:
    //stdout
    tuple val(image_type), file("*.csv")

    script:
    """
    python ${workflow.projectDir}/bin/join_coordinates.py join $x
    """
}