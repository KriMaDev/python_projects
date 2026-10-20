from pypdf import PdfReader, PdfWriter

from merge_pdf import merge_pdfs


def make_pdf(path, pages):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=200, height=200)
    writer.write(path)


def test_merge_pdfs_combines_pages_in_alphabetical_order(tmp_path):
    make_pdf(tmp_path / "b.pdf", pages=2)
    make_pdf(tmp_path / "a.pdf", pages=1)
    (tmp_path / "notes.txt").write_text("not a pdf")

    output = merge_pdfs(str(tmp_path))

    assert output == str(tmp_path / "output.pdf")
    assert len(PdfReader(output).pages) == 3


def test_merge_pdfs_skips_previous_output(tmp_path):
    make_pdf(tmp_path / "a.pdf", pages=1)
    make_pdf(tmp_path / "b.pdf", pages=1)

    merge_pdfs(str(tmp_path), "merged.pdf")
    output = merge_pdfs(str(tmp_path), "merged.pdf")

    assert len(PdfReader(output).pages) == 2


def test_merge_pdfs_empty_folder(tmp_path):
    assert merge_pdfs(str(tmp_path)) is None
    assert not (tmp_path / "output.pdf").exists()
