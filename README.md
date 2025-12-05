# Content Fin | Intercom Velocity Engine

A prototype AI copywriter trained on Intercom's style guide. Built to demonstrate high-velocity content operations for the Director of Content role.

## Features

- **Content Fin Chat**: Paste any blog post or content, get instant multi-channel drafts (LinkedIn, Twitter, TikTok, RAG-optimized)
- **Draft History**: All generated content saved for review
- **Style Guide**: Built-in reference for Intercom's voice and tone

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (optional - works in demo mode without it)
export ANTHROPIC_API_KEY="your-key-here"

# Run
streamlit run app.py
```

## Deploy to Render

1. Push this repo to GitHub
2. Create a new **Web Service** on Render
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Add environment variable: `ANTHROPIC_API_KEY` = your key

## Project Structure

```
├── app.py              # Main Streamlit app (chat interface)
├── config.py           # Configuration & batch generation prompts
├── requirements.txt    # Dependencies
├── .gitignore          # Git ignore rules
├── .streamlit/
│   └── config.toml     # Streamlit theme (Intercom dark mode)
└── utils/
    ├── generator.py    # Batch AI generation (JSON output mode)
    └── scraper.py      # URL scraping for Intercom blog posts
```

## Built By

[Bryan Collins](https://bryancollins.com) - Prototype for Intercom Director of Content application.

