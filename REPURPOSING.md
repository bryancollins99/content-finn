# Repurposing Guide

## Overview
This tool is designed with a modular architecture, making it trivial to adapt for other companies, roles, or personal projects. The core logic (scraping -> generation -> presentation) is agnostic to the specific brand.

## How to Adapt This Tool

### 1. Changing the Brand Identity (`config.py`)
All visual and tonal elements are centralized in `config.py`.

- **Brand Colors & Logo**: Update `BRAND_PRIMARY_COLOR`, `BRAND_LOGO_URL`, and `BRAND_NAME`.
- **System Prompt**: The `SYSTEM_PROMPT` variable defines the AI's persona.
    - *Current*: "Director of Content at Intercom... confident, future-focused."
    - *New Example*: "Head of Growth at [Company]... data-driven, empathetic, casual."

### 2. Modifying the Output Format
The tool currently generates 4 specific assets (LinkedIn, Twitter, TikTok, Fin). To change this:
1. Update `SYSTEM_PROMPT` in `config.py` to request different keys (e.g., "blog_summary", "newsletter_intro").
2. Update the `st.tabs` section in `app.py` to match your new keys.

### 3. Swapping the Model
The tool uses Anthropic's Claude 3.5 Sonnet for high-quality creative writing.
- To use OpenAI (GPT-4o), modify `utils/generator.py` to use the `openai` client library instead of `anthropic`. The rest of the logic remains the same.

## Quick Start for Recruiters
If you are reviewing this code:
1. `pip install -r requirements.txt`
2. `streamlit run app.py`
3. Click "⚡ Run 30s Demo" to see the output without needing an API key.


