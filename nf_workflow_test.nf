// Define the main Nextflow script
nextflow.enable.dsl=2

// Define channels to collect HTML files from each process
ch_html_process1 = Channel.fromPath("/home/nv066607/python_github_enterprise/issdecoder/notebooks/decoding_plots.html")
ch_html_process2 = Channel.fromPath("/home/nv066607/python_github_enterprise/issdecoder/notebooks/decoding_plots_2.html")
ch_html_process3 = Channel.fromPath("/home/nv066607/python_github_enterprise/issdecoder/notebooks/decoding_plots_3.html")

// Concatenate HTML files from all processes
ch_all_html_files = reg_html.merge(tile_html).merge(decoder_html)

// Define the process to merge HTML files
process mergeHTML {

    // Input files - HTML files from the channel
    input:
    path(all_html_files)

    // Output file - merged HTML file
    output:
    file 'merged.html'

    // Script to merge HTML files
    script:
    """
    cat ${all_html_files.collect{ it.getName() }.sort().join(' ')} > qc_report.html
    """
}

// Define workflow
workflow {
    // Merge HTML files
    mergeHTML(ch_all_html_files)
}
