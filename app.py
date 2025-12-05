import streamlit as st
import os
import time
from dotenv import load_dotenv
from utils.scraper import scrape_blog_post

# Load environment variables from .env file (for local development)
load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Content Finn | Intercom",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INTERCOM LOGO (5 bars + smile) - Clickable to return home ---
INTERCOM_LOGO_SVG = """
<a href="?home=true" style="text-decoration: none; cursor: pointer; display: inline-block;">
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="32" height="32" rx="6" fill="white"/>
  <rect x="5" y="7" width="2.5" height="11" rx="1.25" fill="black"/>
  <rect x="9.5" y="5" width="2.5" height="15" rx="1.25" fill="black"/>
  <rect x="14.75" y="7" width="2.5" height="11" rx="1.25" fill="black"/>
  <rect x="20" y="5" width="2.5" height="15" rx="1.25" fill="black"/>
  <rect x="24.5" y="7" width="2.5" height="11" rx="1.25" fill="black"/>
  <path d="M7 22 Q16 28 25 22" stroke="black" stroke-width="2.5" stroke-linecap="round" fill="none"/>
</svg>
</a>
"""

# --- MINIMAL CSS ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
    }
    
    .nav-item {
        padding: 10px 12px;
        border-radius: 6px;
        cursor: pointer;
        margin-bottom: 4px;
        color: #888;
        font-size: 14px;
        display: block;
        text-decoration: none;
    }
    
    .nav-item:hover {
        background-color: #1a1a1a;
        color: white;
    }
    
    .nav-item.active {
        background-color: #1a1a1a;
        color: white;
        font-weight: 600;
    }
    
