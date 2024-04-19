pythonScript = "${workflow.projectDir}/bin/concat_csv.py"

process CONCAT_CSV {
    
    label 'learn_registration'
    
    input:
    path(csv_files)

    output:
    path('starfish_result.csv')
        
    script:
    """
    python ${pythonScript} ${csv_files} 
    """
   }