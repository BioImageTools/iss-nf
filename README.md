# Reusable in-situ sequencing analysis workflow orchestrated by Nextflow

Nextflow workflow for the automated creation of a transcript map from ISS image data.


| Producer | Microscope | Stitched | Data location | Execution | Next steps | Issues |
|----------|----------|----------|----------|----------|----------|
| Dima, GSK              | VS200   | Yes   | GSK cluster     | Working  |                                            |  PostCODE | 
| Alvaro, EMBL-Rome      | ?       | Yes   | cba/iss-nf-data | TODO     | OME-Zarr Conversion, OME-Zarr Registration |           | 
| Jorge, Saka, EMBL-HD   | ?       | Yes   | ?               | TODO     | Find the data                              |           | 
| PostCODE example       | ?       | No    | ?               | TODO     | Find the data, Stitch it                   |           | 




## TODO

 - [ ] Scripts for testing data (minimal from StarFISH and mouse-brain tissue: https://zenodo.org/records/7647746)
 - [ ] Docker/Singularity images
 - [ ] Find better way to define input parameters
 - [ ] PostCODE decoding
 - [ ] (Optional) Spot assignment to cells
