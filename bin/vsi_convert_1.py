import bioformats
import numpy as np
import javabridge
from tifffile import imwrite

javabridge.start_vm(class_path=bioformats.JARS)
filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230626/Image.vsi'


with bioformats.ImageReader(filename) as reader:
    image = reader.read(series=13)
javabridge.kill_vm()
print(image.shape)
imwrite('/home/vakili/Documents/python_github/iss-nf/bin/alvaro_convert/r1_DAPI.tiff', image[:,:,0])
imwrite('/home/vakili/Documents/python_github/iss-nf/bin/alvaro_convert/r1_Cy3.tiff', image[:,:,1])
imwrite('/home/vakili/Documents/python_github/iss-nf/bin/alvaro_convert/r1_Cy5.tiff', image[:,:,2])