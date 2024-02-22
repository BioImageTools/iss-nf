pythonScript = "${workflow.projectDir}/bin/join_json.py"

process JOIN_JSON {

    input:
    tuple path('*')

    output:
    tuple path("experiment.json")

    script:
    """
    python ${pythonScript} merge_json ${path}
    """
   }