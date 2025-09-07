#Usage: python ai_agent_pdf_extract.py --pdf dafinkers.pdf --json-out hand_safety.json
# ai_agent_pdf_extract.py
import os
import json
import re
import argparse
from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai import types

# ---------- config ----------
DEFAULT_MODEL = "gemini-1.5-flash"

SYSTEM_RULES = """
You are an information extraction agent. Extract a concise, structured JSON summary from a short narrative PDF.

Return a SINGLE JSON OBJECT with exactly these top-level keys (no extras):
- document_title: string
- content_type: string
- summary: string                     # 2–4 sentences max
- characters: [                       # list of character objects
    {
      "name": string,
      "role": string,
      "notable_details": [string]     # short phrases
    }
  ]
- locations: [                        # list of location objects
    {
      "name": string,
      "region": string or "N/A",
      "context": string               # what happens there
    }
  ]
- time_references: [                  # list of time references if any
    {
      "year": number or "N/A",
      "context": string
    }
  ]
- key_events: [string]                # 4–8 bullet points, past tense
- quotes: [string]                    # key lines verbatim from text (short)
- language_style_notes: {
    "dialect": string,
    "examples": [string]              # spellings or phrases showing dialect
  ]
- word_count_estimate: number         # rough count of words in the story

Rules:
1) Output JSON ONLY. No markdown, no explanations, no trailing text.
2) If an item is missing in the source, use "N/A" or [] as appropriate.
3) Quotes must be short and verbatim; do not invent lines.
4) Keep "summary" faithful and neutral.
5) Do not add fields beyond those specified.
"""

def ensure_json_object(text: str) -> dict:
    """Attempt to parse JSON. If wrapped in fences or with stray text, salvage the object."""
    s = text.strip()

    # Remove code fences if present
    if s.startswith("```"):
        s = s.strip("`")
        s = re.sub(r"^json", "", s, flags=re.IGNORECASE).strip()

    # Direct parse
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # Salvage first {...} block
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(s[start:end+1])
        raise

def extract_with_gemini(pdf_path: str, model_name: str = DEFAULT_MODEL) -> dict:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set")

    genai.configure(api_key=api_key)

    # Upload PDF as a file input
    uploaded = genai.upload_file(pdf_path)

    gen_config = types.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.2,
        max_output_tokens=4096,
    )

    model = genai.GenerativeModel(model_name)

    prompt = f"""{SYSTEM_RULES}
Return JSON now."""
    resp = model.generate_content(
        [{"role": "user", "parts": [prompt, uploaded]}],
        generation_config=gen_config,
        safety_settings=None,
    )

    if not resp or not getattr(resp, "candidates", None):
        raise RuntimeError("Empty response from model")

    obj = ensure_json_object(resp.text or "")
    return obj

def write_json(obj: dict, out_json: str):
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    return out_json

def main():
    parser = argparse.ArgumentParser(
        description="Extract structured JSON summary from a narrative PDF using Gemini 1.5 Flash"
    )
    parser.add_argument("--pdf", required=True, help="Path to input PDF")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model name")
    parser.add_argument("--json-out", default="extracted_summary.json", help="Output JSON file")
    args = parser.parse_args()

    obj = extract_with_gemini(args.pdf, model_name=args.model)
    out_path = write_json(obj, args.json_out)
    print(f"Wrote JSON to {out_path}")

if __name__ == "__main__":
    main()