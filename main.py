import os
import sys
from pathlib import Path

from pdf2image import convert_from_path, pdfinfo_from_path
from dotenv import load_dotenv

# Path to .env file (same directory as this script)
ENV_PATH = Path(__file__).resolve().with_name(".env")


def load_env():
    """Load variables from .env if it exists."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)


def save_env(pdf_path: str, root_output_dir: str, image_format: str, dpi: int):
    """Save last used config to .env."""
    lines = [
        f"PDF_FILE={pdf_path}",
        f"ROOT_OUTPUT_DIR={root_output_dir}",
        f"IMAGE_FORMAT={image_format}",
        f"IMAGE_DPI={dpi}",
    ]
    ENV_PATH.write_text("\n".join(lines))


def ask_with_default(prompt: str, default: str) -> str:
    """Ask user for input, showing a default value."""
    if default:
        answer = input(f"{prompt} [{default}]: ").strip()
        return answer or default
    else:
        return input(f"{prompt}: ").strip()


def pdf_to_images_stream(
    pdf_path: Path,
    output_dir: Path,
    image_format: str = "png",
    dpi: int = 300,
):
    """Convert PDF to images, processing one page at a time, into output_dir."""
    if not pdf_path.exists():
        print(f"ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Normalize format
    fmt = image_format.lower()
    if fmt not in ("png", "jpeg", "jpg"):
        print("ERROR: Image format must be 'png' or 'jpeg/jpg'.")
        sys.exit(1)

    # Extension for files
    extension = "png" if fmt == "png" else "jpg"
    pil_format = "PNG" if extension == "png" else "JPEG"

    # Check if images for this PDF already exist inside this folder
    pattern = f"{pdf_path.stem}_p*.{extension}"
    existing_files = list(output_dir.glob(pattern))

    if existing_files:
        print(f"Found existing images for '{pdf_path.name}' in '{output_dir}':")
        for f in existing_files:
            print(f"  - {f.name}")
        choice = input("Images already exist. Skip conversion? (y/N): ").strip().lower()
        if choice in ("y", "yes"):
            print("Skipping conversion.")
            return
        else:
            print("Continuing. Existing files with the same names will be overwritten.")

    # Get page count without loading all pages
    info = pdfinfo_from_path(str(pdf_path))
    total_pages = info.get("Pages", 0)

    print(f"Converting '{pdf_path}' ({total_pages} pages) to {extension.upper()} in '{output_dir}' at {dpi} DPI")

    for page_number in range(1, total_pages + 1):
        images = convert_from_path(
            str(pdf_path),
            dpi=dpi,
            first_page=page_number,
            last_page=page_number,
        )

        img = images[0]  # only one page requested
        output_file = output_dir / f"{pdf_path.stem}_p{page_number:03d}.{extension}"

        # For PNG / JPEG the default quality is usually fine; we could tweak JPEG quality if needed.
        if pil_format == "JPEG":
            img.save(output_file, pil_format, quality=95)  # slightly higher JPEG quality
        else:
            img.save(output_file, pil_format)

        print(f"Saved: {output_file}")

    print("Conversion completed.")


def main():
    load_env()

    # Read defaults from .env (if available)
    default_pdf = os.getenv("PDF_FILE", "").strip()
    default_root_output_dir = os.getenv("ROOT_OUTPUT_DIR", "converted_pdfs").strip()
    default_image_format = os.getenv("IMAGE_FORMAT", "png").strip()

    # DPI as string first (for prompt), then we will parse to int
    default_dpi_str = os.getenv("IMAGE_DPI", "300").strip()

    # Ask user, using .env values as defaults
    pdf_input = ask_with_default("Enter PDF file path", default_pdf or "document.pdf")
    root_output_dir_input = ask_with_default(
        "Enter ROOT output folder (will contain all PDF folders)",
        default_root_output_dir,
    )
    image_format_input = ask_with_default(
        "Enter image format (png/jpeg)",
        default_image_format or "png",
    )
    dpi_input_str = ask_with_default(
        "Enter DPI (e.g. 150–600)",
        default_dpi_str or "300",
    )

    # Parse DPI to int with a small safety net
    try:
        dpi_value = int(dpi_input_str)
        if dpi_value <= 0:
            raise ValueError
    except ValueError:
        print("Invalid DPI value. Falling back to 300.")
        dpi_value = 300

    # Suggest default subfolder name = PDF name without extension
    pdf_stem = Path(pdf_input).stem
    subfolder_default = pdf_stem
    subfolder_name = ask_with_default(
        "Enter subfolder name for this PDF inside the root folder",
        subfolder_default,
    )

    # Save choices to .env for next run (PDF path, ROOT folder, format, DPI)
    save_env(pdf_input, root_output_dir_input, image_format_input, dpi_value)

    # Build paths
    pdf_path = Path(pdf_input).expanduser().resolve()
    root_output_dir = Path(root_output_dir_input).expanduser().resolve()
    output_dir = root_output_dir / subfolder_name

    # Run conversion
    pdf_to_images_stream(
        pdf_path,
        output_dir,
        image_format=image_format_input,
        dpi=dpi_value,
    )


if __name__ == "__main__":
    main()

