nextflow.enable.dsl=2
params.path = "${workflow.projectDir}/tile_size.txt"

Channel.fromPath(params.path)
    .splitText()
    .view{"Item: ${it}"}