pythonScript = "${workflow.projectDir}/bin/register_qc.py"

process REGISTER_QC {
    publishDir "RegisterQc", mode: 'copy', overwrite: true
    //debug true
    label 'apply_registration'
    
    input:
    path(regImg_path)

    output:
    path("0-reg_qc.html")

    script:
    """
    python ${pythonScript} $regImg_path
    """
}
