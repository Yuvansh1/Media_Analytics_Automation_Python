# -*- coding: utf-8 -*-

# To execute this script, use the following command in terminal: streamlit run <file_name>.py
# Ensure you have the required packages installed: streamlit, requests, beautifulsoup4

# -*- coding: utf-8 -*-

# To run: streamlit run BOA_Newsroom_analyzer.py

import os
import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key from environment file
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    st.error("Missing Gemini API key. Please check your .env file.")
    st.stop()

# Initialize Gemini model
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="Bank of America Newsroom Analyzer", layout="centered")
st.title("🏦 Bank of America Newsroom Analyzer")
st.write("Analyzing content from [Bank of America Newsroom](https://newsroom.bankofamerica.com/content/newsroom/home.html)...")

# Scrape page content
try:
    page_url = "https://newsroom.bankofamerica.com/content/newsroom/home.html"
    page_response = requests.get(page_url)
    soup = BeautifulSoup(page_response.text, "html.parser")
    body_text = soup.body.get_text(separator=" ", strip=True) if soup.body else ""
except Exception as e:
    st.error(f"Error fetching content: {e}")
    st.stop()

if not body_text:
    st.error("No content found in the page body.")
    st.stop()

# Prepare text for Gemini
sanitized_text = ' '.join(body_text.split())
input_chunk = sanitized_text[:3000]

gemini_prompt = f"""
You are reviewing the homepage content of Bank of America's newsroom:

{input_chunk}

Please address the following:
1. Highlight the main themes or subjects presented.
2. List any mentioned financial or ESG-related efforts.
3. Note any individuals quoted or mentioned.
4. Describe the bank's focus or priorities, if observable.
5. Wrap up with a brief three-line summary of the content.
"""

# Analyze
if st.button("🔍 Analyze Newsroom"):
    with st.spinner("Working on it..."):
        try:
            gemini_response = model.generate_content(gemini_prompt)
            raw_output = gemini_response.text.strip()

            formatted_output = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", raw_output)
            html_output = formatted_output.replace("\n", "<br>")

            st.success("Done analyzing.")
            st.subheader("🧠 Gemini's Breakdown")

            with st.expander("Click to view full analysis", expanded=True):
                st.markdown(
                    f"""
                    <div style='background-color:#f9f9f9; color:#111; padding: 20px; border-radius: 10px; border: 1px solid #ccc; font-size: 16px; line-height: 1.6'>
                        {html_output}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as err:
            st.error(f"Something went wrong: {err}")
            st.stop()
