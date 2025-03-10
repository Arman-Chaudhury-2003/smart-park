import cv2
import pytesseract
import numpy as np
import easyocr

# Use EasyOCR instead of Tesseract
reader = easyocr.Reader(['en'])

def process_image(image_path):
    # Read image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Denoise image (optional)
    processed = cv2.fastNlMeansDenoising(processed, None, 30, 7, 21)

    # OCR Recognition with EasyOCR
    plate_number = reader.readtext(image_path, detail=0)

    # Return result
    return plate_number[0] if plate_number else "Plate Not Detected"
