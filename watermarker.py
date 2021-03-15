from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import os.path
from pathlib import Path


class Watermarker:
    def __init__(self, text):
        self.text = text
        self.print_text()

    def print_text(self):
        print(self.text)

    def open_image(self):
        """Opens a dialog window and loads the selected image, then calls add_watermark method."""
        # Getting filepath with open file dialog
        # without initialdir="/" opens the last opened directory
        file_path = filedialog.askopenfilename(title="Open Image",
                                               filetypes=(("image files", "*.jpg .png .gif*"), ("all files", "*.*")))
        # Open the selected image
        if file_path != "":
            image = Image.open(rf"{file_path}")
            self.add_watermark(image, file_path)
            # Inform user the process finished
            confirmation_window = messagebox.showinfo(title="Finished", message="Image was watermarked.")

    def open_directory(self):
        """Opens a dialog window to select an image directory, then calls batch_images method."""
        file_directory = filedialog.askdirectory(title="Select Image Folder")
        self.batch_images(file_directory)

    def add_watermark(self, image, path):
        """Adds watermark to the passed image object.
        image : PIL.Image
        path : str"""
        # Set watermark text padding
        padding_x = 20
        padding_y = 20
        # Amount of pixels from the bottom of the image, must be smaller than image height
        push = 20
        # Alpha transparency value
        aplha = 70
        # Setting the watermark text
        if self.text is not None and len(self.text) > 0:
            watermark_text = self.text
        else:
            watermark_text = "© Your Name"
        # --------------------------------
        # Make image drawable
        draw_image = ImageDraw.Draw(image)
        # Font
        # Trying to make the font size dynamic, depending on image size
        font_size = int(image.size[1] / 1000 * 60)
        font = ImageFont.truetype("font/Inter-Regular.ttf", size=font_size)
        # Getting the text size tuple
        text_size = draw_image.textsize(watermark_text, font)

        # Image width - text width, image height - text height - push (distance from the bottom of the image)
        watermark_pos = (image.size[0] - (text_size[0] + padding_x), image.size[1] - (text_size[1] + padding_y) - push)

        # Create watermark image filled with colour
        image_text = Image.new("RGB", size=(text_size[0] + padding_x, text_size[1] + padding_y), color="#000000")
        watermark = ImageDraw.Draw(image_text)
        # Add text to the watermark image
        watermark.text((padding_x / 2, padding_y / 2), watermark_text, fill="#ffffff", font=font)
        image_text.putalpha(aplha)
        # Place watermark in the original image
        image.paste(image_text, watermark_pos, image_text)
        # Save the image with watermark as a new file
        self.save_image(image, path)

    def save_image(self, image, path):
        """Saves the image in the path.
        image : PIL.Image
        path : str"""
        # Save the image as a new file with watermarked at the end of the file name
        new_path = os.path.splitext(path)[0] + "_watermarked" + os.path.splitext(path)[1]
        image.save(new_path)

    def batch_images(self, path):
        """Processes all images in the selected folder and watermarks them with add_watermark method.
        path : str"""
        all_images = []
        image_paths = []
        folder_name = "watermarked/"
        folder_path = path + "/"
        # Create a new directory inside the current image directory
        Path(folder_path + folder_name).mkdir(parents=True, exist_ok=True)
        # Allowed image extensions
        allowed_extensions = [".jpg", ".gif", ".png", ".tif", ".tiff", ".tga"]

        # Iterate over all the files in the current directory
        for file in os.listdir(folder_path):
            # Splits the filename and assigns it's extension to extension variable
            extension = os.path.splitext(file)[1]
            # Loads and appends all images in the folder to all_images
            # Appends image names to image_paths
            if extension.lower() in allowed_extensions:
                image_paths.append(folder_path + folder_name + file)
                all_images.append(Image.open(fr"{folder_path}{file}"))

        # Watermark all images
        for i in range(len(image_paths)):
            self.add_watermark(all_images[i], image_paths[i])
        # Inform user the process finished
        confirmation_window = messagebox.showinfo(title="Finished", message="All images were watermarked.")
