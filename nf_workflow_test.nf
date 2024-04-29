<<<<<<< HEAD
// Define the main Nextflow script
nextflow.enable.dsl=2

// Define channels to collect HTML files from each process
ch_html_process1 = Channel.fromPath("/hpc/scratch/hdd2/nv066607/iss-nf/RegisterQc/0-reg_qc.html")
ch_html_process2 = Channel.fromPath("/home/nv066607/python_github_enterprise/issdecoder/notebooks/decoding_plots.html")
ch_html_process3 = Channel.fromPath("/hpc/scratch/hdd2/nv066607/iss-nf/RegisterQc/0-reg_qc2.html")

// Concatenate HTML files from all processes
ch_all_html_files = ch_html_process1.merge(ch_html_process2).merge(ch_html_process3)

// Define the process to merge HTML files
process mergeHTML {

    // Input files - HTML files from the channel
    input:
    path(all_html_files)

    // Output file - merged HTML file
    output:
    file 'qc_report.html'

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
=======
#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.flagActive = true


include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from './modules/registration.nf'
include { REGISTER_QC } from './modules/register_qc.nf'
include { TILING } from './modules/tiler.nf'
include { TILE_SIZE_ESTIMATOR } from './modules/tile_size_estimator.nf'
include { SPACETX } from './modules/spacetx.nf'
include { JOIN_JSON } from './modules/join_json.nf'
include { MAKE_EXP_JSON } from './modules/experiment_json.nf'
include { SPOT_FINDER as SPOT_FINDER1 } from './modules/decoding.nf'
include { SPOT_FINDER as SPOT_FINDER2 } from './modules/decoding.nf'
include { TILE_PICKER } from './modules/tile_picker.nf'
include { THRESHOLD_FINDER } from './modules/threshold_finder.nf'
include { POSTCODE_DECODER } from './modules/postcode_decoding.nf'
include { JOIN_COORDINATES } from './modules/join_coords.nf'
include { DECODER_QC } from './modules/decoder_qc.nf'
include { MERGE_HTML } from './modules/merge_html.nf'
include { CONCAT_CSV } from './modules/concat_csv.nf'
include { CONCAT_NPY } from './modules/concat_npy.nf'



workflow {
    println params.empty_barcodes

/*     input_npy = Channel.fromPath('/hpc/scratch/hdd1/nv066607/test-data/*.npy').toSortedList()
    //input_npy.view()
    test = CONCAT_NPY(input_npy)
    name = test.map { it ->
            it.baseName
        }
    if (name.contains("spots_postcode_input")){
        println "YES"
    }else{
        println "NO"
    } */
    if (params.PoSTcode){
        println "yes"
    }else{
        println "no"
    }

>>>>>>> iss-nf-emptyBarcodes
}
