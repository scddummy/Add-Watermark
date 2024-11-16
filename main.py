from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math
import os
import pathlib

WM_FONT = ImageFont.truetype('arial.ttf', 36)


def find_diagonal_angle(width, height):
    tangent = height / width
    angle_radians = math.atan(tangent)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def get_image_file():
    x = askopenfilename()
    return x


def check_watermark():
    if not watermark.get():
        return False
    else:
        return True


def save_image():
    global file_path
    global file_name_sans_ext
    global file_ext
    global tk_image
    img = ImageTk.getimage(tk_image)
    img.show()
    img.save(f"{file_path}/{file_name_sans_ext}_watermark{file_ext}")


def open_image():
    if not check_watermark():
        instructions.config(text="enter watermark (please)")
    else:
        image_file = get_image_file()
        global file_path
        global file_name_sans_ext
        global file_ext
        global tk_image
        file_name = os.path.basename(image_file)
        file_path = os.path.dirname(image_file)
        file_ext = pathlib.Path(file_name).suffix
        file_name_sans_ext = pathlib.Path(file_name).stem
        if image_file:
            try:
                with Image.open(image_file).convert("RGBA") as base:
                    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

                    draw = ImageDraw.Draw(txt)
                    draw.text((base.width / 2, base.height / 2), watermark.get(), (0, 0, 0, 50), font=WM_FONT)
                    txt = txt.rotate(find_diagonal_angle(base.width, base.height)).resize(base.size)

                    out = Image.alpha_composite(base, txt)
                    tk_image = ImageTk.PhotoImage(out)

                    # noinspection PyTypeChecker
                    panel = Label(window, image=tk_image)
                    panel.image = tk_image
                    panel.grid(column=0, row=4, columnspan=4)

                    save_button.config(state=NORMAL)

            except (FileNotFoundError, OSError) as e:
                print(f"Error opening image: {e}")
        else:
            print("Error: No image file selected")

        return file_path, file_name, file_ext


# UI SETUP
window = Tk()
window.title("Watermarkify")
window.geometry("800x500")
window.config(padx=25, pady=25, bg="blue")
window.resizable(width=True, height=True)

instructions = Label(text="enter watermark", background="blue", fg="white", font=("Arial", 16, "normal"))
instructions.grid(column=1, row=0, columnspan=2)
instructions.config(pady=10)
watermark = Entry(width=50)
watermark.grid(column=1, row=1, columnspan=2)
blank = Label(text="", background="blue", font=("Arial", 2, "normal"))
blank.grid(column=1, row=2, columnspan=2)

upload_button = Button(text="upload image", width=18, command=open_image)
save_button = Button(text="save image", width=18, command=save_image, state=DISABLED)
upload_button.grid(column=1, row=3)
save_button.grid(column=2, row=3)

window.grid_columnconfigure((0, 3), weight=1)

window.mainloop()
