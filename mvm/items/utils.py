import os
import secrets
from PIL import Image, ImageOps
from flask import current_app


def save_thumbnail(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    print(f_ext)
    if f_ext == ".jpeg":
        f_ext = ".jpg"
        print(f_ext)
    picturefilename = random_hex + f_ext
    picturepath = os.path.join(current_app.root_path, 'static/images/thumbnails', picturefilename)
    outputsize = (250, 166)
    i = Image.open(form_picture)
    i.thumbnail(outputsize)
    j = ImageOps.fit(image=i, size=outputsize, bleed=0.05)
    j.save(picturepath)
    return picturefilename

def save_item(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    if f_ext == ".jpeg":
        f_ext = ".jpg"
        print(f_ext)
    picturefilename = random_hex + f_ext
    picturepath = os.path.join(current_app.root_path, 'static/images/items', picturefilename)
    i = Image.open(form_picture)    
    i.save(picturepath)
    return picturefilename

def get_image_from_file(filename):
    picturepath = os.path.join(current_app.root_path, 'static/images/items', filename)
    with open(picturepath, 'rb') as imgfile:
        return imgfile.read()