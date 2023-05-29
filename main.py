import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import blockchain as chain
import datetime
import glob
import cv2
import pandas as pd
import pathlib

blockchain = chain.Blockchain()
index = 0


def read_qr_code(filename):
    try:
        scan_img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(scan_img)
        return value
    except:
        return


def open_file():
    global image
    global image_label
    global img
    global resize_image

    upload_text.set('loading...')
    file = askopenfile(parent=root, mode='rb', title='Select a file')
    if file:
        print(file.name)

        # render updated image on gui
        img = Image.open(file.name)
        resize_image = img.resize((180, 180))
        image = ImageTk.PhotoImage(resize_image)
        image_label.configure(image=image)
        image_label.image = image

        value = read_qr_code(file.name)
        print(value)

    upload_text.set('Browse')

    # verify block
    new_project = chain.Project(value)
    status = chain.verify_project(new_project, blockchain)
    print(status)
    # update status on UI
    status_placeholder.set(status)


def add_block():
    global index

    file = askopenfile(parent=root, mode='rb', title='Select a file')
    if file:
        print(file.name)
        value = read_qr_code(file.name)
        print(value)

    # create new block on blockchain
    new_project = chain.Project(value)
    index = index + 1
    blockchain.add_block(chain.Block(index, datetime.datetime.now(), new_project.calculate_hash(), ""))

    print('Block added successfully')
    messagebox.showinfo("Success!!!", f"Block with id {value} successfully added on Blockchain!")


# GUI
root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=320, bg='white', borderwidth=0, highlightthickness=0)
canvas.grid(columnspan=3, rowspan=3)

# logo
logo = Image.open('images/logo1.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo, bg='white')
logo_label.image = logo
logo_label.grid(column=1, row=0)

# instructions
instructions = tk.Label(root, text="Upload the QR Code of Product", font=("Arial", 14), bg='white')
instructions.grid(column=1, row=1)

# button
# browse button
upload_text = tk.StringVar()
upload_button = tk.Button(root, command=lambda: open_file(), textvariable=upload_text, width=15, height=2, bg="#20bebe",
                          foreground="white", font=("Arial", 14))
upload_text.set("Upload")
upload_button.grid(column=1, row=2)

canvas = tk.Canvas(root, width=600, height=450, bg='white', borderwidth=0, highlightthickness=0)
canvas.grid(columnspan=3, rowspan=7)

# image
img = Image.open('images/upload.png')
resize_image = img.resize((180, 180))
image = ImageTk.PhotoImage(resize_image)
image_label = tk.Label(image=image, width=180, height=180, bg='white')
image_label.image = image
image_label.grid(column=1, row=3, pady=40)

# Disease Name
status_placeholder = tk.StringVar()
status_placeholder.set('Status Here')
status = tk.Label(root, textvariable=status_placeholder, font=('Arial', 20, "bold"), bg='white')
status.grid(column=1, row=4)

# Confidence label
detected_label = tk.Label(root, text='Upload new Product in Blockchain', font=('Arial', 12), bg='white')
detected_label.grid(column=1, row=5, pady=(25, 0))

store_text = tk.StringVar()
store_button = tk.Button(root, command=lambda: add_block(), textvariable=store_text, width=25, height=2, bg="#20bebe",
                         foreground="white", font=("Arial", 12))
store_text.set("Upload New Product")
store_button.grid(column=1, row=6)

# render window
# Create some projects
project1 = chain.Project("ABC-123")
project2 = chain.Project("ABC-456")
project3 = chain.Project("ABC-789")
projects = [chain.Project("ABC-123"), chain.Project("ABC-456"), chain.Project("ABC-789")]

# Add projects to the blockchain
for project in projects:
    index = index + 1
    blockchain.add_block(chain.Block(index, datetime.datetime.now(), project.calculate_hash(), ""))

# Verify project authenticity
chain.verify_project(project1, blockchain)
chain.verify_project(project2, blockchain)
chain.verify_project(project3, blockchain)

root.mainloop()
