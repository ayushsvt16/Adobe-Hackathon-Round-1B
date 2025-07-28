def extract_key_sentences(section_text, keywords, max_sentences=2):
    """
    Return up to max_sentences from section_text containing any of the keywords.
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', section_text)
    matched = [s.strip() for s in sentences if any(kw.lower() in s.lower() for kw in keywords)]
    return " ".join(matched[:max_sentences])
