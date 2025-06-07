import os 
UPLOAD_DIR= os.path.join(os.path.dirname(__file__),"../../data")
TESSERACT_CMD=r"C:\Program Files\tesseract-ocr\tesseract.exe"
os.makedirs(UPLOAD_DIR,exist_ok=True)