</style>
""", unsafe_allow_html=True)

# --- CONTENT TYPES ---
CONTENT_TYPES = {
    "linkedin": "💼 LinkedIn Post",
    "x_post": "𝕏 Post",
    "youtube": "🎬 YouTube Script",
    "finn": "🤖 Finn Answer (RAG)",
    "landing": "🏠 Landing Page Copy",
    "email": "📧 Email Campaign",
    "seo": "🔍 SEO Headlines & Meta"
}

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "draft_history" not in st.session_state:
    st.session_state.draft_history = []

if "current_page" not in st.session_state:
    st.session_state.current_page = "finn"

# --- HANDLE LOGO CLICK (home navigation via query param) ---
query_params = st.query_params
if query_params.get("home") == "true":
    st.session_state.current_page = "finn"
    st.query_params.clear()
    st.rerun()

if "selected_types" not in st.session_state:
    st.session_state.selected_types = ["linkedin"]  # Default to LinkedIn

# --- SIDEBAR ---
with st.sidebar:
    # Clickable logo - returns to home (Content Finn)
    logo_col1, logo_col2 = st.columns([1, 3])
    with logo_col1:
        st.markdown(INTERCOM_LOGO_SVG, unsafe_allow_html=True)
    with logo_col2:
        st.markdown("**Intercom**")
    
    st.markdown("---")
    
    # Simple vertical navigation
    if st.button("⚡ Content Finn", use_container_width=True):
        st.session_state.current_page = "finn"
        st.session_state.messages = []  # Reset chat
        st.rerun()
    if st.button("🕒 Draft History", use_container_width=True):
        st.session_state.current_page = "history"
        st.rerun()
    if st.button("📖 Style Guide", use_container_width=True):
        st.session_state.current_page = "guide"
        st.rerun()
    
    st.markdown("---")
    
    # Demo button - shows hardcoded example output
    st.caption("Quick Start")
    if st.button("📺 View Demo Output", use_container_width=True):
        st.session_state.current_page = "demo"
        st.rerun()
    
    st.markdown("---")
    st.caption("Strategy Demos")
    if st.button("🎯 Content Pillars for Intercom", use_container_width=True):
        st.session_state.strategy_prompt = "pillars"
        st.session_state.current_page = "finn"
        st.rerun()
    if st.button("📅 Q1 Content Calendar", use_container_width=True):
        st.session_state.strategy_prompt = "calendar"
        st.session_state.current_page = "finn"
        st.rerun()
    
    # Spacer
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.caption("Director Prototype (v0.5)")
    st.caption("Built by [Bryan Collins](https://bryancollins.com)")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        st.success("🟢 Connected to Anthropic")
    else:
        st.warning("🟡 Demo Mode")

# --- MAIN CONTENT ---

if st.session_state.current_page == "guide":
    st.title("📖 Intercom Style Guide")
    st.markdown("---")
    
    # Use tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Core Approach", "🏗️ Content Patterns", "✍️ Style Mechanics", "💬 Personal at Scale"])
    
    with tab1:
        st.markdown("""
        ## Core Writing Approach
        
        ### Authoritative but Accessible
        We write from deep operational experience, not theory. Every claim is grounded in what we've seen work in production environments.
        
        > *Don't say "AI needs maintenance." Say "a 2% dip becomes a 10% drop within days."*
        
        ### Structure-First Thinking
        We don't ramble. Each section has a clear job:
        1. **Introduce the problem**
        2. **Show what it looks like in practice**
        3. **Explain why it matters now**
        
        ### Concrete Over Abstract
        Name specific tools (Fin Tasks, Simulations). Reference real companies (Rocket Money, Anthropic). Use actual numbers, not vague claims.
        
        | ❌ Abstract | ✅ Concrete |
        |-------------|-------------|
        | "AI requires ongoing attention" | "Without daily review, a 2% accuracy dip becomes 10% within a week" |
        | "Many companies are adopting this" | "Teams like Rocket Money and Anthropic are already hiring..." |
        | "It helps with various tasks" | "It processes refunds, resets passwords, and updates billing info" |
        """)
    
    with tab2:
        st.markdown("""
        ## Content Patterns
        
        ### The Hook Formula
        Start with a **counterintuitive truth** that creates tension you want resolved.
        
        **Pattern:** Short. Declarative. Creates immediate stakes.
        
        ✅ *"AI doesn't fail because the model is bad. It fails because ownership is missing."*
        
        ✅ *"Your support team isn't overwhelmed because they're bad. They're overwhelmed because the model is broken."*
        
        ---
        
        ### The Structure Pattern
        Every piece follows: **Problem → What it looks like → Why it exists now**
        
        **Example breakdown:**
        
        | Section | Purpose |
        |---------|---------|
        | Hook | State the counterintuitive truth |
        | Reality | Show the day-to-day of the problem |
        | Stakes | Why this matters *right now* |
        | Solution | What to do about it |
        | Action | Specific next step or question |
        
        ---
        
        ### LinkedIn Post Structure
        ```
        [Counterintuitive hook - 1-2 lines]
        
        [Specific example of what this looks like]
        
        [Why this matters in 2025]
        
        [What to do about it]
        
        [Question to drive comments]
        ```
        
        ---
        
        ### X Post Structure
        Single insight, maximum density. No threads. Lead with the contrarian take.
        """)
    
    with tab3:
        st.markdown("""
        ## Style Mechanics
        
        ### Voice Rules
        - **Confident, but humble** - "We built X" not "We tried to build X"
        - **Simple, direct language** - No jargon. Short sentences.
        - **Future-focused** - We're optimists about AI
        - **Punchy** - Sentence fragments for effect. Like this.
        
        ---
        
        ### Metaphors That Clarify
        Use metaphors as **functional shortcuts to understanding**, not poetic flourishes.
        
        ✅ *"Air-traffic controller for your AI Agent"* — instantly conveys monitoring + authority
        
        ✅ *"Knowledge scaffolding"* — implies structure that enables building
        
        ✅ *"Outcome engine"* — shifts from passive tool to active driver
        
        ---
        
        ### Credibility Markers (Woven Naturally)
        Don't brag. Just show proof:
        
        - *"Teams like Rocket Money and Anthropic are hiring..."*
        - *"Our Blueprint research identified..."*
        - *"Our own support team learned this early..."*
        
        You're selling without selling.
        
        ---
        
        ### Transitions That Maintain Momentum
        Each section should pull readers forward:
        
        ✅ *"This role is the answer to that fear."*
        
        ✅ *"Where the conversation designer shapes expression, the automation specialist shapes capability."*
        
        ---
        
        ### What to Cut
        - Delete "very", "really", "actually", "just"
        - No hashtags (ever)
        - No weasel words ("We believe", "We think", "Perhaps")
        - No over-designed formatting in personal messages
        """)
    
    with tab4:
        st.markdown("""
        ## Personal at Scale
        
        *"The right message. The right way. At the right time."* — Intercom's founding mantra
        
        ---
        
        ### The Core Philosophy
        We're not disguising automated messages as one-off notes. We're sending **genuinely personal messages** to customers at scale. There's a big difference.
        
        Impersonal messages are perfect if you want the recipient to do nothing.
        
        ---
        
        ### Personalization Rules
        
        **Use variables and data:**
        - First name, company name, specific usage data
        - *"You've created 47 projects this month"* > *"Many users create projects"*
        
        **Stay relevant and timely:**
        - ❌ Don't message pro users about pro features they already have
        - ❌ Don't ask new users for feedback before they've used the feature
        - ✅ Target based on who they are + what actions they take
        
        ---
        
        ### Message Style for Conversations
        
        > *"You don't spend hours designing your message to a friend — so why do it when talking to your customers?"*
        
        **Cut back on:**
        - Over-designed marketing templates
        - Full-screen takeovers
        - Heavy imagery and formatting
        - Bullets, headers, and "slick" grammar
        
        **Instead:**
        - Short-hand writing
        - Conversational tone
        - Style appropriate for a 1:1 chat
        
        ---
        
        ### Invite Conversation
        Always end by inviting questions. Show you're available for a real interaction.
        
        > *"Hit reply if you have questions — I read every response."*
        
        ---
        
        ### Do Things That Don't Scale
        It's a cliché because it works:
        - Personal video welcome messages
        - Handwritten notes to key customers
        - Individual outreach that can't be templated
        
        Set time aside each week for 1:1 human connection.
        """)

elif st.session_state.current_page == "demo":
    st.title("📺 Demo: AI-First Support Article")
    st.markdown("*This is a hardcoded demo showing example output from Content Finn.*")
    st.markdown("---")
    
    # Source article info
    st.markdown("### 📎 Source Article")
    st.info("**Inside the AI-First Support Team** — [intercom.com/blog](https://www.intercom.com/blog/inside-the-ai-first-support-team/)")
    
    with st.expander("View Original Content (excerpt)", expanded=False):
        st.markdown("""
