# Mouse brain data

## Download raw data

1. Download the dataset by accessing the following link: https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BSST700

You can then transfer it to the HPC using sftp.

### EMBL data location

- Data is at `/g/cba/exchange/iss-nf-data/mouse-brain/raw`

## Stitch

2a. Read the 'preprocess_postcode_data4iss-nf.py' script in this folder. To preprocess the data as stated by a), run:

	$ python preprocess_postcode_data4iss-nf.py run_tile_formating 'path/2/S-BSST700/' 'path/2/outputdir'

NOTE: 'path/2/S-BSST700' should point to that directory, 'S-BSST700'. 

2b. To create the stitched dataset, run the second command from the 'preprocess_postcode_data4iss-nf.py' script:

	$ python preprocess_postcode_data4iss-nf.py run_stitched_formating 'path/2/S-BSST700/slected-tiles' 'path/2/outputdir'

NOTE: Here the first argument points to a different folder than 2a.

### EMBL data location

- Data is at `/g/cba/exchange/iss-nf-data/mouse-brain/stitched`

## Run iss-nf

3. Modify the 'postcode_configuration.config' depending on which system are you running the workflow.

### EMBL data location

#### Registered images

- Data is at `/g/cba/exchange/iss-nf-data/mouse-brain/registered`


