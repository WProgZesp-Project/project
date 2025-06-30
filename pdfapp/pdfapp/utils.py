from PyPDF2 import PdfMerger


def merge_pdfs(file_paths, output_path):
    """
    Scala wiele plików PDF w jeden.

    :param file_paths: Lista ścieżek do plików PDF do scalenia.
    :param output_path: Ścieżka do pliku wynikowego.
    """
    merger = PdfMerger()
    for pdf in file_paths:
        merger.append(pdf)
    with open(output_path, 'wb') as f_out:
        merger.write(f_out)
    merger.close()
