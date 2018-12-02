import pytesseract
from PIL import Image

# 打开图片
image = Image.open("test.png")

text = pytesseract.image_to_string(image)
print(text)
