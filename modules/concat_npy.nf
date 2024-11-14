pythonScript = "${workflow.projectDir}/bin/concat_npy.py"

process CONCAT_NPY {
    
    label 'concat'
    container "nimavakili/base_env:latest"
    
    input:
    path(npy_files)

    output:
    path('spots_postcode_input.npz')
        
    script:
    """
    python ${pythonScript} ${npy_files} 
    """
   }