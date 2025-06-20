import os

YOUR_AWS_ACCESS_KEY_ID = ''
YOUR_AWS_SECRET_ACCESS_KEY = ''
YOUR_AWS_DEFAULT_REGION = ''


def get_pdf_content(url):
    import requests
    from io import BytesIO

    response = requests.get(url)
    response_content = BytesIO(response.content)

    return response, response_content

def pymupdf_pdf_extraction(file_path, url=None):
    import fitz  # pip install PyMuPDF
    response, _ = get_pdf_content(url)
    text = ""

    if url:
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            text = "".join([page.get_text() for page in doc])
    else:
        with fitz.open(file_path) as doc:
            text = "".join([page.get_text() for page in doc])

    return text


def pdfplumber_pdf_extraction(file_path, url=None):
    import pdfplumber
    _, response_content = get_pdf_content(url)
    text = ""

    if url:
        with pdfplumber.open(response_content) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    else:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

    return text

def pdfminer_pdf_extraction(file_path, url=None):
    from pdfminer.high_level import extract_text
    _, response_content = get_pdf_content(url)
    text = ""

    if url:
        text = extract_text(response_content)
    else:
        text = extract_text(file_path)

    return text

def pypdf2_pdf_extraction(file_path, url=None):
    from PyPDF2 import PdfReader
    _, response_content = get_pdf_content(url)
    text = ""

    if url:
        reader = PdfReader(response_content)
    else:
        reader = PdfReader(file_path)

    text = "".join([page.extract_text() or "" for page in reader.pages])

    return text

def extract_text_from_pdf(file_path, url=None, extraction_method='pdfminer'):
    """
        Extracts text from a PDF file using various libraries.

        Args:
            file_path (str): Path to the local PDF file.
            url (str, optional): If provided, downloads and reads PDF from the URL.
            extraction_method (str): Method to use: 'pdfminer', 'PyMuPDF', 'pdfplumber', or 'PyPDF2'.

        Returns:
            str: Extracted text.
    """
    text = ""

    if extraction_method == 'PyMuPDF':
        text = pymupdf_pdf_extraction(file_path, url)
    elif extraction_method == 'pdfplumber':
        text = pdfplumber_pdf_extraction(file_path, url)
    elif extraction_method == 'pdfminer':
        text = pdfminer_pdf_extraction(file_path, url)
    elif extraction_method == 'PyPDF2':
        text = pypdf2_pdf_extraction(file_path, url)
    else:
        raise ValueError(f"Unsupported extraction method: {extraction_method}")

    return text


def pytesseract_pdf_extraction(file_path, language):
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    text = ""

    # Convert PDF pages to images
    pages = convert_from_path(file_path, dpi=300)

    # OCR each page image
    for i, page_image in enumerate(pages):
        retrieved_text = pytesseract.image_to_string(page_image, lang=language)
        text += f"\nPage {i + 1}:\n{retrieved_text}"

    return text


def aws_textract_pdf_extraction(file_path):
    import boto3
    text = ""

    # You must define your AWS credentials in environment or through IAM roles
    os.environ['AWS_ACCESS_KEY_ID'] = YOUR_AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = YOUR_AWS_SECRET_ACCESS_KEY
    os.environ['AWS_DEFAULT_REGION'] = YOUR_AWS_DEFAULT_REGION

    textract_client = boto3.client('textract', region_name=YOUR_AWS_DEFAULT_REGION)

    # Read PDF file as bytes
    with open(file_path, "rb") as document:
        image_bytes = document.read()

    # Use AWS Textract to analyze the document
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=["TABLES", "FORMS"]
    )

    # Extract lines of text from the response
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'

    return text

def extract_text_from_pdf_ocr(file_path, extraction_method='pytesseract', language='eng'):
    """
        Extracts text from a scanned PDF file using OCR techniques.

        Args:
            file_path (str): Path to the local scanned PDF.
            extraction_method (str): OCR method to use: 'pytesseract' or 'aws_textract'.
            language (str): Language code for OCR (default: 'eng').

        Returns:
            str: Extracted OCR text.
    """
    text = ""

    if extraction_method == 'pytesseract':
        text = pytesseract_pdf_extraction(file_path, language)
    elif extraction_method == 'aws_textract':
        text = aws_textract_pdf_extraction(file_path)
    else:
        raise ValueError(f"Unsupported OCR extraction method: {extraction_method}")

    return text