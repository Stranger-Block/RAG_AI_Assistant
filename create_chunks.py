from PyPDF2 import PdfReader
import json
import re
import os
import argparse
from typing import List


def split_text_simple(text: str, chunk_size: int = 800, chunk_overlap: int = 200, separators=None) -> List[str]:
    
    if separators is None:
        separators = ["\n", ".", " ", "•"]

    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        if end < text_len:
            found = False
            for sep in separators:
                idx = text.rfind(sep, start, end)
                if idx != -1 and idx > start:
                    end = idx + len(sep)
                    found = True
                    break
            if not found:
                end = min(start + chunk_size, text_len)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        next_start = end - chunk_overlap
        if next_start <= start:
            next_start = start + (chunk_size - chunk_overlap)
        if next_start <= start:
            next_start = start + 1

        if len(chunks) > 20000:
            raise MemoryError("Too many chunks generated (safety limit reached)")

        start = next_start
        if start < 0:
            start = 0
        if start >= text_len:
            break

    return chunks
def main():
    parser = argparse.ArgumentParser(description="Create overlapping text chunks from a PDF")
    parser.add_argument("--pdf", dest="pdf_path", help="Path to the PDF file", default=None)
    parser.add_argument("--output", dest="output", help="Output JSON file path", default=None)
    parser.add_argument("--chunk_size", type=int, default=800)
    parser.add_argument("--chunk_overlap", type=int, default=200)
    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not pdf_path:
        candidate = os.path.join(os.path.dirname(__file__), "azure_cloud_computing_and_development_fundamentals.pdf")
        if os.path.exists(candidate):
            pdf_path = candidate

    if not pdf_path or not os.path.exists(pdf_path):
        print("ERROR: PDF not found. Provide a path with --pdf or place `azure_cloud_computing_and_development_fundamentals.pdf` next to this script.")
        print("Tried path:", pdf_path)
        raise FileNotFoundError(f"PDF not found at {pdf_path}")

    reader = PdfReader(pdf_path)
    pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
    full_text = "\n".join(pages_text)

    print(f"✅ Loaded PDF with {len(reader.pages)} pages")

    # Section detection
    section_pattern = re.compile(r"(\d+(\.\d+)*\.? )\s+([A-Z][\w\s&\-]+)")
    sections = [(m.group(), m.start()) for m in section_pattern.finditer(full_text)]
    print(f"✅ Detected {len(sections)} sections")

    chunks = []

    for i, (section_title, start_pos) in enumerate(sections):
        end_pos = sections[i + 1][1] if i + 1 < len(sections) else len(full_text)
        section_text = full_text[start_pos:end_pos].strip()
        if not section_text:
            continue

        section_chunks = split_text_simple(section_text, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)

        for chunk_text in section_chunks:
            chunks.append({
                "section": section_title,
                "content": chunk_text
            })

    output_file = args.output or (os.path.splitext(pdf_path)[0] + "_chunks.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Created {len(chunks)} chunks from {len(sections)} sections")
    print(f"Chunks saved to: {output_file}")

if __name__ == "__main__":
    main()
