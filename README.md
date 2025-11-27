## 📄  PDF → Images Converter (Python)

A lightweight, fully offline Python tool that converts every page of a
PDF file into individual PNG or JPEG images.
Designed for reliability, low memory usage, and a smooth terminal
experience.

### ✨ Key Features

-   🔧 100% offline — no internet and no subscription required
-   📄 One page at a time — prevents high memory usage on large PDFs
-   🖼️ Supports PNG and JPEG
-   📂 Automatic folder organization
-   🔍 Detects total pages automatically
-   ♻️ Skips or overwrites existing images (your choice)
-   💾 Saves last-used settings in a .env file
-   🧩 Fully cross-platform: Linux, macOS, Windows

### 🛠️ Installation

1. Install Python dependencies

    pip install pdf2image pillow python-dotenv

2. Install Poppler (required by pdf2image)

Ubuntu / Linux

    sudo apt-get update
    sudo apt-get install poppler-utils

macOS

    brew install poppler

Windows

Download Poppler binaries and add bin/ to PATH:

https://github.com/oschwartz10612/poppler-windows/releases/

### 🚀 Usage

Run the script:

    python your_script_name.py

You will be asked for:

1.  📄 PDF file path
2.  📁 Root output directory
3.  🖼️ Image format (png / jpeg)
4.  🎯 DPI value (e.g., 150, 300, 600)
5.  🗂️ Subfolder name for this PDF

### 📦 Output Structure

    converted_pdfs/
        document_name/
            document_name_p001.png
            document_name_p002.png
            document_name_p003.png

### ⚙️ Environment File

A .env file is created automatically:

    PDF_FILE=/path/to/last.pdf
    ROOT_OUTPUT_DIR=converted_pdfs
    IMAGE_FORMAT=png
    IMAGE_DPI=300

### 🧠 How It Works

-   Uses pdfinfo_from_path() to extract total page count
-   Calls convert_from_path() one page at a time
-   Saves each page with consistent naming
-   Prompts when previous images exist
-   Ensures safe paths using Pathlib

### 📝 License

This project is free to use, modify, and distribute.