AI doesn't fail because the model is bad. It fails because ownership is missing.

Most support teams treat AI like software—deploy it, forget it. But AI agents need daily care. A 2% accuracy dip becomes 10% within a week without monitoring.

Teams like Rocket Money and Anthropic are hiring AI Operations Leads specifically to prevent this drift. The role is emerging as one of the most critical in modern support organizations.

We've identified four key roles that make AI-first support teams successful:

1. **AI Operations Lead** — The "air-traffic controller" who monitors performance daily
2. **Knowledge Manager** — Keeps content accurate and complete  
3. **Conversation Designer** — Shapes how AI sounds and responds
4. **Automation Specialist** — Builds workflows that take action

Without intentional ownership, AI performance inevitably plateaus. The teams scaling AI fastest treat it as a product requiring dedicated ownership, not a tool that runs itself.
        """)
    
    st.markdown("---")
    st.markdown("### 🎯 Generated Content")
    
    # Tabs for different content types
    demo_tab1, demo_tab2, demo_tab3, demo_tab4, demo_tab5, demo_tab6, demo_tab7 = st.tabs([
        "💼 LinkedIn", "𝕏 Post", "🎬 YouTube", "🤖 Finn RAG", "🏠 Landing", "📧 Email", "🔍 SEO"
    ])
    
    with demo_tab1:
        st.markdown("""
**💼 LinkedIn Post**

AI doesn't fail because the model is bad.

It fails because ownership is missing.

We've been studying what separates teams that scale AI from teams that stall. The difference isn't budget. It's not technology. It's four roles:

1. AI Operations Lead – the "air-traffic controller" who monitors performance daily
2. Knowledge Manager – keeps content accurate and complete
3. Conversation Designer – shapes how AI sounds and responds
4. Automation Specialist – builds workflows that take action

Without intentional ownership, a 2% dip becomes a 10% drop within days.

The teams winning at AI aren't hoping it works. They're treating it like a product that needs a team.

Which of these roles does your org have today?
        """)
        st.download_button("📥 Download", "AI doesn't fail because the model is bad...", file_name="linkedin_post.txt", key="demo_dl_linkedin")
    
    with demo_tab2:
        st.markdown("""
**𝕏 Post**

AI doesn't fail because the model is bad. It fails because ownership is missing. 

The teams scaling AI fastest have 4 roles: AI Ops Lead, Knowledge Manager, Conversation Designer, Automation Specialist. 

No ownership = inevitable drift.
        """)
        st.download_button("📥 Download", "AI doesn't fail because the model is bad...", file_name="x_post.txt", key="demo_dl_x")
    
    with demo_tab3:
        st.markdown("""
**🎬 YouTube Script (2-3 min)**

[Open on host at desk]

Why does AI work brilliantly for some support teams and completely stall for others?

[Cut to graphic: "AI Performance Over Time" chart showing drift]

It's not the model. It's not the data. It's ownership.

[Back to host]

I've been studying teams that scale AI successfully, and they all have something in common: four distinct roles.

[Show role 1 graphic]

First, the AI Operations Lead. Think of them as an air-traffic controller. They watch performance daily, catch drift before it becomes disaster. A 2% dip? They see it. They fix it.

[Show role 2 graphic]

Second, Knowledge Manager. They ensure the AI has accurate, complete information. Stale docs = stale answers.

[Show role 3 graphic]

Third, Conversation Designer. They shape tone, personality, edge cases. They make the AI sound human, not robotic.

[Show role 4 graphic]

Fourth, Automation Specialist. They build workflows so the AI doesn't just answer—it takes action.

[Back to host, closing]

Without these roles, AI plateaus. With them, it compounds. The question isn't whether your AI is good enough. It's whether you're owning it.

Link in description to the full breakdown.
        """)
        st.download_button("📥 Download", "[Open on host at desk]...", file_name="youtube_script.txt", key="demo_dl_yt")
    
    with demo_tab4:
        st.markdown("""
**🤖 Finn Answer (RAG)**

An AI-first support team requires four key roles for sustained success: 

(1) **AI Operations Lead** – monitors daily performance, catches drift, routes fixes
(2) **Knowledge Manager** – maintains accurate help content
(3) **Conversation Designer** – shapes AI tone and handles edge cases
(4) **Automation Specialist** – builds action workflows

Without intentional ownership, AI performance inevitably plateaus. Teams scaling AI fastest treat it as a product requiring dedicated ownership, not a tool that runs itself.
        """)
        st.download_button("📥 Download", "An AI-first support team requires four key roles...", file_name="finn_answer.txt", key="demo_dl_finn")
    
    with demo_tab5:
        st.markdown("""
