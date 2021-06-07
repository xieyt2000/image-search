import colorgram 
from PIL import Image
img = Image.open('test.jpg')
colors = colorgram.extract(img, 5)
print(colors)
first_color = colors[0]
print(first_color.rgb)

