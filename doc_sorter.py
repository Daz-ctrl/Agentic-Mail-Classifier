import os
import json
import shutil
import glob  # Added to find all PDF files automatically
from google import genai
from google.genai import types
from pydantic import BaseModel

# Initialize the Gemini Client
client = genai.Client()
MODEL_ID = 'gemini-2.5-flash'

# Structure for Agent 1's response
class DocumentClassification(BaseModel):
    document_type: str  
    is_spam: bool       
    confidence_score: float

def process_single_pdf(file_path):
    """Processes a single PDF file through the multi-agent pipeline."""
    # Extract just the filename (e.g., 'Goodmail.pdf') from the path
    file_name = os.path.basename(file_path)
    print(f"\n=============================================")
    print(f"📂 Processing: {file_name}")
    print(f"=============================================")
    
    # 1. Read the local PDF file bytes
    try:
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_name}: {e}")
        return

    # 🕵️‍♂️ AGENT 1: The Classifier
    print("🕵️‍♂️ Agent 1 (Classifier) is scanning document context...")
    
    prompt_agent_1 = """
    You are an AI Security Mail Classifier. Analyze this document file bytes carefully.
    Determine if this document is a legitimate piece of corporate/personal communication 
    (like an internship notice, company announcement, invoice) OR if it is Spam/Phishing.
    
    Return a valid JSON schema containing:
    - document_type (String description)
    - is_spam (Boolean: true if malicious/junk, false if clean)
    - confidence_score (Float between 0.0 and 1.0)
    """

    try:
        response_agent_1 = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                prompt_agent_1
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DocumentClassification,
                temperature=0.1
            )
        )
        
        result_data = json.loads(response_agent_1.text)
        is_spam_decision = result_data["is_spam"]
        doc_type = result_data["document_type"]
        print(f"📊 Agent 1 Result -> Type: {doc_type} | Is Spam: {is_spam_decision}")

    except Exception as e:
        print(f"❌ Agent 1 failed to process {file_name}: {e}")
        return

    # 📦 AUTO-SORTING ACTION
    destination_folder = "Spam" if is_spam_decision else "Legit"
    destination_path = os.path.join(destination_folder, file_name)

    # Make sure subfolders exist
    os.makedirs(destination_folder, exist_ok=True)

    try:
        shutil.move(file_path, destination_path)
        print(f"🚚 Action Taken: Moved to '{destination_folder}/' directory.")
    except Exception as e:
        print(f"⚠️ Could not move file: {e}")
        return

    # 📝 AGENT 2: Deep Summary (Only runs for clean files)
    if is_spam_decision:
        print(f"🛑 Agent 2 skipped deep summary: File quarantined as Spam.")
    else:
        print("📝 Agent 2 (Triage Analyst) is extracting key context...")
        
        prompt_agent_2 = """
        You are a Senior Executive Triage Analyst. Summarize this legitimate corporate document.
        Provide a 2-sentence Executive Summary and a clear bulleted list of Action Items or Next Steps mentioned.
        """

        try:
            with open(destination_path, "rb") as f:
                moved_pdf_bytes = f.read()

            response_agent_2 = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    types.Part.from_bytes(data=moved_pdf_bytes, mime_type="application/pdf"),
                    prompt_agent_2
                ]
            )
            
            print("\n--- AGENT 2 ANALYSIS SUMMARY ---")
            print(response_agent_2.text.strip())
            print("---------------------------------")
        except Exception as e:
            print(f"❌ Agent 2 failed to analyze summary: {e}")

def scan_and_process_folder():
    """Finds all PDFs in the current directory and runs them through the agents."""
    # Find all .pdf files in the current folder (ignores subfolders like Legit/Spam)
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print("🔍 No PDF files found in the main folder to process!")
        print("Make sure your PDFs are sitting directly in this folder (not inside Legit or Spam).")
        return

    print(f"🚀 Found {len(pdf_files)} PDF(s) to process. Starting batch pipeline...")
    
    for file_path in pdf_files:
        process_single_pdf(file_path)
        
    print("\n🏁 Batch processing complete! All files cleared from root directory.")

if __name__ == "__main__":
    scan_and_process_folder()