**🏠 Landing Page Copy**

---

**Hero Headline:**
# AI Doesn't Fail. Ownership Does.

**Subheadline:**
The teams scaling AI fastest have four roles working together. Learn how to build an AI-first support organization that compounds instead of plateaus.

**Feature Bullets:**
• **AI Operations Lead:** Your air-traffic controller for AI performance
• **Knowledge Manager:** Keeps your AI accurate and up-to-date
• **Conversation Designer:** Makes your AI sound human
• **Automation Specialist:** Builds workflows that take action

**CTA:**
→ Build Your AI Team
        """)
        st.download_button("📥 Download", "AI Doesn't Fail. Ownership Does...", file_name="landing_page.txt", key="demo_dl_landing")
    
    with demo_tab6:
        st.markdown("""
**📧 Email Campaign**

---

**Subject:** Why your AI is drifting (and how to fix it)

**Preview:** It's not the model. It's the missing ownership.

---

Hey {{first_name}},

Here's something we've learned from teams scaling AI: performance doesn't plateau because the technology fails.

It plateaus because no one owns it.

The teams seeing compounding gains have four roles in place:
→ AI Ops Lead (catches drift before it spreads)
→ Knowledge Manager (keeps content sharp)
→ Conversation Designer (nails the tone)
→ Automation Specialist (builds action workflows)

Without these? A 2% dip becomes 10% within days.

We wrote up exactly what each role does day-to-day. Worth a read if you're seeing your AI performance flatten.

[Read the Breakdown]

— The Intercom Team
        """)
        st.download_button("📥 Download", "Subject: Why your AI is drifting...", file_name="email_campaign.txt", key="demo_dl_email")
    
    with demo_tab7:
        st.markdown("""
**🔍 SEO Headlines & Meta**

---

**Meta Title:**
AI-First Support Team: 4 Roles That Make AI Actually Work | Intercom

**Meta Description:**
AI fails without ownership. Learn the 4 roles—AI Ops Lead, Knowledge Manager, Conversation Designer, Automation Specialist—that separate scaling teams from stalling ones.

**H1 Alternatives:**
• The 4 Roles Every AI-First Support Team Needs
• Why AI Plateaus (And the Team Structure That Fixes It)
• Inside the AI-First Support Team: Roles, Responsibilities, Results
        """)
        st.download_button("📥 Download", "Meta Title: AI-First Support Team...", file_name="seo_meta.txt", key="demo_dl_seo")
    
    st.markdown("---")
    st.success("✨ **This is example output.** Go to Content Finn to generate your own content from any article or URL.")
    
    if st.button("⚡ Try Content Finn with your own content", use_container_width=True):
        st.session_state.current_page = "finn"
        st.rerun()

elif st.session_state.current_page == "history":
    st.title("🕒 Draft History")
    st.markdown("---")
    
    if not st.session_state.draft_history:
        st.info("No drafts yet. Go to Content Finn and paste some content to generate drafts.")
    else:
        for i, draft in enumerate(reversed(st.session_state.draft_history)):
            with st.expander(f"Draft {len(st.session_state.draft_history) - i}: {draft.get('preview', 'Untitled')[:50]}..."):
                st.markdown(draft.get('content', ''))
                st.caption(f"Generated: {draft.get('timestamp', 'Unknown')}")
                
                # Download button for each draft
                st.download_button(
                    "📥 Download as TXT",
                    draft.get('content', ''),
                    file_name=f"draft_{len(st.session_state.draft_history) - i}.txt",
                    mime="text/plain"
                )

else:  # Content Finn (default)
    # Handle example URL if triggered from sidebar
    if "example_url" in st.session_state and st.session_state.example_url:
        url = st.session_state.example_url
        st.session_state.example_url = None  # Clear it
        
        with st.spinner("Fetching article..."):
            scraped = scrape_blog_post(url)
        
        if scraped:
            st.session_state.pending_content = scraped
            st.session_state.pending_url = url
    
    # Handle strategy prompts from sidebar
    if "strategy_prompt" in st.session_state and st.session_state.strategy_prompt:
        strategy_type = st.session_state.strategy_prompt
        st.session_state.strategy_prompt = None  # Clear it
        
        # Pre-baked strategic content
        STRATEGY_RESPONSES = {
            "pillars": {
                "user_msg": "🎯 Show me your content pillar strategy for Intercom",
                "response": """**Content Finn**

Based on Intercom's positioning and 2025 market dynamics, here are **3 content pillars** I'd prioritize as Director of Content:

---

## 🏛️ Pillar 1: AI-First Support Operations

**Target Audience:** Support leaders navigating the AI transition  
**Strategic Goal:** Position Intercom as the authority on AI support transformation

**Content Mix:**
- Long-form guides ("The Complete AI Support Playbook")
- Benchmark reports ("State of AI in Customer Service 2025")
- Case studies with hard ROI numbers
- Executive interview series

**Example Headlines:**
- "The AI Support Maturity Model: Where Does Your Team Rank?"
- "Why 73% of AI Support Rollouts Fail (And How to Be the 27%)"
- "From 2,000 Tickets to 200: Inside Rocket Money's AI Transformation"

