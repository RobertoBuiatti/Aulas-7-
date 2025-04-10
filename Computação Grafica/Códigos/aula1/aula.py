from PIL import Image

mode = 'RGB'
size = [100, 50]
color = 0
img = Image.new(mode, size, color)
# img.show()
# img.save('aula.png')

img2 = Image.open('aula.png')
matriz = img2.load()
for i in range(10, 30):
    for j in range(10, 40):
        matriz[i, j] = (255, 0, 0)
img2.show()

for i in range(10, 30):
    for j in range(10, 40):
        print(matriz[i, j], end=' ')
    print()