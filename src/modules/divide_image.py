from PIL import Image
import os



def create_sub_image(x, y, file_name, img_dir, width_size, height_size):
    sub_image = (x, y, x + width_size, y + height_size)
    save_sub_image(file_name, x, y, sub_image, img_dir)


def save_sub_image(file_name, x, y, sub_image, img_dir):
    name, extension = os.path.splitext(file_name)
    img = Image.open(os.path.join(img_dir, file_name))
    sub_image_path = os.path.join(f"{name}", f"{name}_{x}_{y}{extension}")
    try:
        img.crop(sub_image).save(sub_image_path)
    except Exception as e:
        print(e)
        