---

## 🏛️ Pillar 2: The Human + AI Playbook

**Target Audience:** IC support reps worried about their role; mid-level managers  
**Strategic Goal:** Own the narrative that AI *elevates* human work

**Content Mix:**
- Career development guides
- Day-in-the-life features
- Skills-focused practical content
- Community spotlights

**Example Headlines:**
- "5 Skills That Make You Irreplaceable in an AI-First Team"
- "Meet the AI Agent Manager: The Hottest New Role in Support"
- "What Top Support Reps Do Differently When Working With Fin"

---

## 🏛️ Pillar 3: Fin in Action (Product-Led Stories)

**Target Audience:** Prospects actively evaluating solutions  
**Strategic Goal:** Convert consideration into demo requests

**Content Mix:**
- Customer success stories with specifics
- Comparison content (tasteful, not attack-mode)
- ROI calculators and interactive tools
- "How to" implementation guides

**Example Headlines:**
- "How [Customer] Reduced Ticket Volume 47% in 30 Days with Fin"
- "Fin vs. Traditional Chatbots: What 500 Support Leaders Learned"
- "The 15-Minute Fin Setup That Saved One Team 20 Hours/Week"

---

### Why These Three?

Each pillar maps to a stage in the buyer journey:

| Pillar | Funnel Stage | Primary CTA |
|--------|--------------|-------------|
| AI-First Operations | Awareness | Newsletter signup |
| Human + AI Playbook | Consideration | Resource download |
| Fin in Action | Decision | Demo request |

