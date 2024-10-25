# VNUHCM LIBRARY DOWNLOADER

This project provides a Python script to automatically download images from a specified URL range and combine them into a high-resolution PDF file.

## Download/Clone Repository

To get started, clone this repository to your local machine or download the ZIP file:

```bash
git clone https://github.com/longlephamtien/vnuhcm-lib-downloader.git
```

## Installation
<!-- Describe how to install the project -->
To install the project, you need to have Python installed on your machine. You can install Python from the official website. Once you have Python installed and source code, you can run the following command to install the required packages:
```bash
pip install -r requirement.txt
```
## Setup

After cloning the repository and installing the required libraries, follow these steps to set up your project:

1. **Locate the `base_url.txt` file:**
   - Open the `base_url.txt` file located in the root directory of your project.

2. **Configure the Base URL:**
   - In `base_url.txt`, set the base URL for downloading images. 
   - Replace the placeholder URL with the actual base URL from which you want to download images.
   - Example format:
     ```plaintext
     # Base URL for downloading images
     # Replace {page} in the URL with the page number to download each image sequentially
     https://example.com/images/page_{page}
     ```

3. **Specify the Page Range:**
   - Define the starting and ending page numbers in the same `base_url.txt` file.
   - Use the following format:
     ```plaintext
     START_PAGE: 1
     END_PAGE: 100
     ```

4. **Save Changes:**
   - After making the necessary modifications to `base_url.txt`, save the file.

### Example `base_url.txt` Configuration
```plaintext
https://example.com/images/page_{page}
START_PAGE: 1
END_PAGE: 100
```

## Usage
<!-- Describe how to use the project -->
To use the project, you need to run the following command:
```bash
python main.py
```
After the script completes execution, check the `downloaded_images` folder for downloaded images. The `batch_files` folder will contain batch PDFs, and a final high-resolution PDF will be saved as `output_high_resolution.pdf` in the main project directory.

