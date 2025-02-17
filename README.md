# DEPRECATED

Please go to: https://github.com/embl-cba/iss-nf

# Reusable in-situ sequencing analysis workflow orchestrated by Nextflow

Nextflow workflow for the automated creation of a transcript map from ISS image data.

![Nextflow workflow diagram](workflow_diagram.PNG)

# Installation instructions for Your Repository

Follow these steps to set up and install the necessary environment and dependencies for your project.

## Prerequisites

Ensure you have the following installed on your system:
- [Git](https://git-scm.com/) (for cloning the repository)

## Clone the Repository

Clone the project repository from GitHub to your machine.
	
```bash
git clone https://github.com/embl-cba/iss-nf.git
```

## How to run the code

1. **Prepare Your Dataset**

   To run the workflow you need the following data:
   - Image data with naming scheme: `r<Round>_<Channel>.tiff`, where "Round" is a one-based integer and "Channel" is free text without spaces.
    - For example: `r1_DAPI.tiff`
   - Codebook: `codebook.json`, as defined by StarFISH (FIXME: Add link to specification)
   - Experimental metadata `experimental_metadata.json`

   Examples for a codebook and metadata can be [found here](examples/mouse_brain). Corresponding example image data is available [on Zenodo](https://zenodo.org/records/14884160)

2. **Modify the configuration files**

   - **Update the Input Directory:**
     In the `nextflow.config` file, locate the `INPUTDIR` variable and set it to the path of your dataset.
     ```bash
     INPUTDIR = "/path/to/your/dataset"
     ```
   
   - **Prepare the codebook:**
     The workflow uses a `codebook.json` file that should be readable by the STARFISH library. Use our default format as a guide when preparing your own codebook.
     
     **Important note:** For automated threshold finding, the algorithm expects 10-20% of your gene panel to consist of empty barcodes. These empty barcodes should be added at the bottom of your `codebook.json`.

   - **Modify the metadata:**
     You’ll also need to update the `experiment_metadata.json` file. This file contains metadata about your dataset. Modify it to reflect the specifics of your data (e.g., number of rounds, channels, etc.).

3. **Load nextflow**

   To run the workflow, you need to install [Nextflow](https://www.nextflow.io/docs/latest/install.html).
   After installation, your Nextflow environment needs to be activated, e.g., using 
   ```bash
   conda activate nextflow
   ```
   or, on a computer cluster, it may be possible to access nextflow via easy-build using 
   ```bash
   module load Nextflow
   ```

4. **Run the workflow**

	Once you’ve updated your configuration files and loaded Nextflow, you can execute the workflow using the following command in your terminal:
	```bash
	nextflow run nf_workflow.nf -profile apptainer 
  ```

## Troubleshooting

You are welcome to ask us by [writing an issue](https://github.com/embl-cba/iss-nf/issues).