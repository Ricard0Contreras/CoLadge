import fast_colorthief


def getColor(path):
    # path of the image of
    image_path = path

    # Sets the quality of the colors extracted
    calidad = 5

    # dominant_color = fast_colorthief.get_dominant_color(image_path, quality=calidad, use_gpu=True)
    colorList = fast_colorthief.get_dominant_color(image_path, quality=calidad, use_gpu=True)

    # Considering only storing the main color of a picture

    listColor = [*colorList]

    for n in range(len(listColor)):
        listColor[n] = str(listColor[n]).replace("(", "")
        listColor[n] = str(listColor[n]).replace(")", "")

    return listColor
