pythonScript = "${workflow.projectDir}/bin/concat_csv.py"

process CONCAT_CSV {
    
    label 'concat'
    container "nimavakili/base_env:latest"
    
    input:
    path(csv_files)

    output:
    path('starfish_result.csv')
        
    script:
    """
    python ${pythonScript} ${csv_files} 
    """
   }