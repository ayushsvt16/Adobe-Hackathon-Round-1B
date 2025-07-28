# Adobe Hackathon - Problem 1B: Personalized Summary Extraction

This repository contains the solution to **Problem 1B** from the Adobe Generative AI Hackathon. The goal is to extract **personalized summaries** from PDF documents based on a given **user persona** and **job description**.

---

## 🚀 Features

- 📑 **Outline Extraction**: Extracts hierarchical headings (Title, H1, H2, H3) using PDF structure
- 🧠 **Persona & Job Matching**: Matches document content with persona/job keywords
- 📊 **Section Ranking**: Ranks document sections by semantic relevance
- ✂️ **Summary Extraction**: Extracts concise summaries from the top-ranked sections
- 🐳 **Dockerized**: Lightweight and ready-to-deploy in a Docker container (under 200MB)

---

## 📁 Directory Structure

```
.
├── main.py                  # Entry point for the pipeline
├── extractor_optimized.py   # Extracts document structure
├── persona_job.py           # Loads persona & job files, extracts keywords
├── ranker.py                # Ranks document sections by relevance
├── summarizer.py            # Summarizes top-ranked sections
├── Dockerfile               # Lightweight Docker setup
```

---

## 🧪 Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the script

```bash
python main.py --pdf path/to/input.pdf --persona path/to/persona.json --job path/to/job.json
```

This will generate personalized content summaries from the input PDF.

---

## 🐳 Docker Usage

### Build Docker image

```bash
docker build -t adobe-solution-1b .
```

### Run Docker container

```bash
docker run -v $(pwd)/data:/app/data adobe-solution-1b \
  --pdf data/sample.pdf \
  --persona data/persona.json \
  --job data/job.json
```

---

## 📄 Problem Overview

> Given a PDF document and metadata (persona and job description), the task is to:
>
> - Match and rank sections by semantic similarity to the persona/job
> - Generate a short, meaningful summary of relevant sections


---

## ✅ Requirements

- Python 3.8+
- PyMuPDF (`fitz`)
- SentenceTransformers or Transformers
- scikit-learn, numpy, etc.

---

## 📦 Output

The script returns a structured list of the most relevant sections and their summaries based on persona-job alignment.

Example:
```json
[
  {
    "section_title": "Machine Learning in Healthcare",
    "page_number": 12,
    "summary": "This section outlines how ML models can detect anomalies in patient data..."
  }
]
```
