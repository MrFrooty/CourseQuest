import fitz

def load_pdf_text(pdf_stream):
    pdf_reader = fitz.open(stream=pdf_stream, filetype="pdf")
    num_pages = pdf_reader.page_count
    catalog_text = ""

    for page_num in range(num_pages):
        page = pdf_reader.load_page(page_num)
        catalog_text += page.get_text()
    
    return catalog_text