# Reusable in-situ sequencing analysis workflow orchestrated by Nextflow

Nextflow workflow for the automated creation of a transcript map from ISS image data.

![Nextflow workflow diagram](image.png)

## Analysed data

- [Mouse brain](https://git.embl.de/grp-cba/iss-nf/-/blob/main/data/mouse_brain/README.md?ref_type=heads)
  - Status: Done

## DELETEME

| Producer              | Microscope | Stitched | EMBL data access             | Public data access | Execution | Next steps                                                                                              | Issues  |
|-----------------------|------------|----------|------------------------------|--------------------|-----------|----------------------------------------------------------------------------------------------------------|---------|
| Dima, GSK             | VS200      | Yes      | GSK cluster                   |                    | Working   | PostCODE                                                                                                 |         |
| Alvaro, EMBL-Rome     | ?          | Yes      | iss-nf-data/alvaro_000        |                    | TODO      | [OME-Zarr Conversion](https://git.embl.de/grp-cba/iss-nf/-/issues/3), OME-Zarr Registration              |         |
| Jorge, Saka, EMBL-HD  | ?          | Yes      | ?                             |                    | TODO      | [Find the data](https://git.embl.de/grp-cba/iss-nf/-/issues/2)                                           |         |
| [PostCode publication](https://www.biorxiv.org/content/10.1101/2021.10.12.464086v1) | ?          | iss-nf-data/S-BSST700 | https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BSST700 | TODO      | Read access to data, [Stitch it](https://git.embl.de/grp-cba/iss-nf/-/issues/7)                         |         |


## Run on published dataset (from PoSTcode preprint)
Follow the instructions in the 'process_postcode_data' directory.

# Installation Instructions for Your Repository

Follow these steps to set up and install the necessary environment and dependencies for your project.

## Prerequisites

Ensure you have the following installed on your system:
- [Anaconda](https://www.anaconda.com/products/distribution) (for managing the environment)
- [Git](https://git-scm.com/) (for cloning the repository)

## Installation Steps

1. **Create a Conda Environment**

   First, create a new Conda environment using the provided `iss-nf.yml` file. This file contains all the dependencies required for your project.

   ```bash
   conda env create -f iss-nf.yml

2. **Clone the Repository**

	Next, clone the project repository from GitHub to your local machine.
	
	```bash
	git clone https://github.com/milana-gataric/postcode.git

3. **Activate the Conda Environment**

	Activate the Conda environment you created in step 1.
	```bash
	conda activate iss-nf

4. **Navigate to the Project Directory**
	Change your current directory to the cloned repository.
	```bash
	cd postcode

5. **Install the Project in Editable Mode**
	Finally, install the project in editable mode. This allows you to make changes to the source code and have those changes immediately available without reinstalling the package.
	```bash
	python3 -m pip install -e .


## TODO

 - [ ] Scripts for testing data (minimal from StarFISH and mouse-brain tissue: https://zenodo.org/records/7647746)
 - [ ] Docker/Singularity images
 - [ ] Find better way to define input parameters
 - [ ] PostCODE decoding
 - [ ] (Optional) Spot assignment to cells

