from tkinter import *
from tkinter.ttk import *
from watermarker import Watermarker


# UI -------------------------------------------------------------------------------------------------------------------
class WatermarkerUI(Tk):
    def __init__(self):
        # Initialize Tk
        super().__init__()

        # Create watermarker variable to contain watermarker object when initialized
        self.watermarker = None
        # Initialize Tk window (self is window now)
        self.title("Watermarker")
        # Style the widgets - import everything from ttk (tkinter.ttk *), otherwise not working
        # self.style = Style(self)
        # print(self.style.theme_names())
        # print(self.style.theme_use("vista"))

        self.config(padx=40, pady=40)
        # Canvas for the image
        #self.canvas = Canvas(width=300, height=300)
        #self.canvas.grid(column=2, row=0)

        # Main UI
        self.label_text = Label(text="Watermark text:", font=("Segoe UI", 12))
        self.label_text.grid(column=0, row=1)
        self.entry_text = Entry()
        self.entry_text.grid(column=1, row=1, columnspan=2, sticky="EW")
        self.button_batch = Button(text="Batch images", command=self.batch_watermark)
        self.button_batch.grid(column=1, row=2, columnspan=1)
        self.button_load = Button(text="Watermark one image", command=self.add_watermark)
        self.button_load.grid(column=2, row=2, columnspan=1)

        # self.mainloop()

    def initialize_watermaker(self):
        text = self.entry_text.get()
        # Create Watermarker object and pass it text from entry_text
        self.watermarker = Watermarker(text)

    def add_watermark(self):
        self.initialize_watermaker()
        # Open image
        self.watermarker.open_image()

    def batch_watermark(self):
        self.initialize_watermaker()
        # Open directory
        self.watermarker.open_directory()
