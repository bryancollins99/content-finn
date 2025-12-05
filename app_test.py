import streamlit as st
import os
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

st.title("🧪 Content Finn Test Lab")

# API Key Check
api_key = os.environ.get("ANTHROPIC_API_KEY")
if api_key:
    st.success(f"✅ API Key found: {api_key[:10]}...")
else:
    st.error("❌ No API Key found in environment variables")

# Simple Input
prompt = st.text_area("Enter prompt:", "Write a short LinkedIn post about AI.")

if st.button("Generate"):
    if not api_key:
        st.error("Cannot generate without API key")
        st.stop()
        
    client = anthropic.Anthropic(api_key=api_key)
    
    with st.spinner("Calling Claude..."):
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            st.subheader("Response:")
            st.markdown(message.content[0].text)
            st.success("✅ Generation successful!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

