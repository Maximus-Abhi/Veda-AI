import base64
import pymupdf


def convert_pdf_to_images(pdf_bytes):
    document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    page_images = []

    try:
        for page_number in range(len(document)):
            page = document[page_number]
            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False)

            image_bytes = pixmap.tobytes("png")
            page_images.append({
                "page": page_number + 1,
                "image": image_bytes,
                "width": pixmap.width,
                "height": pixmap.height,})

    finally:
        document.close()
    return page_images


def convert_pdf_to_base64_images(pdf_bytes):
    document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages = []

    try:
        for page_number in range(len(document)):
            page = document[page_number]

            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(1.5, 1.5),
                alpha=False)

            image_bytes = pixmap.tobytes("png")
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            pages.append({
                "page": page_number + 1,
                "image": image_base64,
                "width": pixmap.width,
                "height": pixmap.height,})

    finally:
        document.close()
    return pages


def extract_pdf_text(pdf_bytes):
    document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages = []

    try:
        for page_number in range(len(document)):
            page = document[page_number]

            pages.append({
                "page": page_number + 1,
                "text": page.get_text("text"),})

    finally:
        document.close()

    return pages