from pdf2image import convert_from_path, pdfinfo_from_path
from pathlib import Path

def pdf_to_images_stream(pdf_path: str, output_folder: str = "pages", dpi: int = 300):
    pdf_path = Path(pdf_path)
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get page count without loading pages
    info = pdfinfo_from_path(str(pdf_path))
    total_pages = info["Pages"]

    for page in range(1, total_pages + 1):
        images = convert_from_path(
            str(pdf_path),
            dpi=dpi,
            first_page=page,
            last_page=page,
        )
        img = images[0]  # only one page produced
        out_file = output_dir / f"{pdf_path.stem}_p{page:03d}.png"
        img.save(out_file, "PNG")
        print("Saved:", out_file)

if __name__ == "__main__":
    pdf_to_images_stream("my_document.pdf")

