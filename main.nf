#!/usr/bin/env nextflow
nextflow.enable.dsl=2


include { LEARN_TRANSFORM; APPLY_TRANSFORM; NORMALIZE } from '../modules/registration.nf'
include { MAKE_EXP_JSON } from '../modules/experiment_json.nf'
include { TILE_SIZE_ESTIMATOR } from '../modules/tile_size_estimator.nf'
include { TILING } from '../modules/tiler.nf'
include { SPACETX } from '../modules/spacetx.nf'
include { TILE_PICKER } from '../modules/tile_picker.nf'
include { SPOT_FINDER as SPOT_FINDER1 } from '../modules/decoding.nf'
include { THRESHOLD_FINDER } from '../modules/threshold_finder.nf'
include { SPOT_FINDER as SPOT_FINDER2 } from '../modules/decoding.nf'
include { POSTCODE_DECODER } from '../modules/postcode_decoding.nf'
include { JOIN_COORDINATES } from '../modules/join_coords.nf'