pythonScript = "${workflow.projectDir}/bin/exp_metadata_json.py"

process MAKE_EXP_JSON {
    debug true
    label 'minimal'

    input:
    path(experiment_metadata_json)

    output:
    path("*.json")

    script:
    """
    python ${pythonScript} make_exp_json $experiment_metadata_json
    """
}
