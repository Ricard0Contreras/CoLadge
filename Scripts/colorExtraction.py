import fast_colorthief


def getColor(path):
    # path of the image worked on
    image_path = path

    # Sets the quality of the colors extracted
    calidad = 1

    # dominant_color = fast_colorthief.get_dominant_color(image_path, quality=calidad, use_gpu=True)
    colorList = fast_colorthief.get_dominant_color(image_path, quality=calidad, use_gpu=True)

    return colorList
