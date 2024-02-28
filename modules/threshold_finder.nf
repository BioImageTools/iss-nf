pythonScript = "${workflow.projectDir}/bin/threshold_finder.py"
filt_tiledDir = channel.fromPath('Tiled').filter {it.name.startsWith("anchor_dots")}
filt_tiledDir.view()

process THRESHOLD_FINDER {

    input:
    path(filt_tiledDir), path("Experiment.json")

    output:
    val(fov_id), val(threshold)
    
    script:
    """
    python ${pythonScript} run_threshold ${filt_tiledDir} ${Experiment.json} n_tilePicker=40 min_thr=0.008 max_thr=0.01 n_vals=10
    """
}
