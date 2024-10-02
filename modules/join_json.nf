pythonScript = "${workflow.projectDir}/bin/join_json.py"

process JOIN_JSON {
    
    label 'concat'
    
    input:
    path(all_spacetx_json)

    output:
    path("experiment.json")

    script:
    """
    python ${pythonScript} merge_json ${all_spacetx_json}
    """
   }