def score_section(section_text, keywords, section_title=None):
    score = sum(1 for kw in keywords if kw in section_text.lower())
    # Bonus for special phrases in titles
    if section_title:
        special_phrases = ["guide", "adventure", "nightlife", "packing", "culinary", "coastal", "experiences"]
        title_text = section_title.lower()
        for phrase in special_phrases:
            if phrase in title_text:
                score += 3  # or more for "guide"
    return score

def rank_sections(sections, keywords):
    ranked = []
    for sec in sections:
        score = score_section(sec["section_text"], keywords, section_title=sec["section_title"])
        sec["score"] = score
        ranked.append(sec)
    return sorted(ranked, key=lambda x: -x["score"])
