# Reusable in-situ sequencing analysis workflow orchestrated by Nextflow

Nextflow workflow for the automated creation of a transcript map from ISS image data.

![Nextflow workflow diagram](image.png)

## Analysed data

- [Mouse brain](https://git.embl.de/grp-cba/iss-nf/-/blob/main/data/mouse_brain/README.md?ref_type=heads)
  - Status: Done

## DELETEME

| Producer | Microscope | Stitched | EMBL data access | Public data access |  Execution | Next steps | Issues |

|----------|----------|----------|----------|------|----|----------|----------|----------|

| Dima, GSK              | VS200   | Yes   | GSK cluster |            |  Working  |                                            |  PostCODE | 
| Alvaro, EMBL-Rome      | ?       | Yes   | iss-nf-data/alvaro_000|  |  TODO     | [OME-Zarr Conversion](https://git.embl.de/grp-cba/iss-nf/-/issues/3), OME-Zarr Registration |           | 
| Jorge, Saka, EMBL-HD   | ?       | Yes   | ?             |     |    |  TODO     | [Find the data](https://git.embl.de/grp-cba/iss-nf/-/issues/2)       |           | 
| [PostCode publication](https://www.biorxiv.org/content/10.1101/2021.10.12.464086v1)   | ?       | iss-nf-data/S-BSST700 | https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BSST700 | TODO     | Read access to data, [Stitch it](https://git.embl.de/grp-cba/iss-nf/-/issues/7)                   |           | 



## Run on published dataset (from PoSTcode preprint)
Follow the instructions in the 'process_postcode_data' directory.


## TODO

 - [ ] Scripts for testing data (minimal from StarFISH and mouse-brain tissue: https://zenodo.org/records/7647746)
 - [ ] Docker/Singularity images
 - [ ] Find better way to define input parameters
 - [ ] PostCODE decoding
 - [ ] (Optional) Spot assignment to cells
