pythonScript = "${workflow.projectDir}/bin/to_spatialdata.py"

process TO_SPATIALDATA {

    publishDir "ISS-reports", mode: 'copy', overwrite: true
    label 'concat'
    container "nimavakili/spatialdata-env:latest"

    input:
    path(spotsPath_imgPaths)

    output:
    path "spatialdata_processed"

    script:
    """
    python ${pythonScript} to_spatialdata $spotsPath_imgPaths
    """
   }