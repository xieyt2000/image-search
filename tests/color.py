import colorgram 

colors = colorgram.extract('test.jpg', 3)
print(colors)
first_color = colors[0]
print(first_color.rgb)
print(tuple(first_color.hsl))
print(first_color.proportion)