pythonScript = "${workflow.projectDir}/bin/concat_npy.py"

process CONCAT_NPY {
    
    label 'learn_registration'
    
    input:
    path(npy_files)

    output:
    path('spots_postcode_input.npz')
        
    script:
    """
    python ${pythonScript} ${npy_files} 
    """
   }