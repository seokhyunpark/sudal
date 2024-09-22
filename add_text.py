from PIL import ImageDraw, ImageFont

def add_image_text(my_image, text):
    image = my_image
    image_width, image_height = image.size

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font='NotoSansKR-Bold.ttf', size=40)

    bbox = font.getbbox(text)
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
                text,
                font=font,
                fill=outline_color
            )

    text_color = (255, 255, 255)
    draw.text(position, text, font=font, fill=text_color)

    return image
