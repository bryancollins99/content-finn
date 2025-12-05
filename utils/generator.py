# =============================================================================
# Batch Generator - JSON Output Mode
# This module provides structured JSON output for programmatic use.
# The main app.py uses its own inline chat-style generation.
# =============================================================================

import json
import os
import anthropic
import config

def generate_campaign(text: str, api_key: str = None, demo_mode: bool = False) -> dict:
    """
    Generates the marketing campaign assets.
    If demo_mode is True, returns pre-canned data immediately.
    Otherwise, calls Anthropic API.
    """
    if demo_mode:
        return config.DEMO_RESPONSE

    if not api_key:
        raise ValueError("API Key is required for non-demo mode.")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        # Using Claude 3.5 Sonnet (latest available via API)
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            temperature=0.7,
            system=config.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the blog content to repurpose:\n\n{text}"
                }
            ]
        )

        # Extract JSON from the response
        content = message.content[0].text
        
        # Robust JSON extraction
        try:
            # First try direct parsing
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: Find first { and last }
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Last resort fallback if JSON is malformed
                return {
                    "linkedin": "Error parsing generated content.",
                    "twitter": "Error parsing generated content.", 
                    "tiktok": "Error parsing generated content.",
                    "fin": content # Return full text so user sees something
                }

    except anthropic.APIConnectionError as e:
        raise Exception("Connection error. Please check your internet connection.")
    except anthropic.AuthenticationError as e:
        raise Exception("Authentication failed. Please check your API Key.")
    except Exception as e:
        raise Exception(f"Generation failed: {str(e)}")
