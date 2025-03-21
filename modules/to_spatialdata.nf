pythonScript = "${workflow.projectDir}/bin/to_spatialdata.py"

process TO_SPATIALDATA {

    publishDir "ISS-reports", mode: 'copy', overwrite: true
    label 'concat'
    container "nimavakili/spatialdata-env:0.2.5"

    input:
    path(exp_metadata_json)
    path(spotsPath_imgPaths)

    output:
    path "spatialdata_processed"

    script:
    """
    python ${pythonScript} to_spatialdata $exp_metadata_json $spotsPath_imgPaths
    """
   }