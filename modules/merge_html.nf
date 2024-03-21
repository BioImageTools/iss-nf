// Define the process to merge HTML files
process MERGE_HTML {

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