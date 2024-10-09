### Sample
  * Type
	- [ ] cell culture 2D
	- [ ] cell culture 3D
	- [ ] organoid
	- [ ] tissue 2D
	- [ ] tissue 3D
	- [ ] whole organism/single cell
	- [ ] environmental sample
  * Size scale
    - [ ] 10-100 nm
	- [ ] 100-1000 nm
    - [ ] 1-10 $\mu$m
	- [ ] 10-100 $\mu$m
    - [ ] 100-1000 $\mu$m
	- [ ] >1000 $\mu$m
  * Cellular components

### Assay
  * [Imaging method](http://purl.obolibrary.org/obo/FBbi_00000222)
	- [ ] [time lapse microscopy](http://purl.obolibrary.org/obo/FBbi_00000249)
	- [ ] [bright field microscopy](http://purl.obolibrary.org/obo/FBbi_00000243)
	- [ ] [confocal microscopy](http://purl.obolibrary.org/obo/FBbi_00000251)
	- [ ] [multi-photon microscopy](http://purl.obolibrary.org/obo/FBbi_00000255)
    - [ ] [SPIM](http://purl.obolibrary.org/obo/FBbi_00000369)
	- [ ] [FRAP](http://purl.obolibrary.org/obo/FBbi_00000366)
	- [ ] [scanning electron microscopy](http://purl.obolibrary.org/obo/FBbi_00000257)
	- [ ] [transmission electron microscopy](http://purl.obolibrary.org/obo/FBbi_00000258)
	- [ ] [X-ray microscopy](http://purl.obolibrary.org/obo/FBbi_00000260)
	- [ ] [atomic force microscopy](http://purl.obolibrary.org/obo/FBbi_00000259)
	- [ ] [resolution-enhancing method](http://purl.obolibrary.org/obo/FBbi_00000321) (i.e. super-resolution imaging)

### Data
  * Dimensions
    - [ ] x,y
	- [ ] z
	- [ ] t
	- [ ] c
  * [Format](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_1915)
    - [ ] [TIFF](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3591)
	- [ ] [OME-TIFF](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3590)
	- [ ] [HDF5](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3590)
	- [ ] [Zarr](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3915) (including OME-Zarr)
	- [ ] [AVI](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3990)
	- [ ] [MPEG-4](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3997)
	- [ ] [DSV](https://purl.bioontology.org/ontology/EDAM?conceptid=http%3A%2F%2Fedamontology.org%2Fformat_3751) (Delimiter-Separated Values tabular format)
	- [ ] Proprietary format
  * Size
    - [ ] <1 GB
	- [ ] 1-100 GB
	- [ ] 100-1000 GB
	- [ ] 1-10 TB
	- [ ] >10 TB
  * Storage type
    - [ ] Cluster file system (e.g. /scratch)
    - [ ] NFS volume (e.g. group shares)
	- [ ] S3 bucket
	- [ ] File sharing service (e.g. ownCloud, Google Drive ...)
	- [ ] Git repository
	- [ ] local disk

### Operations
  * Data handling
    - [ ] [Conversion](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_3434)
  * Image processing
    - [ ] [Drift correction](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation__RBh3vNecu5XlIPh3kbMM4Cq)
	- [ ] [Image registration](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_registration)
	- [ ] [Image enhancement](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_enhancement) (e.g. denoising, smoothing ...)
	- [ ] [Image reconstruction](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_reconstruction) (e.g. deconvolution, stitching, tomographic reconstruction ...)
	- [ ] [Image segmentation](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_segmentation)
  * Analysis
    - [ ] [Object feature extraction](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Feature_extraction)
	- [ ] [Object tracking](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_tracking)
	- [ ] [Object counting](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Cell_counting)
	- [ ] [Classification](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_2990) (i.e. image, pixel or object classification)
	- [ ] [Clustering](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation___Clustering)
	- [ ] [Single molecule localisation](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation__R8EfungVXA0oQM2Ac7YY5eu)
	- [ ] [Statistical calculation](http://edamontology.org/operation_2238) (i.e. statistical analysis)
	- [ ] [Visualisation](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_0337) (e.g. surface/volume rendering, montage, overlay, plotting ...)
	- [ ] [Annotation](https://purl.bioontology.org/ontology/EDAM-BIOIMAGING?conceptid=http%3A%2F%2Fedamontology.org%2Foperation_022)
### Software
  * Scripts
	- [ ] Python
	- [ ] Java
	- [ ] R
	- [ ] Fiji/ImageJ macro
	- [ ] Matlab
	- [ ] Netflow workflow
	- [ ] Galaxy workflow
	- [ ] Other:
  * Third-party software and libraries
  	- [ ] Fiji/ImageJ
    - [ ] Cellprofiler
	- [ ] Ilastik
	- [ ] Napari
	- [ ] Cellpose
	- [ ] StarDist
	- [ ] YOLO
	- [ ] Commercial software:
	- [ ] Other: 

### Project owner
  * EMBL unit
    - [ ] Developmental biology
	- [ ] Cell biology and biophysics
	- [ ] Molecular systems biology
	- [ ] Genome biology
	- [ ] Directors' research
	- [ ] Structural biology - Grenoble
	- [ ] Structural biology - Hamburg
	- [ ] Epigenetics and Neurobiology (Rome)
	- [ ] Tissue Biology and Disease Modelling (Barcelona)
	- [ ] Bioinformatics (EBI research)
    - [ ] Support services - Heidelberg 
	- [ ] Support services - Rome
	- [ ] Support services - Barcelona
	- [ ] Support services - Hamburg
	- [ ] Support services - Grenoble
	
	
