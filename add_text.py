from PIL import Image, ImageDraw, ImageFont

def add_image_text():
    image = Image.open("sudal.png")
    texts= ['졸귀 수달이', '졸귀 수달이', '졸귀 수달이', '졸귀 수달이', '졸귀 수달이'] #생성한 text
    num = 5
    image_width, image_height = image.size

    for i in range(num):
        image = Image.open("sudal.png")
        draw = ImageDraw.Draw(image)
        font = [
            ImageFont.truetype('NotoSansKR-Bold.ttf', size=70),
            ImageFont.truetype('NanumPenScript-Regular.ttf', size=70),
            ImageFont.truetype('BagelFatOne-Regular.ttf', size=70),
            ImageFont.truetype('SingleDay-Regular.ttf', size=70),
            ImageFont.truetype('Gugi-Regular.ttf', size=70)
        ]

        bbox = font[i].getbbox(texts[i])
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((image_width - text_width) // 2, image_height - text_height - 50)
        outline_color = (0, 0, 0)
        outline_thickness = 7

        for x_offset in range(-outline_thickness, outline_thickness+1):
            for y_offset in range(-outline_thickness, outline_thickness+1):
                if x_offset == 0 and y_offset == 0:
                    continue
                draw.text(
                    (position[0] + x_offset, position[1] + y_offset),
                    texts[i],
                    font=font[i],
                    fill=outline_color
                )

        text_color = (255, 255, 255)
        draw.text(position, texts[i], font=font[i], fill=text_color)
        image.show()
        print(i)


add_image_text()