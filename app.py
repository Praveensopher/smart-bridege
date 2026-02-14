import os
import textwrap
from dataclasses import dataclass
from typing import Any, Dict

from dotenv import load_dotenv
import requests
from flask import Flask, render_template, request, jsonify


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# Load variables from a local .env file if present (GROQ_API_KEY, etc.)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_ID = "llama-3.3-70b-versatile"


def get_groq_headers() -> Dict[str, str]:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "Missing GROQ_API_KEY environment variable. "
            "Set it before starting the Flask app."
        )
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }


def call_groq(prompt: str, max_tokens: int = 1200) -> str:
    """
    Call Groq's chat completions API with the given prompt and return the text.
    """
    payload: Dict[str, Any] = {
        "model": GROQ_MODEL_ID,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are MarketAI Suite, an expert sales and marketing assistant. "
                    "You generate highly structured, actionable, and concise outputs."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=get_groq_headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Bubble up a readable error message to the UI
        raise RuntimeError(f"Groq API error: {exc}") from exc

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected Groq API response format: {data}") from exc


# -----------------------------------------------------------------------------
# Domain prompts
# -----------------------------------------------------------------------------


def build_campaign_prompt(form: Dict[str, str]) -> str:
    platform = form.get("platform") or "LinkedIn"
    
    # Platform-specific guidance
    platform_guidance = {
        "LinkedIn": "Professional B2B platform. Use industry insights, thought leadership, and value-driven content. Character limits: 3000 chars for posts, 150 chars for headlines.",
        "Facebook": "Visual and community-focused. Use engaging visuals, storytelling, and interactive content. Character limits: 5000 chars for posts, 40 chars for headlines.",
        "Instagram": "Highly visual platform. Focus on aesthetics, stories, reels, and carousel posts. Use hashtags (5-10). Character limits: 2200 chars for captions, 150 chars for bio.",
        "Twitter/X": "Concise and real-time. Use threads for longer content, trending topics, and quick engagement. Character limits: 280 chars per tweet, use threads for longer content.",
        "Email Marketing": "Direct and personalized. Focus on subject lines, clear value propositions, and strong CTAs. Use segmentation and personalization. Subject lines: 50-60 chars.",
        "YouTube": "Video-first platform. Focus on titles, descriptions, thumbnails, and engagement hooks. Titles: 60 chars max, descriptions: up to 5000 chars.",
        "TikTok": "Short-form video, trending sounds, and authentic content. Focus on hooks in first 3 seconds, trending hashtags, and entertainment value. Videos: 15-60 seconds.",
        "Google Ads": "Search intent-focused. Focus on keywords, ad copy variations, and conversion-optimized CTAs. Headlines: 30 chars, descriptions: 90 chars.",
        "Pinterest": "Visual discovery platform. Focus on high-quality images, keyword-rich descriptions, and seasonal trends. Descriptions: up to 500 chars.",
        "Snapchat": "Ephemeral and mobile-first. Focus on short videos, filters, and authentic behind-the-scenes content. Videos: up to 60 seconds.",
    }
    
    platform_specific = platform_guidance.get(platform, "Follow best practices for the selected platform.")
    
    return textwrap.dedent(
        f"""
        You are generating a comprehensive, platform-optimized marketing campaign for {platform}.

        Product details:
        - Name: {form.get("product_name") or "N/A"}
        - Description: {form.get("product_description") or "N/A"}
        - Target audience: {form.get("target_audience") or "Small business owners"}
        - Primary platform: {platform}
        - Campaign objective: {form.get("objective") or "Lead generation"}
        - Tone and style: {form.get("tone") or "Professional, value-focused"}

        Platform-specific guidance: {platform_specific}

        Output a comprehensive, structured campaign plan with the following sections:
        
        1. Campaign Objectives
           - 2-3 specific, measurable objectives aligned with {platform} best practices
        
        2. Platform-Specific Strategy
           - Key insights about {platform} audience behavior
           - Optimal posting times and frequency recommendations
           - Content format recommendations (e.g., video, carousel, single image, text)
           - Platform-specific best practices and character limits
        
        3. Audience Insight Summary
           - Deep dive into target audience behavior on {platform}
           - What content resonates on this platform
           - Engagement patterns and preferences
        
        4. 5 Targeted Content Ideas
           - Each idea should include:
             * Title/Headline
             * Content format (post, video, carousel, story, etc.)
             * 2-3 line description
             * Suggested hashtags or keywords (if applicable)
             * Why it works for {platform}
        
        5. 3 Variations of Compelling Ad Copy
           - Each variation should be optimized for {platform}:
             * Attention-grabbing hook/headline (respect platform character limits)
             * 2-4 sentence body (platform-appropriate length)
             * Clear, action-oriented CTA
             * Note any visual recommendations (images, videos, etc.)
        
        6. Recommended Calls To Action
           - 3-5 platform-specific CTAs
           - Explain why each CTA works well on {platform}
        
        7. Content Calendar Suggestions
           - Recommended posting frequency
           - Best days/times for {platform}
           - Content mix recommendations
        
        8. Performance Metrics to Track
           - Key KPIs specific to {platform}
           - What success looks like for this campaign

        Use Markdown headings (##, ###) and bullet lists. Be comprehensive, specific, and platform-optimized. 
        Ensure all content respects {platform}'s character limits, format requirements, and best practices.
        """
    ).strip()


def build_pitch_prompt(form: Dict[str, str]) -> str:
    return textwrap.dedent(
        f"""
        You are generating an enterprise B2B sales pitch.

        Context:
        - Solution: {form.get("solution_name") or "B2B enterprise software solution"}
        - Prospect role: {form.get("prospect_role") or "IT Director at a Fortune 500 company"}
        - Prospect company: {form.get("company_name") or "Fortune 500 enterprise"}
        - Key pain points: {form.get("pain_points") or "Legacy systems, security, scalability, cost"}
        - Desired outcome: {form.get("desired_outcome") or "Move to next evaluation stage"}

        Output a structured sales pitch with these sections:
        1. 30-Second Elevator Pitch (3–5 sentences, conversational)
        2. Clear Value Proposition (3–5 bullet points)
        3. Key Differentiators (3–5 bullets addressing enterprise pain points)
        4. Risk & Objection Handling (2–3 common objections with concise responses)
        5. Strategic Call To Action
           - 1–2 suggested next steps tailored to an enterprise IT Director.

        Use Markdown headings and bullets. Keep it crisp, outcome-focused, and executive-ready.
        """
    ).strip()


def build_lead_scoring_prompt(form: Dict[str, str]) -> str:
    return textwrap.dedent(
        f"""
        You are an expert sales operations analyst performing B2B lead qualification and scoring.

        Lead attributes:
        - Lead name: {form.get("lead_name") or "Not specified"}
        - Budget: {form.get("budget") or "$50,000"}
        - Urgency: {form.get("urgency") or "High"}
        - Timeline: {form.get("timeline") or "Immediate implementation"}
        - Company size: {form.get("company_size") or "Mid-market / Enterprise"}
        - Industry: {form.get("industry") or "Technology / SaaS"}
        - Decision-maker role: {form.get("decision_role") or "Director or above"}
        - Use case summary: {form.get("use_case") or "Digital transformation project"}

        Task:
        - Analyze the lead using a structured BANT / MEDDIC-style approach.
        - Output a quantified lead score from 0 to 100.
        - Provide probability of conversion as a percentage.

        Output format (Markdown):
        1. Lead Score Summary
           - Score: X/100
           - Probability of conversion: Y%
        2. Qualification Breakdown
           - Budget:
           - Authority:
           - Need:
           - Timing:
           - Fit / Ideal Customer Profile:
        3. Detailed Reasoning
           - Short paragraphs explaining the score and probability.
        4. Recommended Next Actions
           - 3–5 concrete follow-up steps for the sales team.

        Be precise and evidence-based based on the given inputs.
        """
    ).strip()


# -----------------------------------------------------------------------------
# Flask app
# -----------------------------------------------------------------------------


app = Flask(__name__)


@dataclass
class AIResult:
    title: str
    raw_markdown: str


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.route("/api/campaign", methods=["POST"])
def api_campaign():
    try:
        prompt = build_campaign_prompt(request.form)
        content = call_groq(prompt)
        return jsonify({"ok": True, "content": content})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/api/pitch", methods=["POST"])
def api_pitch():
    try:
        prompt = build_pitch_prompt(request.form)
        content = call_groq(prompt)
        return jsonify({"ok": True, "content": content})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/api/lead-score", methods=["POST"])
def api_lead_score():
    try:
        prompt = build_lead_scoring_prompt(request.form)
        content = call_groq(prompt)
        return jsonify({"ok": True, "content": content})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    """
    Lightweight health check endpoint to verify the Flask app is running.
    This does NOT call Groq.
    """
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug)

