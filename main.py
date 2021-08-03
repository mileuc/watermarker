from PIL import ImageTk, ImageDraw, ImageFont
import PIL.Image  # to avoid confusion with the built-in Image class
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
import ctypes
import math

SOURCE_DIRECTORY = "/images"
colour_code = ((196, 229, 142), "#c4e58e")  # default colour for the text watermark font

# ------------------------------------ FUNCTIONS ---------------------------------------------------


def open_base_image():
    # open dialog and allow user to select file to be watermarked
    base_image_path_btn_text.set("Loading...")
    base_image_path_btn.config(state="disabled", bg="light grey")
    photo_name = askopenfilename(initialdir=SOURCE_DIRECTORY, title="Select a file as the base image",
                                 filetype=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
    if photo_name:
        base_image_path_input.delete(0, END)
        base_image_path_input.insert(0, photo_name)
        base_image_path_btn_text.set("Select Base Image")
        base_image_path_btn.config(state="normal", bg="#c4e58e")
        add_wm_image_path_btn.config(state="normal", bg="#c4e58e")
        add_wm_text_btn.config(state="normal", bg="#c4e58e")
    else:
        base_image_path_btn_text.set("Select Base Image")
        base_image_path_btn.config(state="normal", bg="#c4e58e")


def open_watermark_image():
    # open dialog and allow user to select watermark
    add_wm_image_path_btn_text.set("Loading...")
    add_wm_image_path_btn.config(state="disabled", bg="light grey")
    photo_name = askopenfilename(initialdir=SOURCE_DIRECTORY, title="Select a file as the watermark image",
                                 filetype=(("png files", "*.png"), ("jpeg files", "*.jpeg"), ("all files", "*.*")))
    if photo_name:
        wm_image_path_input.delete(0, END)
        wm_image_path_input.insert(0, photo_name)
        add_wm_image_path_btn_text.set("Select Watermark Image")
        add_wm_image_path_btn.config(state="normal", bg="#c4e58e")
        add_wm_image_btn.config(state="normal", bg="#c4e58e")
    else:
        add_wm_image_path_btn_text.set("Select Watermark Image")
        add_wm_image_path_btn.config(state="normal", bg="#c4e58e")


def add_image_watermark():
    add_wm_image_btn_text.set("Loading...")
    add_wm_image_btn.config(state="disabled", bg="light grey")
    base_image_path = base_image_path_input.get()
    watermark_image_path = wm_image_path_input.get()

    try:
        image = PIL.Image.open(base_image_path).convert("RGBA")
        wm_image = PIL.Image.open(watermark_image_path).convert("RGBA")

        # Size watermark relative to size of base image
        wm_resized = wm_image.resize((round(image.size[0] * .10), round(image.size[1] * .10)))
        wm_mask = wm_resized.convert("RGBA")

        # Set position to lower right corner
        position = (image.size[0] - wm_resized.size[0], image.size[1] - wm_resized.size[1])

        # new image that contains the original image and the watermark image combined
        combined_image = PIL.Image.new('RGBA', image.size, (0, 0, 0, 0))
        combined_image.paste(image, (0, 0))
        combined_image.paste(wm_mask, position, mask=wm_mask)
        combined_image.show()

        # Save watermarked photo
        finished_img = combined_image.convert("RGB")
        finished_img_name = base_image_path[:-4] + " _image_WM.jpg"
        finished_img.save(finished_img_name)

        success_text.set(f"Success! File saved to:\n{finished_img_name}.")

    except AttributeError:  # when trying to read an empty file path
        success_text.set("Sorry, something is wrong with your base or watermark image.\nPlease try again!")
    finally:
        add_wm_image_btn_text.set("Add Image Watermark")
        add_wm_image_btn.config(state="normal", bg="#c4e58e")
        wm_image_path_input.delete(0, END)


def add_text_watermark():
    global colour_code

    add_wm_text_btn_text.set("Loading...")
    add_wm_text_btn.config(state="disabled", bg="light grey")
    # cannot add images while watermark image is chosen
    base_image_path = base_image_path_input.get()
    try:
        scale = float(font_scale_input.get())
    except ValueError:
        scale = 1

    try:
        image = PIL.Image.open(base_image_path).convert("RGBA")
        wm_text = wm_text_input.get()
        # print(wm_text)

        draw = ImageDraw.Draw(image)
        font_size = round(math.sqrt(image.size[0] + image.size[1]) * scale)
        font = ImageFont.truetype("arial.ttf", font_size)

        text_size_x, text_size_y = draw.textsize(wm_text, font)

        # set text position
        text_position = (image.size[0] - text_size_x, image.size[1] - text_size_y)
        # print(text_position)

        # draw text on image
        draw.text(text_position, wm_text, (int(colour_code[0][0]), int(colour_code[0][1]), int(colour_code[0][2]), 1),
                  font=font)

        # save watermarked photo
        image = image.convert("RGB")
        image.show()
        finished_img_name = base_image_path[:-4] + f"_text_WM_{wm_text}.jpg"  # insert before .jpg
        image.save(finished_img_name)

        success_text.set(f"Success! File saved to:\n{finished_img_name}.")
    except AttributeError:
        success_text.set("Sorry, something is wrong with your base image or text.\nPlease try again!")
    finally:
        add_wm_text_btn_text.set("Add Text Watermark")
        add_wm_text_btn.config(state="normal", bg="#c4e58e")
        wm_text_input.delete(0, END)


def choose_colour():
    global colour_code
    # colour_code contains a 2-element tuple with the RGB tuple and the hexadecimal string
    colour_code = askcolor(title="Choose colour")
    colour_btn.config(bg=colour_code[1])


def close_window():
    window.destroy()


# ------------------------------------ GUI -------------------------------------------------------
# GUI should allow you to select photo / path to add images,
#  Outgoing photo name / path
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # improves tkinter window resolution
window = Tk()
window.title("Watermarker")
window.config(padx=50, pady=50, bg="#FDEFEF")

# logo
logo = PIL.Image.open("images/chikorita.png")
logo = logo.resize((round(logo.size[0] * .20), round(logo.size[1] * .20)))
logo = ImageTk.PhotoImage(logo)

canvas = Canvas(window, width=114, height=150, bg="#FDEFEF", highlightthickness=0)  # height/width match 20% of original
canvas.create_image(57, 75, image=logo)
canvas.grid(column=2, row=0, columnspan=3, pady=(0, 30))

# status message bar
instruction_label = Label(window, text="Add a text or image watermark to an image!", font="Ariel", bg="#F4DFD0",
                          fg="GREY")
instruction_label.grid(column=2, row=1, columnspan=3, pady=(0, 15))


# base image path input and image selection button
base_image_path_label = Label(text="Location of Image to be Watermarked", font="Ariel", bg="#c4e58e", fg="grey")
base_image_path_label.grid(column=2, row=2, padx=(0, 15), sticky="E")
base_image_path_input = Entry(width=32)
base_image_path_input.grid(column=3, row=2, sticky="W")
base_image_path_btn_text = StringVar()
base_image_path_btn_text.set("Select Base Image")
base_image_path_btn = Button(window, textvariable=base_image_path_btn_text, command=open_base_image, font="Ariel",
                             bg="#c4e58e", fg="grey", relief=GROOVE)
base_image_path_btn.grid(column=4, row=2, sticky="W", padx=(15, 0), pady=(2, 2))

# watermark image path input and image selection button - row 3
wm_image_path_label = Label(text="Location of Watermark Image", font="Ariel", bg="#c4e58e", fg="grey")
wm_image_path_label.grid(column=2, row=3, padx=(0, 15), sticky="E")
wm_image_path_input = Entry(width=32)
wm_image_path_input.grid(column=3, row=3, sticky="W")
add_wm_image_path_btn_text = StringVar()
add_wm_image_path_btn_text.set("Select Watermark Image")
add_wm_image_path_btn = Button(window, textvariable=add_wm_image_path_btn_text, command=open_watermark_image,
                               font="Ariel", bg="#c4e58e", fg="grey", relief=GROOVE)
add_wm_image_path_btn.grid(column=4, row=3, sticky="W", padx=(15, 0), pady=(2, 2))
add_wm_image_path_btn.config(state="disabled", bg="light grey")


# add watermark image button
add_wm_image_btn_text = StringVar()
add_wm_image_btn_text.set("Add Image Watermark")
add_wm_image_btn = Button(window, textvariable=add_wm_image_btn_text, command=add_image_watermark, font="Ariel",
                          bg="#c4e58e", fg="grey", relief=GROOVE)
add_wm_image_btn.grid(column=4, row=4, sticky="W", padx=(15, 0), pady=(2, 2))
add_wm_image_btn.config(state="disabled", bg="light grey")


# watermark text input, label, button - row 5
wm_text_label = Label(text="Watermark Text", font="Ariel", bg="#c4e58e", fg="grey")
wm_text_label.grid(column=2, row=5, padx=(0, 15), sticky="E")
wm_text_input = Entry(width=16)
wm_text_input.grid(column=3, row=5, sticky="W")
add_wm_text_btn_text = StringVar()
add_wm_text_btn_text.set("Add Text Watermark")
add_wm_text_btn = Button(window, textvariable=add_wm_text_btn_text, command=add_text_watermark, font="Ariel",
                         bg="#c4e58e", fg="grey", relief=GROOVE)
add_wm_text_btn.grid(column=4, row=5, sticky="W", padx=(15, 0), pady=(2, 2))
add_wm_text_btn.config(state="disabled", bg="light grey")

# font scale input, label, button - row 6
font_scale_label = Label(text="Scale Font Size by", font="Ariel", bg="#c4e58e", fg="grey")
font_scale_label.grid(column=2, row=6, padx=(0, 15), sticky="E")
font_scale_input = Entry(width=7)
font_scale_input.insert(0, "1")
font_scale_input.grid(column=3, row=6, sticky="W")

# font colour and size options - row 6
colour_btn = Button(window, text="Choose Font Colour", command=choose_colour, font="Ariel", bg="#c4e58e", fg="grey",
                    relief=GROOVE)
colour_btn.grid(column=3, row=7, sticky="W", pady=(6, 0))


# exit button - row 8
exit_btn = Button(window, text="Exit", command=close_window, font="Ariel", bg="#c4e58e", fg="grey", relief=GROOVE,
                  height=2, width=15)
exit_btn.grid(column=4, row=8, sticky="W", padx=(15, 0), pady=(2, 2))

# success message - row 9
success_text = StringVar()
success_text.set(" ")
success_label = Label(window, textvariable=success_text)
success_label.grid(columnspan=3, column=2, row=9, pady=(15, 0))


window.mainloop()