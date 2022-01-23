from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageFont, ImageDraw, ImageTk


DEFAULT_FONT_SIZE = 50
DEFAULT_LOGO_SIZE = (150, 150)
DEFAULT_LOGO_POSITION = (300, 300)
DEFAULT_FONT_STYLE = "arial.ttf"

image = None
logo = None
copied_image = None
copied_logo = None


# Function
def select_image():
    global image, copied_image
    file_name = askopenfilename(title="Select an image")
    image = Image.open(file_name)
    copied_image = image.copy()
    image = image.resize((250, 250), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    panel = Label(window, image=image)
    panel.image = image
    panel.grid(row=1, column=1, columnspan=2)


def select_logo():
    global logo, copied_logo
    file_name = askopenfilename(title="Select a logo")
    logo = Image.open(file_name)
    copied_logo = logo.copy()
    logo = logo.resize((250, 250), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(logo)
    panel = Label(window, image=logo)
    panel.image = logo
    panel.grid(row=1, column=4, columnspan=2)


def apply_watermark():
    global copied_logo, copied_image
    if copied_logo:
        # image watermark in input position
        size = list(map(int, logo_size.get().strip().split("x")))
        watermark_logo_size = (size[0], size[1])
        copied_logo.thumbnail(watermark_logo_size)
        position = list(map(int, logo_position.get().strip().split(",")))
        copied_image.paste(copied_logo, position)

    # text watermark in bottom right corner
    draw = ImageDraw.Draw(copied_image)
    text = text_entry.get()
    width, height = copied_image.size
    font = ImageFont.truetype(DEFAULT_FONT_STYLE, int(font_size.get().strip()))

    # calculate the x,y coordinates of the text
    margin = 10
    text_width, text_height = draw.textsize(text, font)
    x = width - text_width - margin
    y = height - text_height - margin

    # draw watermark in the bottom right corner
    draw.text((x, y), text, font=font, fill="black")
    copied_image.show()

    save_image(copied_image)


def save_image(copied_image):
    copied_image.save("images/watermarked-image.jpg")
    messagebox.showinfo(title="Success", message=f"Watermarked image saved")


# Configure UI
window = Tk()
window.title("Watermarking Application")
window.config(padx=50, pady=50, bg="white")

t1 = Label(text="Select an image: ", fg="black", bg="white", font=("Ariel", 13))
t1.grid(row=0, column=0, columnspan=2)
t1.config(pady=20)

select_image_btn = Button(text="Pick Image", command=select_image)
select_image_btn.grid(row=1, column=0)


t2 = Label(text="Select the logo: ", fg="black", bg="white", font=("Ariel", 13))
t2.grid(row=0, column=3, columnspan=2)
t2.config(pady=20)

select_logo_btn = Button(text="Pick Logo", command=select_logo)
select_logo_btn.grid(row=1, column=3)


empty_text = Label(text=" ", bg="white")
empty_text.grid(row=5, column=1)

logo_size_label = Label(text="Logo Size(widthxheight): ", fg="black", bg="white", font=("Ariel", 8))
logo_size_label.grid(row=6, column=0)

logo_size = Entry(width=15)
logo_size.grid(row=6, column=1, columnspan=2)
logo_size.insert(0, f"{str(DEFAULT_LOGO_SIZE[0])}x{str(DEFAULT_LOGO_SIZE[1])}")

logo_position_label = Label(text="Logo Position(x,y): ", fg="black", bg="white", font=("Ariel", 8))
logo_position_label.grid(row=7, column=0)

logo_position = Entry(width=15)
logo_position.grid(row=7, column=1, columnspan=1)
logo_position.insert(0, f"{str(DEFAULT_LOGO_POSITION[0])},{str(DEFAULT_LOGO_POSITION[1])}")


t3 = Label(text="Enter the text: ", fg="black", bg="white", font=("Ariel", 13))
t3.grid(row=9, column=0, columnspan=2)
t3.config(pady=20)

text_entry = Entry(width=30)
text_entry.grid(row=10, column=0, columnspan=2)

empty_text = Label(text=" ", bg="white")
empty_text.grid(row=11, column=1)

font_size_label = Label(text="Font Size(in pixels): ", fg="black", bg="white", font=("Ariel", 8))
font_size_label.grid(row=12, column=0)

font_size = Entry(width=15)
font_size.grid(row=12, column=1, columnspan=2)
font_size.insert(0, str(DEFAULT_FONT_SIZE))


empty_text = Label(text=" ", bg="white")
empty_text.grid(row=14, column=1)
empty_text.config(pady=30)


watermark_btn = Button(text="Apply Watermark and Save", command=apply_watermark)
watermark_btn.grid(row=15, column=1)

window.mainloop()
