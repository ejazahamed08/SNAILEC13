import cv2
from PIL import Image
image = Image.open("2392608446.jpg")
print(image.format, image.size, image.mode)
image.show()