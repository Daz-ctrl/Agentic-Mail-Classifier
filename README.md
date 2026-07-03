# Agentic-Mail-Classifier & Triage Pipeline

An intelligent, multi-agent automated pipeline designed to monitor an incoming queue of documents, filter out threat/spam payloads, and extract key insights from safe corporate and internship opportunities. Powered by Generative AI (`gemini-2.5-flash`), the system reads file bytes directly, classifies data against strict JSON schemas, and automatically performs system-level folder containment.

## 🛠️ Project Architecture

1. **Ingestion Engine:** Automatically scans the root directory for any incoming `.pdf` files.
2. **Agent 1 (The AI Classifier):** Leverages the Google GenAI SDK to perform deep contextual scanning on raw file bytes. Utilizing `response_schema` backed by Pydantic, it guarantees zero-hallucination structural outputs classifying the document type and threat level.
3. **Automated File Router:** Automatically executes programmatic sorting, isolating suspicious items into a quarantined `Spam/` directory or moving valid communication into a `Legit/` directory.
4. **Agent 2 (The Triage Analyst):** Automatically acts on legitimate correspondence to parse out a 2-sentence Executive Brief and structural Action Items.

## 🚀 Technical Stack

- **Language:** Python 3.x
- **AI Infrastructure:** Google GenAI SDK (`gemini-2.5-flash`)
- **Data Validation:** Pydantic (Structured Outputs / JSON Schema enforcement)
- **File Automation:** Native `os`, `shutil`, and `glob` file handling modules

## 📦 Getting Started

### 1. Installation
Clone this repository and ensure you have the modern GenAI SDK and Pydantic libraries installed:
```bash
pip install google-genai pydantic
