import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from preprocess import get_grayscale, add_border


def pil_to_cv2(pil_image):
    """
    Convert a PIL image to an OpenCV image (NumPy array).
    :param pil_image: Input PIL image.
    :return: OpenCV image.
    """

    open_cv_image = np.array(pil_image)

    return cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)


def is_image_file(file_path: str) -> bool:
    """
    Check if the file is an image based on its extension.
    :param file_path: Path to the file.
    :return: True if it's an image, False otherwise.
    """
    image_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".svg",
    )
    return file_path.lower().endswith(image_extensions)


def preprocess_image(image):
    image = get_grayscale(image=image)
   # image = add_border(image=image)
    return image


def pdf_to_images(pdf_path, first_page=19, last_page=19, dpi=300):
    """
    Convert a PDF file into a list of images (one per page).
    :param pdf_path: Path to the input PDF.
    :return: List of images (one for each page).
    """
    images = convert_from_path(
        pdf_path, dpi=dpi
    )

    for i, _ in enumerate(images):
        # images[i].save(f"{i+1}.png", "PNG")
        images[i] = preprocess_image(pil_to_cv2(images[i]))

    return images


def extract_text_from_image(image, lang="fas", config=""):
    """
    Extract text from a single image using Tesseract OCR.
    :param image: PIL Image object.
    :param lang: Language for OCR (default is Persian 'fas').
    :param config: Configuration options for Tesseract.
    :return: Extracted text as a string.
    """
    return pytesseract.image_to_string(image, lang=lang, config=config)


def load_image(image_path):
    """
    Load an image file using OpenCV.
    :param image_path: Path to the image file.
    :return: Image as a NumPy array.
    """
    image = cv2.imread(image_path)

    image = preprocess_image(image=image)

    return image


def process_inputs(inputs, dpi):
    """
    Process both PDFs and images and return a combined list of PIL images.
    :param inputs: List of input file paths (both PDFs and images).
    :return: List of images (PIL Image objects).
    """
    images = []
    for file_path in inputs:
        if file_path.lower().endswith(".pdf"):
            # Convert PDF to images
            images.extend(pdf_to_images(file_path, dpi=dpi))
        elif is_image_file(file_path):
            # Load image file directly
            images.append(load_image(file_path))
        else:
            print(f"Unsupported file format: {file_path}")
    return images


def extract_text_from_images(images, config, lang="fas"):
    """
    Apply OCR to a list of images and return a dictionary with page numbers and extracted text.
    :param images: List of PIL Image objects.
    :param lang: Language for OCR (default is Persian 'fas').
    :return: Dictionary where keys are page numbers and values are the extracted text.
    """
    ocr_data = {}
    for page_num, image in enumerate(images, start=1):
        text = extract_text_from_image(image, lang=lang, config=config)
        ocr_data[page_num] = text
    return ocr_data




