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
            # try to move `end` backwards to nearest separator for a cleaner break
            found = False
            for sep in separators:
                idx = text.rfind(sep, start, end)
                if idx != -1 and idx > start:
                    end = idx + len(sep)
                    found = True
                    break
            if not found:
                # fallback: keep the hard end
                end = min(start + chunk_size, text_len)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # advance start by chunk_size - overlap, but ensure progress to avoid infinite loop
        next_start = end - chunk_overlap
        if next_start <= start:
            # fallback: advance by nominal step
            next_start = start + (chunk_size - chunk_overlap)
        if next_start <= start:
            # last resort: move forward one character to guarantee progress
            next_start = start + 1

        # safety: prevent runaway chunking
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

    # Determine PDF path: prefer passed argument, then try a few sensible defaults
    pdf_path = args.pdf_path
    if not pdf_path:
        # Try multiple possible PDF names
        candidates = [
            os.path.join(os.path.dirname(__file__), "azure_cloud_computing_and_development_fundamentals.pdf")
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                pdf_path = candidate
                break

    if not pdf_path or not os.path.exists(pdf_path):
        print("ERROR: PDF not found. Provide a path with --pdf or place a PDF file next to this script.")
        print("Expected one of: azure_cloud_computing_and_development_fundamentals.pdf")
        print("Tried path:", pdf_path)
        raise FileNotFoundError(f"PDF not found at {pdf_path}")

    reader = PdfReader(pdf_path)
    pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
    full_text = "\n".join(pages_text)

    print(f"✅ Loaded PDF with {len(reader.pages)} pages")

    section_pattern = re.compile(r"^(\d+(\.\d+)*\.?\s+[A-Z][^\n]*?)$", re.MULTILINE)
    sections = [(m.group(1).strip(), m.start()) for m in section_pattern.finditer(full_text)]
    
    if not sections:
        print("⚠️  No numbered sections detected. Falling back to paragraph-based chunking...")
        paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
        chunks = []
        
        for para in paragraphs:
            para_chunks = split_text_simple(para, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
            for chunk_text in para_chunks:
                chunks.append({
                    "section": "Document Content",
                    "content": chunk_text
                })
        
        print(f"✅ Created {len(chunks)} chunks from {len(paragraphs)} paragraphs")
    else:
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
        
        print(f"✅ Created {len(chunks)} chunks from {len(sections)} sections")

    output_file = args.output or (os.path.splitext(pdf_path)[0] + "_chunks.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Chunks saved to: {output_file}")


if __name__ == "__main__":
    main()
