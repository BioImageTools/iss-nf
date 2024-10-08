process LEARN_TRANSFORM {
    //publishDir "Transformations", mode: 'copy', overwrite: true
    //debug true
    label 'learn_registration'
    container "nimavakili/registration:latest"

    input:
    tuple val(roundID), path(inputMovImagePath)
    path(fixImagePath)
    val(rescale_factor)
    path(param_files)

    output:
    tuple val(roundID), path("*.txt")

    // https://github.com/BioImageTools/ome-zarr-image-analysis-nextflow/issues/7
    //conda '/g/cba/miniconda3/envs/bia'

    script:
    """
    python /scripts/registration.py  run_learn $fixImagePath $inputMovImagePath $rescale_factor $param_files
    """
}

process APPLY_TRANSFORM {
    //publishDir "Registered", mode: 'copy', overwrite: true
    //debug true
    label 'apply_registration'
    container "nimavakili/registration:latest"

    input:
    tuple val(roundID), path(transformPath), path(movingImagePath)

    output:
    tuple val(roundID), path("*.tif*")

    script:
    """
    python /scripts/registration.py run_apply $movingImagePath $transformPath
    """
}

process NORMALIZE {
    //publishDir "Normalized", mode: 'copy', overwrite: true
    //debug true
    label 'learn_registration'
    container "nimavakili/registration:latest"

    input:
    tuple val(sampleID), path(imagePath)

    output:
    tuple val(sampleID), path("*.tif*")

    script:
    """
    python /scripts/registration.py run_norm $imagePath
    """
}