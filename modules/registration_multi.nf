pythonScript = "${workflow.projectDir}/bin/registration.py"

process LEARN_TRANSFORM {
    publishDir "Transformations", mode: 'copy', overwrite: true
    debug true
    label 'registration'

    input:
    tuple val(roundID), path(inputMovImagePath)
    path(fixImagePath)
    file(param_files)
    //tuple val(roundID), path(inputMovImagePath)

    output:
    tuple val(roundID), path("*.txt")

    // https://github.com/BioImageTools/ome-zarr-image-analysis-nextflow/issues/7
    //conda '/g/cba/miniconda3/envs/bia'

    script:
    """
    python ${pythonScript} run_learn $fixImagePath ${inputMovImagePath} $param_files
    """
}

process APPLY_TRANSFORM {
    publishDir "Registered", mode: 'copy', overwrite: true
    debug true

    input:
    tuple val(roundID), path(movingImagePath), path(transformPath)

    output:
    tuple val(roundID), path("*.tif")

    script:
    """
    python ${pythonScript} run_apply $movingImagePath $transformPath
    """
}

process NORMALIZE {
    publishDir "Normalized", mode: 'copy', overwrite: true
    debug true

    input:
    tuple val(sampleID), path(imagePath)

    output:
    tuple val(sampleID), path("*.tif")

    script:
    """
    python ${pythonScript} run_norm $imagePath
    """
}