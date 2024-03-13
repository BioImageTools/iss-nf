pythonScript = "${workflow.projectDir}/bin/register_qc.py"

process REGISTER_QC {
    publishDir "RegisterQc", mode: 'copy', overwrite: true
    //debug true

    input:
    path(nuclei_path)
    path(dapis_path)

    output:
    path("reg_qc.html")

    script:
    """
    python ${pythonScript} $nuclei_path $dapis_path
    """
}
