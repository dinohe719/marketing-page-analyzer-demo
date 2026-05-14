import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page config
st.set_page_config(
    page_title="Marketing Page Analyzer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }

    .hero {
        padding: 2rem 2.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #eef2ff 0%, #fdf2f8 100%);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #4b5563;
        line-height: 1.6;
    }

    .feature-card {
        padding: 1.2rem;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        height: 100%;
    }

    .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.4rem;
    }

    .feature-text {
        font-size: 0.9rem;
        color: #6b7280;
    }

    .result-box {
        padding: 1.5rem;
        border-radius: 20px;
        background-color: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
    }

    .small-caption {
        color: #6b7280;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ About")
    st.write(
        "This tool analyzes a company's marketing page and generates an AI-powered audit."
    )

    st.markdown("### What it analyzes")
    st.write("• Target audience")
    st.write("• Value proposition")
    st.write("• Customer pain points")
    st.write("• Messaging style")
    st.write("• Strengths and weaknesses")
    st.write("• Conversion suggestions")

    st.markdown("---")
    st.markdown("### Example URLs")
    st.code("https://www.notion.com/product")
    st.code("https://www.slack.com/")
    st.code("https://www.fireworks.ai/")

# Hero section
st.markdown("""
<div class="hero">
    <div class="hero-title">📊 Marketing Page Analyzer</div>
    <div class="hero-subtitle">
        Paste any company marketing page URL and receive an AI-generated marketing audit,
        including audience analysis, value proposition, messaging review, and conversion improvement ideas.
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🎯 Audience Insight</div>
        <div class="feature-text">Identify who the page is targeting and whether the message fits that audience.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">💬 Messaging Review</div>
        <div class="feature-text">Analyze the clarity, tone, and persuasiveness of the marketing language.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🚀 Conversion Ideas</div>
        <div class="feature-text">Get practical suggestions to improve sign-ups, demos, or purchases.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# Input area
st.markdown("### Analyze a marketing page")

url = st.text_input(
    "Enter a company marketing page URL:",
    placeholder="https://www.example.com/product"
)

analyze_button = st.button("🚀 Analyze Page", use_container_width=True)


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

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        title = soup.title.string if soup.title else "Untitled Page"

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return title, text[:6000]

    except Exception as e:
        return None, f"Error extracting page: {e}"


def analyze_marketing_page(page_title, page_text):
    """
    Use OpenAI to analyze the marketing page.
    """
    prompt = f"""
You are a professional marketing strategist and conversion rate optimization expert.

Analyze the following marketing webpage text and generate a clear marketing audit report.

Use this exact structure:

# Marketing Page Analysis Report

## Page Analyzed
Page title: {page_title}

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


if analyze_button:
    if not url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("Analyzing the page... This may take a few seconds."):
            page_title, page_text = extract_page_text(url)

            if page_title is None:
                st.error(page_text)
            else:
                result = analyze_marketing_page(page_title, page_text)

                st.success("Analysis complete!")

                st.markdown(f"""
                <div class="result-box">
                    <p class="small-caption">Analyzed page:</p>
                    <h3>{page_title}</h3>
                    <p class="small-caption">{url}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 📋 Analysis Report")
                st.markdown(result)

                st.download_button(
                    label="⬇️ Download Report",
                    data=result,
                    file_name="marketing_page_analysis.txt",
                    mime="text/plain",
                    use_container_width=True
                )