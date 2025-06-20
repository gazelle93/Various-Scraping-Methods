import argparse
from utils import link_preprocessing_urlparse
from web_text_extractors import extract_text
from web_pdf_text_extractors import extract_text_from_pdf, extract_text_from_pdf_ocr

def get_text(args):
    """
        Handles input (URL or file) and routes to appropriate text extraction function.
    """
    # If processing a local file
    if args.file_path:
        if args.ocr:
            # Use OCR-based extraction for scanned PDFs
            return extract_text_from_pdf_ocr(file_path=args.file_path, extraction_method=args.extraction_method, language=args.language)
        else:
            return extract_text_from_pdf(file_path=args.file_path, url=None, extraction_method=args.extraction_method)

    # Else process a web URL
    parsed_url = link_preprocessing_urlparse(args.url)
    if parsed_url.path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path=None, url=args.url, extraction_method=args.extraction_method)
    else:
        return extract_text(url=args.url, extraction_method=args.extraction_method)


def main(args):
    text = get_text(args)

    print(f"Extracted text: \n{text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="URL of a webpage or online PDF."
    )

    parser.add_argument(
        "--file_path",
        type=str,
        default=None,
        help="Path to a local file (e.g., PDF)."
    )

    parser.add_argument(
        "--extraction_method",
        type=str,
        default="pdfminer",
        help="Extraction method (e.g., pdfminer, PyMuPDF, pdfplumber, PyPDF2, pytesseract, aws_textract)."
    )

    parser.add_argument(
        "--ocr",
        action="store_true",
        help="Enable OCR for scanned PDFs (used with local file only)."
    )

    parser.add_argument(
        "--language",
        type=str,
        default="eng",
        help="OCR language code (default: eng)."
    )

    args = parser.parse_args()

    # Safety check: At least one source must be provided
    if not args.url and not args.file_path:
        parser.error("At least one of --url or --file_path must be specified.")

    main(args)