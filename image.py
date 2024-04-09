from PIL import Image

img = Image.open('./image/panel.png')
Img = img.convert('L')
threshold = 128

table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

# 图片二值化
photo = Img.point(table, '1')
photo.save("2b.png")
