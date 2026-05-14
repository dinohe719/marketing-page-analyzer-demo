import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page settings
st.set_page_config(page_title="Marketing Page Analyzer", page_icon="📊")

st.title("📊 Marketing Page Analyzer")
st.write("Enter a company marketing page URL and get a quick marketing analysis.")

url = st.text_input("Enter marketing page URL:")


def extract_page_text(url):
    """
    Extract visible text from a webpage.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary parts
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        # Limit text length to save API cost
        return text[:6000]

    except Exception as e:
        return f"Error extracting page: {e}"


def analyze_marketing_page(page_text):
    """
    Use OpenAI to analyze the marketing page.
    """
    prompt = f"""
You are a professional marketing strategist and conversion rate optimization expert.

Analyze the following marketing webpage text and generate a clear marketing audit report.

Use this exact structure:

# Marketing Page Analysis Report

## Overall Scores
- Overall Marketing Score: X/10
- Message Clarity Score: X/10
- Conversion Potential Score: X/10
- Differentiation Score: X/10

## 1. Target Audience
Explain who this page is mainly targeting.

## 2. Core Value Proposition
Explain the main promise of the product or company.

## 3. Customer Pain Points
List the main problems this page is trying to solve.

## 4. Tone and Messaging Style
Describe whether the tone is professional, friendly, technical, emotional, direct, etc.

## 5. Strengths
List 3 strengths of the marketing page.

## 6. Weaknesses
List 3 weaknesses of the marketing page.

## 7. Conversion Improvement Suggestions
Give 3 specific suggestions to improve sign-ups, demos, purchases, or user conversion.

## 8. One-Sentence Summary
Summarize the marketing effectiveness of the page in one sentence.

Webpage text:
{page_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert marketing page analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


if st.button("Analyze Page"):
    if not url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("Extracting and analyzing the page..."):
            page_text = extract_page_text(url)

            if page_text.startswith("Error"):
                st.error(page_text)
            else:
                result = analyze_marketing_page(page_text)

                st.subheader("Analysis Result")
                st.write(result)