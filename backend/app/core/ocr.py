# backend/app/core/ocr.py

import pdfplumber
import pytesseract
from PIL import Image
import os
from app.config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_pdf(file_path: str) -> list:
    text_chunks = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                chunks = text.split("\n\n")  # basic paragraph split
                for j, chunk in enumerate(chunks):
                    text_chunks.append({
                        "text": chunk,
                        "page": i + 1,
                        "paragraph": j + 1
                    })
    return text_chunks

def extract_text_from_image(file_path: str) -> list:
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    chunks = text.split("\n\n")
    return [{
        "text": chunk,
        "page": 1,
        "paragraph": i + 1
    } for i, chunk in enumerate(chunks)]
