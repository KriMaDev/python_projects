import os
from pypdf import PdfWriter
from colorama import Fore, init

init(autoreset=True)

def merge_pdfs(directory, output_filename="output.pdf"):
    # Initialize PdfWriter object (PdfMerger is deprecated)
    merger = PdfWriter()

    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    pdf_files.sort()  # Sort files alphabetically for a consistent order

    # Add each PDF to the merger
    for pdf_file in pdf_files:
        file_path = os.path.join(directory, pdf_file)
        print(Fore.LIGHTYELLOW_EX + f"Adding {pdf_file} to the merger.")
        merger.append(file_path)

    # Write the output file
    output_path = os.path.join(directory, output_filename)
    with open(output_path, "wb") as output_pdf:
        merger.write(output_pdf)
    
    print(Fore.LIGHTGREEN_EX + f"All PDFs merged into {output_filename}")

# Usage
directory = "C:\\git_reps\\Python_Scripts_Repo\\Pdf_Merger"  # Replace with your directory containing PDF files
merge_pdfs(directory)