#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.flagActive = false


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

    input_npy = Channel.fromPath('/hpc/scratch/hdd1/nv066607/test-data/*.npy').toSortedList()
    input_npy.view()
    CONCAT_NPY(input_npy)

}
