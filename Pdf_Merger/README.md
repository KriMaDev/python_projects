# PDF Merger

Merges every PDF in a folder into one file, in alphabetical order. Handy for scans, invoices or
chapters you want as a single document. Name the files `01_...`, `02_...` to control the order.

| Script | What it does |
|---|---|
| `merge_pdf.py` | Merges all `*.pdf` files in a folder into `output.pdf` (saved in that same folder) |

## Setup

From the repository root, with your virtual environment active (see the [main README](../README.md#setup)):

```bash
pip install -r Pdf_Merger/requirements.txt
```

## How to run

```bash
python Pdf_Merger/merge_pdf.py "C:\Users\me\Documents\Scans"     # Windows
python Pdf_Merger/merge_pdf.py ~/Documents/scans                 # macOS / Linux
python Pdf_Merger/merge_pdf.py                                   # PDFs in the current folder
python Pdf_Merger/merge_pdf.py ~/Documents/scans -o invoices_2026.pdf
python Pdf_Merger/merge_pdf.py --help
```

| Argument | Default | Meaning |
|---|---|---|
| `directory` | current folder | Folder containing the PDFs |
| `-o`, `--output` | `output.pdf` | File name of the merged PDF |

The output file is skipped when collecting PDFs, so running the script twice won't merge it into itself.
An existing output file is overwritten.

## Example output

```text
$ python Pdf_Merger/merge_pdf.py ~/Documents/scans
Adding a_intro.pdf to the merger.
Adding b_chapter.pdf to the merger.
All PDFs merged into output.pdf
```

## Libraries

| Package | Used for | Licence |
|---|---|---|
| [pypdf](https://pypi.org/project/pypdf/) | Reading and writing PDFs (successor of PyPDF2) | BSD-3-Clause |
| [colorama](https://pypi.org/project/colorama/) | Coloured output on Windows | BSD-3-Clause |
