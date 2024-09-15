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


## How to Run the Code

This section will guide you on how to run the workflow using the mouse brain dataset as an example. You can refer to the [mouse brain dataset](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BSST700) for more context.

### Steps to Run the Workflow:

1. **Prepare Your Dataset**

   Before running the workflow, ensure that your data is prepared and follows our [naming scheme for images](/g/cba/exchange/iss-nf-data/mouse-brain/stitched). This ensures the workflow can locate and process your files correctly.

2. **Modify the Configuration Files**

   - **Update the Input Directory:**
     In the `EMBL.config` file, locate the `INPUTDIR` variable and set it to the path of your dataset.
     ```bash
     INPUTDIR = "/path/to/your/dataset"
     ```
   
   - **Prepare the Codebook:**
     The workflow uses a `codebook.json` file that should be readable by the STARFISH library. Use our default format as a guide when preparing your own codebook.
     
     **Important Note:** For automated threshold finding, the algorithm expects 10-20% of your gene panel to consist of empty barcodes. These empty barcodes should be added at the bottom of your `codebook.json`.

   - **Modify the Metadata:**
     You’ll also need to update the `experiment_metadata.json` file. This file contains metadata about your dataset. Modify it to reflect the specifics of your data (e.g., number of rounds, channels, etc.).

3. **Load Nextflow**

   To run the workflow, you need the Nextflow module. If you are using the EMBL cluster, you can easily load it by running the following command:
   ```bash
   module load Nextflow

4. **Run the Workflow**

	Once you’ve updated your configuration files and loaded Nextflow, you can execute the workflow using the following command in your terminal:
	```bash
	nextflow run nf_workflow.nf -c EMBL.config

