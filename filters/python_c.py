import pylibfromcpp
import pylibfromcpp_mono_color
from PIL import Image
import io

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

fileName = "../static/imagen_comentarios/ejemplos/tiger.bmp";
print(type(fileName))
pylibfromcpp.filter_image(fileName)

fileName = "../static/imagen_comentarios/ejemplos/astro.bmp";
#pylibfromcpp_mono_color.filter_image(fileName)