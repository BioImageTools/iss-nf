import bioformats
import numpy as np
import javabridge
from tifffile import imwrite

javabridge.start_vm(class_path=bioformats.JARS)

filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230705_1/Image.vsi'


with bioformats.ImageReader(filename) as reader:
    image = reader.read(series=13)
javabridge.kill_vm()
print(image.shape)
imwrite('/scratch/vakili/alvaro_convert/r3_DAPI.tiff', image[:,:,0])
imwrite('/scratch/vakili/alvaro_convert/r3_Cy3.tiff', image[:,:,1])
imwrite('/scratch/vakili/alvaro_convert/r3_Cy5.tiff', image[:,:,2])