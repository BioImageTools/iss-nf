#!/usr/bin/env nextflow
pythonTestScript = "${workflow.projectDir}/bin/test_tiler.py"
pythonNArgsTestScript = "${workflow.projectDir}/nargs_test.py"
pythonTestFolderContentsPrint = "${workflow.projectDir}/test_python_print_files_current_directory.py"
params.coordinates_csv = "${workflow.projectDir}/test_coordinates.csv"

params.outDir = "/scratch/segonzal/TilerOutput"
params.img_name = "test"
params.indir = "${workflow.projectDir}/TestIndir/*.tif"

process CREATE_IMAGE {
    publishDir "FoVs", mode: 'copy', overwrite: true
    debug true
    input:
        path(img_name)

    output:
        path("*.csv")
        //path("${img_name}/")
        path("*.tif")

    script:
    """
    python ${pythonTestScript} run_tiling $img_name 
    """
}

process CREATE_TXT {
    input:
    tuple val(xid), val(x)

    output:
    path '*.txt'

    """
    echo ${x} >> ${xid}.txt
    """
}

process JOIN_PATHS_TXT {
    publishDir "Final_Tiling_Results", mode: 'copy', overwrite: true
    debug true

    input:
    val x

    output:
    file("combined_paths.txt")

    script:
    """
    touch combined_paths.txt
    cat $x >> combined_paths.txt
    """
}

process FORMAT2SPACETX {
    publishDir "FormattedData", mode: 'copy', overwrite: true
    debug true

    input:
    path '*'
    path coords

    output:
    path("*")

    script:
    """
    python $pythonTestFolderContentsPrint format ./ $coords
    """
}

process READ_EXPERIMENT {
    input:
    path '*'

    output:
    path("*.txt")

    script:
    """
    python $pythonTestFolderContentsPrint print_experiment './'
    """
}

workflow {
    inputTest_ch = Channel.fromPath(params.indir)
    //tile_ch = CREATE_IMAGE(params.img_name)
    tile_ch = CREATE_IMAGE(inputTest_ch)
    //tile_ch[0].view()
    //tile_ch[1].view()
    //CREATE_FULL_CHANNEL_TXT(tile_ch[1])
    //images_txt_ch = tile_ch[1]
    //                    .collectFile(name: 'test_fov.txt', newLine: true)

    //tile_ch[0].view()
    full_paths = tile_ch[1]//.view()//[0].getParent()
    //full_paths.view()

    collectedPaths_ch = full_paths.collect()
    //collectedPaths_ch.view()
    
    // Now give the collected files to a python script that accepts a variable number of arguments:
    coords_ch = Channel.fromPath(params.coordinates_csv)
    spacetx_ch = FORMAT2SPACETX(collectedPaths_ch, coords_ch)
    //spacetx_ch.view()
    READ_EXPERIMENT(spacetx_ch)
}