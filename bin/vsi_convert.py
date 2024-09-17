import bioformats
import numpy as np
import javabridge
from tifffile import imwrite

javabridge.start_vm(class_path=bioformats.JARS)
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230624/Image.vsi'
filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230626/Image.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230704/Image.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230705_1/Image.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230705_2/Image_01.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230706_1/Image.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230706_2/Image_01.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230707_1/Image.vsi'
# filename = '/g/cba/exchange/iss-nf-data/alvaro_000/Folder20230707_2/Image_01.vsi'

with bioformats.ImageReader(filename) as reader:
    image = reader.read(series=13)
javabridge.kill_vm()
print(image.shape)
imwrite('/home/vakili/Documents/python_github/iss-nf/bin/alvaro_convert/r1_DAPI.tiff', image[:,:,0])
imwrite('/home/vakili/Documents/python_github/iss-nf/bin/alvaro_convert/r1_Cy3.tiff', image[:,:,1])
imwrite('/home/vakili/Documents/python_github/iss-nf/bin/alvaro_convert/r1_Cy5.tiff', image[:,:,2])