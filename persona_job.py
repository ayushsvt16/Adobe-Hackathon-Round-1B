def load_persona_and_job(input_dir="input"):
    with open(f"{input_dir}/persona.txt", "r", encoding="utf-8") as f:
        persona = f.read()
    with open(f"{input_dir}/job.txt", "r", encoding="utf-8") as f:
        job = f.read()
    return persona.strip(), job.strip()

def extract_keywords(text):
    """Extract basic keywords from text—naive rule-based, simple for beginners."""
    import re
    stopwords = {
        "the", "and", "for", "this", "with", "are", "that", "from", "can",
        "not", "all", "but", "has", "will", "use", "you", "etc", "per", "who",
        "a", "of", "in", "to", "on", "is", "by", "an", "as", "at", "it", "be",
        "or"
    }
    words = re.findall(r'\w+', text.lower())
    return [w for w in set(words) if w not in stopwords and len(w) > 2]
