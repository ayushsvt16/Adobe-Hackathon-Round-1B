import os
import json
from datetime import datetime

from extractor_optimized import extract_outline
from persona_job import load_persona_and_job, extract_keywords
from ranker import rank_sections
from summarizer import extract_key_sentences

def get_section_bodies(pdf_path, outline):
    """
    For each heading in outline, extract text from that heading until the next heading (or page end).
    Returns list of dicts with section_title, section_text, page_number, document.
    """
    import fitz
    doc = fitz.open(pdf_path)
    headings = outline["outline"]
    results = []
    for idx, heading in enumerate(headings):
        page_idx = heading["page"] - 1
        title = heading["text"]
        page = doc[page_idx]
        blocks = page.get_text("blocks")

        # Find y-coord of this heading on the page
        start_y = None
        for b in blocks:
            btext = b[4].strip() if b[4] else ""
            if btext == title:
                start_y = b[1]
                break

        # Find the y of the next heading, if any on this page
        ending_y = None
        if idx + 1 < len(headings) and headings[idx + 1]["page"] == heading["page"]:
            next_title = headings[idx + 1]["text"]
            for b in blocks:
                btext = b[4].strip() if b[4] else ""
                if btext == next_title:
                    ending_y = b[1]
                    break

        # Collect blocks from start_y up to ending_y
        texts = []
        for b in blocks:
            if b[4]:
                if start_y is not None and b[1] >= start_y:
                    if ending_y is not None and b[1] >= ending_y:
                        break
                    texts.append(b[4])

        para = " ".join(texts).replace('\n', ' ').strip()
        results.append({
            "document": os.path.basename(pdf_path),
            "section_title": title,
            "section_text": para if para else title,
            "page_number": heading["page"]
        })

    doc.close()
    return results

def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # --- Step 1: Extract section bodies from each PDF ---
    all_sections = []
    for pdf_file in sorted(os.listdir(input_dir)):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            outline = extract_outline(pdf_path)
            all_sections.extend(get_section_bodies(pdf_path, outline))

    # --- Step 2: Load persona/job and EXPANDED keywords ---
    persona, job = load_persona_and_job(input_dir)
    core_keywords = extract_keywords(persona + " " + job)
    bonus_keywords = [
        "guide", "coastal", "adventure", "nightlife", "culinary", "experiences", "packing", "activities",
        "things to do", "restaurants", "hotels", "entertainment", "culture", "friends", "group", "tips",
        "trip", "planning", "must-see", "recommendations", "itinerary"
    ]
    keywords = set(core_keywords) | set(bonus_keywords)

    # --- Step 3: Score and rank sections across all PDFs ---
    ranked_sections = rank_sections(all_sections, keywords)
    top_sections = ranked_sections[:5]

    # --- Step 4: Subsection analysis: key sentences or fallback to head of section text
    subsection_analysis = []
    for sec in top_sections:
        summary = extract_key_sentences(sec["section_text"], keywords, max_sentences=2)
        if not summary:
            summary = sec["section_text"][:400]
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": summary,
            "page_number": sec["page_number"]
        })

    # --- Step 5: Output final JSON with timestamp ---
    output = {
        "metadata": {
            "input_documents": sorted([f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]),
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["section_title"],
                "importance_rank": i + 1,
                "page_number": sec["page_number"]
            }
            for i, sec in enumerate(top_sections)
        ],
        "subsection_analysis": subsection_analysis,
    }
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("✅ Output written to output/results.json")

if __name__ == "__main__":
    main()
