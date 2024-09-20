""" 
author: @rgbami on github
last updated: 20.09.24
to get started run
    pip install pymupdf pillow fpdf
version: 1.0
"""

import fitz  # PyMuPDF
from PIL import Image, ImageOps  # Pillow
from fpdf import FPDF
import io
import tempfile
import os
import tkinter as tk  # default GUI
from tkinter import filedialog 


#  Convert each page of the PDF to an image.
def pdf_to_images(pdf_path, dpi=300):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No such file: '{pdf_path}'")
    
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=dpi, colorspace="RGB")
        img_data = pix.tobytes("png")  # Ensure the image data is in PNG format
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    doc.close()
    return images


#   Invert the colors of each image.
def invert_colors(images):
    inverted_images = []
    for img in images:
        inverted_img = ImageOps.invert(img.convert("RGB"))
        inverted_images.append(inverted_img)
    return inverted_images


#    Save the list of images to a PDF file.
def save_images_to_pdf(images, output_pdf_path):
    pdf = FPDF(unit="pt", format=[images[0].width, images[0].height])
    for img in images:
        pdf.add_page()
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_img_file:
            img.save(temp_img_file.name, format='JPEG', quality=95)
            pdf.image(temp_img_file.name, 0, 0)
    pdf.output(output_pdf_path)


# Initialize Tkinter root
root = tk.Tk()
root.withdraw()  # Hide the root window

# Create a file dialog to select the input PDF file
input_pdf_path = filedialog.askopenfilename(
    title="Select Input PDF",
    filetypes=[("PDF files", "*.pdf")]
)

# Create a file dialog to specify the output PDF file
output_pdf_path = filedialog.asksaveasfilename(
    title="Save Output PDF As",
    defaultextension=".pdf",
    filetypes=[("PDF files", "*.pdf")]
)

# Check if the user selected both files
if input_pdf_path and output_pdf_path:
    # Convert PDF to images
    images = pdf_to_images(input_pdf_path)

    # Invert colors of the images
    inverted_images = invert_colors(images)

    # Save the inverted images back to a PDF
    save_images_to_pdf(inverted_images, output_pdf_path)
else:
    print("File selection was cancelled.")