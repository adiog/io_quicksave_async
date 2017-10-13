# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import PIL
import PIL.Image


def crop_image(input_file, output_file, width=640, height=480):
    image = PIL.Image.open(input_file)
    width_factor = (width / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(width_factor)))
    image = image.resize((width, hsize), PIL.Image.ANTIALIAS).crop((0, 0, width, height))
    image.save(output_file)
