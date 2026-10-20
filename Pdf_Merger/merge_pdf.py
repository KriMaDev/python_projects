"""Merge every PDF in a folder into one file, in alphabetical order."""
import argparse
import os

from colorama import Fore, init
from pypdf import PdfWriter


def merge_pdfs(directory: str, output_filename: str = "output.pdf") -> str | None:
    """Merge all PDFs in directory into output_filename (saved in the same folder).

    The output file itself is skipped, so running the script twice doesn't merge it into itself.
    Returns the output path, or None if there was nothing to merge.
    """
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf') and f != output_filename]
    pdf_files.sort()  # Sort files alphabetically for a consistent order

    if not pdf_files:
        print(Fore.LIGHTRED_EX + f"No PDF files found in {directory}")
        return None

    # Initialize PdfWriter object (PdfMerger is deprecated)
    merger = PdfWriter()

    # Add each PDF to the merger
    for pdf_file in pdf_files:
        file_path = os.path.join(directory, pdf_file)
        print(Fore.LIGHTYELLOW_EX + f"Adding {pdf_file} to the merger.")
        merger.append(file_path)

    # Write the output file
    output_path = os.path.join(directory, output_filename)
    with open(output_path, "wb") as output_pdf:
        merger.write(output_pdf)
    merger.close()

    print(Fore.LIGHTGREEN_EX + f"All PDFs merged into {output_filename}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default=".", help="folder containing the PDFs (default: current folder)")
    parser.add_argument("-o", "--output", default="output.pdf", help="name of the merged file (default: output.pdf)")
    args = parser.parse_args()

    init(autoreset=True)

    if not os.path.isdir(args.directory):
        print(Fore.LIGHTRED_EX + f"{args.directory} is not a folder.")
        return
    merge_pdfs(args.directory, args.output)


if __name__ == "__main__":
    main()
