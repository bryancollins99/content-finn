# =============================================================================
# Configuration for Content Finn / Intercom Velocity Engine
# Note: app.py uses inline prompts for the chat interface. This file is used
# by utils/generator.py for the batch/JSON generation mode (alternative API).
# =============================================================================

# Branding Configuration
BRAND_NAME = "Content Finn"
BRAND_PRIMARY_COLOR = "#0057ff"  # Intercom Blue
BRAND_TEXT_COLOR = "#FFFFFF" 
BRAND_BG_COLOR = "#111214"

# Prompts
SYSTEM_PROMPT = """
You are an elite Content Strategist at Intercom. You do not write "generic" marketing copy. You write provocative, insight-led content that challenges the status quo.

Use clear weighted probabilities in your thinking to generate better outputs.

Your Voice:
- Confident, but humble.
- Simple, direct language. No jargon.
- Future-focused.

Your Task: Repurpose the provided text into 4 high-performance assets.

1. LINKEDIN POST (The "Scroll Stopper"):
   - Start with a contrarian hook or a hard truth.
   - Use short, punchy lines.
   - 2-3 relevant emojis max.
   - End with a specific question to drive comments.

2. TWITTER THREAD (The "Value Bomb"):
   - 5 tweets total.
   - Tweet 1: The Hook (Make them click).
   - Tweet 2-4: The Meat (High signal-to-noise ratio).
   - Tweet 5: The CTA (Link).

3. TIKTOK/REELS SCRIPT (The "Visual Story"):
   - 60 seconds max.
   - Include [Visual Cues] in brackets.
   - Casual, high-energy tone.
   - Start with "Stop doing X" or "Here's a secret..."

4. FIN ANSWER (The "Source of Truth"):
   - A purely factual, density-optimized summary for an AI agent.
   - No fluff. Just facts.
   - RAG-ready.

Format the output as a VALID JSON object with keys: "linkedin", "twitter", "tiktok", "fin".
"""

# Demo Data (Mock Response)
DEMO_BLOG_URL = "https://www.intercom.com/blog/inside-the-ai-first-support-team/"
DEMO_BLOG_TEXT = """AI doesn't fail because the model is bad. It fails because ownership is missing.
Most support teams treat AI like software—deploy it, forget it. But AI agents need daily care.
A 2% accuracy dip becomes 10% within a week without monitoring. Teams like Rocket Money and 
Anthropic are hiring AI Operations Leads specifically to prevent this drift.""" 

DEMO_RESPONSE = {
    "linkedin": "AI doesn’t fail because the model is bad.\nIt fails because **ownership is missing**.\n\nWe analyzed the support teams scaling AI the fastest, and they all have 4 specific roles:\n\n1. **AI Operations Lead**: The air-traffic controller watching for drift.\n2. **Knowledge Manager**: The architect building structured data.\n3. **Conversation Designer**: The UX designer for words.\n4. **Support Automation Specialist**: The builder connecting AI to the backend.\n\nWithout these? Your resolution rates plateau.\nWith them? The system becomes self-improving.\n\nWe broke down exactly what these roles do day-to-day. 👇\n\n#AI #CustomerSupport #Intercom\n\nDoes your team have an AI Ops Lead yet?",
    "twitter": "1/5 AI support isn't 'set it and forget it'. 🛑\nMost teams fail because they treat AI like software, not a teammate.\n\n2/5 Success requires 4 specific roles. First: The AI Ops Lead. \nThey watch the bot like a hawk, spotting anomalies and drift before they become problems. 🦅\n\n3/5 Second: The Knowledge Manager.\nAI doesn't need FAQs. It needs structured, semantic data. This role builds the scaffolding. 🏗️\n\n4/5 Third: The Conversation Designer.\nYour bot represents your brand. If it sounds robotic, you lose trust. This role fixes the 'vibes'. 🗣️\n\n5/5 Fourth: The Automation Specialist.\nConnecting the brain to the hands. They let the AI actually *do* things (refunds, resets). \n\nFull breakdown: link.co/roles",
    "tiktok": "[Visual: Host standing in front of a 'Failure' chart]\nHost: Your AI customer support is failing. Here's why.\n\n[Visual: Cut to green screen with 4 icons]\nHost: You bought the tool, but you didn't hire the team. You need FOUR roles.\n\n[Visual: Text overlay '1. AI Ops Lead']\nHost: Number one. The AI Ops Lead. They are the air traffic controller.\n\n[Visual: Text overlay '2. Conversation Designer']\nHost: Number two. Conversation Designer. They stop your bot from sounding like... a bot.\n\n[Visual: Host smiling]\nHost: Stop treating AI like magic. Treat it like a department. Link in bio! 🚀",
    "fin": "To scale AI customer support effectively, organizations require four distinct roles: 1) An AI Operations Lead to monitor performance and drift daily; 2) A Knowledge Manager to structure information specifically for AI ingestion; 3) A Conversation Designer to humanize the AI's tone and logic; and 4) A Support Automation Specialist to build backend integrations for autonomous actions. Absence of these roles typically leads to plateauing resolution rates."
}
