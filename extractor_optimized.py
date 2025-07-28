import fitz
import re
import json
import os
from typing import Dict, Any

def classify_heading_level(text: str, font_size: float, is_bold: bool, page_num: int, y_position: float) -> str:
    text = text.strip()
    if len(text) < 3 or text.lower() in ['page', 'of', 'and', 'the', 'for']:
        return None
    if re.match(r'^\d+\.\s', text):  # "1. Introduction"
        return "H1"
    elif re.match(r'^\d+\.\d+\s', text):  # "1.1 Overview"
        return "H2"
    elif re.match(r'^\d+\.\d+\.\d+\s', text):  # "1.1.1 Details"
        return "H3"
    heading_keywords = [
        r'^(introduction|overview|conclusion|summary|references|appendix|acknowledgements)',
        r'^(table of contents|revision history|abstract|executive summary)',
        r'^(chapter|section|part)\s+\d+',
        r'^(background|methodology|results|discussion|future work)'
    ]
    text_lower = text.lower()
    for pattern in heading_keywords:
        if re.search(pattern, text_lower):
            if font_size >= 16 or is_bold:
                return "H1"
            else:
                return "H2"
    if font_size >= 18:
        return "H1"
    elif font_size >= 14 and is_bold:
        return "H1" if page_num <= 2 else "H2"
    elif font_size >= 13:
        return "H2" if is_bold else "H3"
    elif font_size >= 12 and is_bold:
        return "H3"
    return None

def extract_title_from_first_page(page) -> str:
    title_candidates = []
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = " ".join(span["text"].strip() for span in line["spans"]).strip()
            if not line_text:
                continue
            max_size = max(span["size"] for span in line["spans"]) if line["spans"] else 0
            is_bold = any("Bold" in span.get("font", "") for span in line["spans"])
            if (len(line_text.split()) >= 3 and 
                not line_text.endswith(":") and
                not re.match(r'^\d+\.', line_text) and
                (max_size >= 16 or is_bold) and
                not line_text.lower().startswith(('page', 'chapter', 'section'))):
                title_candidates.append((line_text, max_size, is_bold))
    if title_candidates:
        title_candidates.sort(key=lambda x: (x[2], x[1]), reverse=True)
        return title_candidates[0][0]
    return ""

def extract_outline(pdf_path: str) -> Dict[str, Any]:
    try:
        doc = fitz.open(pdf_path)
        outline = []
        title = ""
        seen_headings = set()
        if len(doc) > 0:
            title = extract_title_from_first_page(doc[0])
        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    line_text = " ".join(span["text"].strip() for span in line["spans"]).strip()
                    if not line_text or line_text in seen_headings:
                        continue
                    max_size = max(span["size"] for span in line["spans"]) if line["spans"] else 0
                    is_bold = any("Bold" in span.get("font", "") for span in line["spans"])
                    y_position = line["bbox"][1] if "bbox" in line else 0
                    level = classify_heading_level(line_text, max_size, is_bold, page_num, y_position)
                    if level:
                        outline.append({
                            "level": level,
                            "text": line_text,
                            "page": page_num + 1
                        })
                        seen_headings.add(line_text)
        doc.close()
        return {
            "title": title,
            "outline": outline
        }
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return {
            "title": "",
            "outline": []
        }

if __name__ == "__main__":
    process_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(process_dir) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(process_dir, pdf_file)
        result = extract_outline(pdf_path)
        output_file = os.path.splitext(pdf_file)[0] + '.json'
        with open(os.path.join(output_dir, output_file), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    print("Done extracting outlines.")
