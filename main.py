import os
import requests
from PIL import Image
from PyPDF2 import PdfMerger

def load_base_url(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    base_url = None
    start_page = None
    end_page = None

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        if not base_url and line:
            base_url = line
        if "START_PAGE" in line:
            start_page = int(line.split(":")[-1].strip())
        if "END_PAGE" in line:
            end_page = int(line.split(":")[-1].strip())

    if not base_url or start_page is None or end_page is None:
        raise ValueError("Base URL or page numbers not found or invalid in base_url.txt.")

    return base_url, start_page, end_page

save_dir = "downloaded_images"  # Folder where images will be saved
batch_dir = "batch_files"  # Folder where batch PDFs will be stored

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

if not os.path.exists(batch_dir):
    os.makedirs(batch_dir)

def download_image(url, page_num):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            file_path = os.path.join(save_dir, f"page_{page_num}.jpg")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: page_{page_num}.jpg")
        else:
            print(f"Failed to download page {page_num}")
    except requests.exceptions.SSLError as e:
        print(f"SSL error occurred: {e}")

def download_all_images(base_url, start_page, end_page):
    for i in range(start_page, end_page + 1):
        url = base_url.format(page=i)
        download_image(url, i)


def process_batch(batch, batch_number, dpi=600):
    pdf_path = os.path.join(batch_dir, f"batch_{batch_number}.pdf")
    image_list = []
    
    for image_file in batch:
        image_path = os.path.join(save_dir, image_file)
        try:
            img = Image.open(image_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            image_list.append(img)
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")
    
    if image_list:
        try:
            image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:], dpi=(dpi, dpi))
            print(f"Batch {batch_number} saved successfully as {pdf_path}")
        except MemoryError:
            print(f"Memory error occurred while saving batch {batch_number}")
    return pdf_path if os.path.exists(pdf_path) else None

def convert_images_to_pdf():
    output_pdf = "output_high_resolution.pdf"

    image_files = [f for f in os.listdir(save_dir) if f.endswith(".jpg")]

    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    batch_size = 50  # Adjust the batch size based on available memory
    batches = [image_files[i:i + batch_size] for i in range(0, len(image_files), batch_size)]

    pdf_files = []
    for i, batch in enumerate(batches):
        pdf_file = process_batch(batch, i, dpi=600)  # Use higher DPI, like 600 for print-quality PDFs
        if pdf_file:
            pdf_files.append(pdf_file)

    if pdf_files:
        merger = PdfMerger()

        for pdf_file in pdf_files:
            merger.append(pdf_file)

        merger.write(output_pdf)
        merger.close()

        print(f"Final high-resolution PDF saved as {output_pdf}")
    else:
        print("No valid PDF files were generated.")

if __name__ == "__main__":
    try:
        base_url, start_page, end_page = load_base_url("base_url.txt")
        print(f"Base URL: {base_url}, Start Page: {start_page}, End Page: {end_page}")

        print("Starting image download...")
        download_all_images(base_url, start_page, end_page)
        print("Image download complete.")

        print("Converting images to PDF...")
        convert_images_to_pdf()
        print("PDF creation complete.")
    except Exception as e:
        print(e)