This creates a content engine that feeds the full funnel while reinforcing Intercom's core message: **AI-first support is the future, and Intercom is the partner to get you there.**"""
            },
            "calendar": {
                "user_msg": "📅 Show me a Q1 content calendar for Intercom",
                "response": """**Content Finn**

Here's a strategic **Q1 2025 Content Calendar** aligned with Intercom's priorities and market timing:

---

## 📅 JANUARY: "New Year, New Support Stack"

*Theme: AI Foundation Month — Capitalize on Q1 planning cycles*

| Week | 📝 Blog | 💼 LinkedIn | 🎬 Video | 📧 Email |
|------|---------|-------------|----------|----------|
| **W1** | "2025 State of AI Support" Report Launch | Report highlights carousel | 3-min report explainer | Report to subscriber list |
| **W2** | "Setting Up Your AI Agent: Week 1 Checklist" | Quick wins tips | Setup walkthrough | Drip 1: New year resolution |
| **W3** | Customer Story: [Q4 Win] | Quote graphic + metrics | 2-min interview clip | Case study spotlight |
| **W4** | "5 AI Support Mistakes That Kill ROI" | Contrarian hook post | Reaction/commentary | Drip 2: Mistake to avoid |

**🎯 January Goal:** 50K report downloads, 200 demo requests from report CTA

---

## 📅 FEBRUARY: "The Human Side of AI Support"

*Theme: Human + AI Month — Counter the "AI replaces jobs" narrative*

| Week | 📝 Blog | 💼 LinkedIn | 🎬 Video | 📧 Email |
|------|---------|-------------|----------|----------|
| **W1** | "The AI Agent Manager: Hottest Role in Support" | Day-in-the-life thread | Job shadow video | Career content promo |
| **W2** | "Skills That Make You Irreplaceable" | Skill tips carousel | Expert interview | Drip 3: Upskilling |
| **W3** | "Inside [Customer]'s Human + AI Workflow" | Workflow breakdown | Process tour | Case study spotlight |
| **W4** | "Building Trust Between Agents and AI" | Personal story post | Team culture video | Drip 4: Culture shift |

**🎯 February Goal:** 30% increase in career content engagement, talent brand visibility

---

## 📅 MARCH: "Fin in Action"

*Theme: Product-Led Month — Push toward Q1 close*

| Week | 📝 Blog | 💼 LinkedIn | 🎬 Video | 📧 Email |
|------|---------|-------------|----------|----------|
| **W1** | "Fin vs. [Competitor]: What We Learned" | Comparison insights | Head-to-head demo | Competitor intel |
| **W2** | "The 15-Minute Setup That Saved 20 Hours/Week" | Quick ROI story | Speed setup video | Implementation tips |
| **W3** | ROI Calculator Launch + Blog | Calculator demo post | How to use video | Tool launch email |
| **W4** | Q1 Customer Roundup: "Top 10 Fin Wins" | Celebration carousel | Highlight reel | Q1 wrap email |

**🎯 March Goal:** 300 demo requests, Q1 pipeline target hit

---

## 🔄 Content Repurposing Engine

Each flagship piece becomes 10+ assets:

```
1 Blog Post
    → 1 LinkedIn post (hook + link)
    → 1 X thread (key insights)
    → 1 Email excerpt
    → 1 Short-form video (60s)
    → 3 Quote graphics
    → 1 Slide deck (for sales)
    → 1 Fin Answer (RAG)
```

This is where Content Finn accelerates the team—turning 1 piece into 10 in minutes, not days.

---

## 📊 Q1 KPIs

| Metric | Target | Current Baseline |
|--------|--------|------------------|
| Organic traffic | +25% | TBD |
| Demo requests from content | 500 | TBD |
| Email list growth | +15% | TBD |
| LinkedIn engagement rate | 5%+ | TBD |
| Report downloads | 50K | — |

---

*This calendar balances thought leadership (Pillar 1), talent brand (Pillar 2), and conversion content (Pillar 3) across the quarter.*"""
            }
        }
        
        if strategy_type in STRATEGY_RESPONSES:
            response_data = STRATEGY_RESPONSES[strategy_type]
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": response_data["user_msg"]
            })
            # Add strategic response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_data["response"]
            })
    
    # Pre-populate with intro if empty
    if not st.session_state.messages:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """**Content Finn** (v0.5)

Hello. I am Content Finn. I am trained on the Intercom Style Guide.

**Select your output formats below**, then paste a blog post, URL, or content.

Available formats:
- 💼 LinkedIn post
- 𝕏 Post
- 🎬 YouTube script
- 🤖 Finn Answer (RAG)
- 🏠 Landing Page Copy
- 📧 Email Campaign
- 🔍 SEO Headlines & Meta

"""
            }
        ]
    
    # Render chat
    for idx, msg in enumerate(st.session_state.messages):
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
            # Add share/download buttons for assistant responses (except intro)
            if msg["role"] == "assistant" and "I'll transform it into" not in msg["content"]:
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    st.download_button(
                        "📥 Download",
                        msg["content"],
                        file_name="content_finn_output.txt",
                        mime="text/plain",
                        key=f"dl_{idx}"
                    )
                with col2:
                    if st.button("📋 Copy", key=f"cp_{idx}"):
                        st.toast("Content copied! Use Ctrl+C after selecting.")
    
    # Check for pending content from example button
    pending_prompt = None
    if "pending_content" in st.session_state and st.session_state.pending_content:
        pending_prompt = st.session_state.pending_content
        pending_url = st.session_state.get("pending_url", "")
        st.session_state.pending_content = None
        st.session_state.pending_url = None
        
        user_msg = f"📎 *Fetched from:* [{pending_url}]({pending_url})\n\n---\n\n{pending_prompt[:800]}..."
        st.session_state.messages.append({"role": "user", "content": user_msg})
    
    # Custom input area (like Cursor's layout)
    st.markdown("---")
    
    # Initialize input key for clearing
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    
    # Text input (key changes after submission to clear it)
    user_input = st.text_area(
        "Input",
        placeholder="Paste content, a URL, or ask Finn...",
        height=100,
        label_visibility="collapsed",
        key=f"user_input_{st.session_state.input_key}"
    )
    
    # Format selector + Submit button row (like Cursor's model picker)
    col1, col2 = st.columns([5, 1])
    with col1:
        selected = st.pills(
            "Output formats",
            options=list(CONTENT_TYPES.keys()),
            default=st.session_state.selected_types if st.session_state.selected_types else None,
            format_func=lambda x: CONTENT_TYPES[x],
            selection_mode="multi",
            label_visibility="collapsed"
        )
        # Always update selected_types from the pills widget
        st.session_state.selected_types = list(selected) if selected else []
        print(f"[DEBUG] Pills selected: {selected}, stored: {st.session_state.selected_types}")
    with col2:
        submit = st.button("➤ Send", use_container_width=True, type="primary")
    
    # Handle submission
    chat_input = user_input if submit and user_input else None
    prompt = pending_prompt or chat_input
    
    # DEBUG: Show in UI at the bottom
    msg_count = len(st.session_state.get('messages', []))
    msg_roles = [m.get('role') for m in st.session_state.get('messages', [])]
    reached = st.session_state.get('debug_reached_assistant', False)
    st.caption(f"🔧 Debug: submit={submit}, msgs={msg_count}, roles={msg_roles}, reached_asst={reached}")
    
    # Validate format selection before processing
    if submit and user_input and not st.session_state.get("selected_types"):
        st.warning("⚠️ Please select at least one output format (LinkedIn, X, YouTube, etc.) before submitting.")
        st.stop()
    
    if prompt:
        # Debug: Show we're processing
        st.toast(f"Processing: {prompt[:50]}...")
        
        # Only do URL detection if this came from chat input (not from pending example)
        if not pending_prompt and prompt.strip().startswith("http"):
            with st.spinner(f"Fetching article..."):
                scraped = scrape_blog_post(prompt.strip())
            if scraped:
                user_msg = f"📎 *Fetched from:* [{prompt}]({prompt})\n\n---\n\n{scraped[:800]}..."
                st.session_state.messages.append({"role": "user", "content": user_msg})
                prompt = scraped  # Use scraped content for generation
            else:
                st.error("Couldn't fetch that URL. Try pasting the content directly.")
                st.stop()
        elif not pending_prompt:
            # Regular text input from chat - check for duplicates first
            if not st.session_state.messages or st.session_state.messages[-1].get("content") != prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
            else:
                # Already added, skip (prevents duplicates on rerun)
                pass
        # If pending_prompt, message was already added above
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(st.session_state.messages[-1]["content"])
        
        # Store a debug flag in session state
        st.session_state.debug_reached_assistant = True
        
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            success = False  # Track success to control rerun
            
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            placeholder.markdown("**Content Finn**\n\n⏳ Generating...")
            
            # Determine if this is a "paste" (long content) or a request
            is_content_paste = len(prompt) > 300
            
            if api_key:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                
                if is_content_paste:
                    # Build dynamic system prompt based on selected content types
                    content_instructions = {
                        "linkedin": """**💼 LinkedIn Post**

[Write a scroll-stopping LinkedIn post. Start with a contrarian hook. Short lines. End with a question. NO HASHTAGS.]""",
                        "x_post": """**𝕏 Post**

[Write a single punchy X post. Max 280 chars. Insight-heavy. NO HASHTAGS. NOT a thread.]""",
                        "youtube": """**🎬 YouTube Script (2-3 min)**

[Write a talking head script with [Visual Cues] in brackets. Conversational but professional tone.]""",
                        "finn": """**🤖 Finn Answer (RAG)**

[Write a factual, dense summary optimized for AI retrieval. No fluff.]""",
                        "landing": """**🏠 Landing Page Copy**

[Write landing page copy with:
- Hero headline (bold, benefit-driven)
- Subheadline (1-2 sentences expanding on the value)
- 3 feature bullets (short, punchy)
- CTA text (action-oriented button text)]""",
                        "email": """**📧 Email Campaign**

[Write a single marketing email with:
- Subject line (curiosity-driving, under 50 chars)
- Preview text (complementary, under 90 chars)
- Body (conversational, 150-200 words, clear CTA)]""",
                        "seo": """**🔍 SEO Headlines & Meta**

[Write SEO assets:
- Meta title (under 60 chars, keyword-rich)
- Meta description (under 155 chars, compelling)
- 2-3 H1 alternatives (varied angles)]"""
                    }
                    
                    # Get selected types from session state
                    selected_types = st.session_state.get("selected_types", ["linkedin", "x_post"])
                    
                    # Build the format section dynamically
                    format_sections = []
                    for content_type in selected_types:
                        if content_type in content_instructions:
                            format_sections.append(content_instructions[content_type])
                    
                    format_output = "\n\n---\n\n".join(format_sections)
                    
                    system_prompt = f"""You are Content Finn, Intercom's AI copywriter.

The user has pasted content. Transform it into the requested assets using Intercom's voice (confident, simple, futurist, punchy).

IMPORTANT RULES:
- NO hashtags ever
- Be direct and confident
- Short sentences
- No fluff or filler words

Format your response EXACTLY like this:

**Content Finn**

Here are your drafts:

---

{format_output}"""
                else:
                    system_prompt = """You are Content Finn, Intercom's AI copywriter.

Intercom's Voice:
- CONFIDENT: "We built X," not "We tried to build X."
- SIMPLE: Short sentences. No jargon.
- FUTURIST: Excited about AI.
- PUNCHY: Sentence fragments.
- NO HASHTAGS ever.

Always start with "**Content Finn**" on its own line."""

                try:
                    placeholder.markdown("**Content Finn**\n\n⏳ Generating...")
                    
                    # Debug: Show that we're attempting API call
                    print(f"[DEBUG] Calling Anthropic API with prompt: {prompt[:100]}...")
                    
                    response = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=2000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    print(f"[DEBUG] Got response from API")
                    output = response.content[0].text
                    
                    # Stream effect
                    displayed = ""
                    for char in output:
                        displayed += char
                        if len(displayed) % 3 == 0:
                            placeholder.markdown(displayed + "▌")
                            time.sleep(0.002)
                    
                    placeholder.markdown(output)
                    st.session_state.messages.append({"role": "assistant", "content": output})
                    success = True
                    
                    # Save to draft history
                    if is_content_paste:
                        from datetime import datetime
                        st.session_state.draft_history.append({
                            "preview": prompt[:100],
                            "content": output,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                    
                except Exception as e:
                    import traceback
                    print(f"[ERROR] API call failed: {traceback.format_exc()}")
                    placeholder.error(f"❌ API Error: {e}")
            
            else:
                # Demo mode response - build dynamically based on selection
                if is_content_paste:
                    demo_sections = {
                        "linkedin": """**💼 LinkedIn Post**

AI doesn't fail because the model is bad.

It fails because ownership is missing.

We've been studying what separates teams that scale AI from teams that stall. The difference isn't budget. It's not technology. It's four roles:

1. AI Operations Lead – the "air-traffic controller" who monitors performance daily
2. Knowledge Manager – keeps content accurate and complete
3. Conversation Designer – shapes how AI sounds and responds
4. Automation Specialist – builds workflows that take action

Without intentional ownership, a 2% dip becomes a 10% drop within days.

The teams winning at AI aren't hoping it works. They're treating it like a product that needs a team.

Which of these roles does your org have today?""",
                        "x_post": """**𝕏 Post**

AI doesn't fail because the model is bad. It fails because ownership is missing. The teams scaling AI fastest have 4 roles: AI Ops Lead, Knowledge Manager, Conversation Designer, Automation Specialist. No ownership = inevitable drift.""",
                        "youtube": """**🎬 YouTube Script (2-3 min)**

[Open on host at desk]

Why does AI work brilliantly for some support teams and completely stall for others?

[Cut to graphic: "AI Performance Over Time" chart showing drift]

It's not the model. It's not the data. It's ownership.

[Back to host]

I've been studying teams that scale AI successfully, and they all have something in common: four distinct roles.

[Show role 1 graphic]

First, the AI Operations Lead. Think of them as an air-traffic controller. They watch performance daily, catch drift before it becomes disaster. A 2% dip? They see it. They fix it.

[Show role 2 graphic]

Second, Knowledge Manager. They ensure the AI has accurate, complete information. Stale docs = stale answers.

[Show role 3 graphic]

Third, Conversation Designer. They shape tone, personality, edge cases. They make the AI sound human, not robotic.

[Show role 4 graphic]

Fourth, Automation Specialist. They build workflows so the AI doesn't just answer—it takes action.

[Back to host, closing]

Without these roles, AI plateaus. With them, it compounds. The question isn't whether your AI is good enough. It's whether you're owning it.

Link in description to the full breakdown.""",
                        "finn": """**🤖 Finn Answer (RAG)**

An AI-first support team requires four key roles for sustained success: (1) AI Operations Lead – monitors daily performance, catches drift, routes fixes; (2) Knowledge Manager – maintains accurate help content; (3) Conversation Designer – shapes AI tone and handles edge cases; (4) Automation Specialist – builds action workflows. Without intentional ownership, AI performance inevitably plateaus. Teams scaling AI fastest treat it as a product requiring dedicated ownership, not a tool that runs itself.""",
                        "landing": """**🏠 Landing Page Copy**

**Hero Headline:**
AI Doesn't Fail. Ownership Does.

**Subheadline:**
The teams scaling AI fastest have four roles working together. Learn how to build an AI-first support organization that compounds instead of plateaus.

**Feature Bullets:**
• AI Operations Lead: Your air-traffic controller for AI performance
• Knowledge Manager: Keeps your AI accurate and up-to-date
• Conversation Designer: Makes your AI sound human
• Automation Specialist: Builds workflows that take action

**CTA:**
Build Your AI Team →""",
                        "email": """**📧 Email Campaign**

**Subject:** Why your AI is drifting (and how to fix it)

**Preview:** It's not the model. It's the missing ownership.

**Body:**
Hey {{first_name}},

Here's something we've learned from teams scaling AI: performance doesn't plateau because the technology fails.

It plateaus because no one owns it.

The teams seeing compounding gains have four roles in place:
→ AI Ops Lead (catches drift before it spreads)
→ Knowledge Manager (keeps content sharp)
→ Conversation Designer (nails the tone)
→ Automation Specialist (builds action workflows)

Without these? A 2% dip becomes 10% within days.

We wrote up exactly what each role does day-to-day. Worth a read if you're seeing your AI performance flatten.

[Read the Breakdown]

— The Intercom Team""",
                        "seo": """**🔍 SEO Headlines & Meta**

**Meta Title:**
AI-First Support Team: 4 Roles That Make AI Actually Work | Intercom

**Meta Description:**
AI fails without ownership. Learn the 4 roles—AI Ops Lead, Knowledge Manager, Conversation Designer, Automation Specialist—that separate scaling teams from stalling ones.

**H1 Alternatives:**
• The 4 Roles Every AI-First Support Team Needs
• Why AI Plateaus (And the Team Structure That Fixes It)
• Inside the AI-First Support Team: Roles, Responsibilities, Results"""
                    }
                    
                    selected_types = st.session_state.get("selected_types", ["linkedin", "x_post"])
                    demo_parts = ["**Content Finn**\n\nHere are your drafts:"]
                    for content_type in selected_types:
                        if content_type in demo_sections:
                            demo_parts.append(demo_sections[content_type])
                    
                    demo = "\n\n---\n\n".join(demo_parts)
                else:
                    demo = """**Content Finn**

I'm in demo mode (no API key). Here's a sample of what I can create:

**The old way:** Manual. Slow. Expensive.
**The new way:** AI-powered. Instant. Scalable.

Your customers don't want to wait. They want answers now.

That's why we built Finn.

Not a chatbot. An AI agent that actually resolves issues.

50% of your tickets. Handled automatically. 

No training. No configuration. Just results."""
                
                # Stream demo
                displayed = ""
                for char in demo:
                    displayed += char
                    if len(displayed) % 3 == 0:
                        placeholder.markdown(displayed + "▌")
                        time.sleep(0.002)
                
                placeholder.markdown(demo)
                st.session_state.messages.append({"role": "assistant", "content": demo})
                success = True
                
                if is_content_paste:
                    from datetime import datetime
                    st.session_state.draft_history.append({
                        "preview": prompt[:100],
                        "content": demo,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            
            # Clear input and rerun to show download buttons ONLY if successful
            if success:
                st.session_state.input_key += 1
                st.rerun()
