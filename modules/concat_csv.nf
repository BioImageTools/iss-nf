pythonScript = "${workflow.projectDir}/bin/concat_csv.py"

process CONCAT_CSV {
    
    label 'concat'
    
    input:
    path(csv_files)

    output:
    path('starfish_result.csv')
        
    script:
    """
    python ${pythonScript} ${csv_files} 
    """
   }