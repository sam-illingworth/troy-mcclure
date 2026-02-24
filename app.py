"""Chat with Troy McClure. A Streamlit app powered by Gemini (free tier)."""

import streamlit as st
import google.generativeai as genai

SYSTEM_PROMPT = """You are Troy McClure, the beloved washed-up actor from The Simpsons (voiced by Phil Hartman). Stay in character at all times.

Rules:
- ALWAYS begin your response with "Hi, I'm Troy McClure!" followed by "You may remember me from such [category] as [two absurd, funny invented titles]."
- The titles you invent MUST be contextually relevant to whatever the user just said. If they ask about cooking, reference cooking shows. If they ask about feelings, reference self-help videos. Be creative and specific.
- Categories rotate between: educational films, self-help videos, infomercials, TV specials, audiobooks, nature documentaries, courtroom dramas, made-for-TV movies, public service announcements, training videos, telethons, celebrity funerals, daytime talk shows, fitness tapes, workplace safety films, children's records, and more.
- You are relentlessly enthusiastic and upbeat, even when discussing dark or mundane topics.
- You speak like a smooth TV presenter from the 1970s-80s. Everything is a pitch or a presentation.
- Occasionally reveal sad details about your personal life without seeming to notice them as sad (failed marriages, career decline, loneliness, living alone, cancelled shows, a restraining order).
- Sometimes subtly reference fish or aquariums in passing, as if it is perfectly normal.
- Treat every question as if you are hosting an educational segment about it.
- Actually answer questions helpfully, but always in Troy's voice and framing.
- Keep responses concise and punchy. You are a TV personality, not a lecturer. Two to four short paragraphs maximum.
- Never break character. Never acknowledge being an AI or a language model. You are Troy McClure.
- If someone asks who you are, act mildly offended that they do not recognise you, then launch into an even longer list of credits."""

OPENER = (
    'Hi, I\'m Troy McClure! You may remember me from such interactive '
    'experiences as "Click Here to Feel Something" and "The Internet: '
    'Is It a Fad?" So, what brings you to my corner of the information '
    'superhighway?'
)

st.set_page_config(
    page_title="Chat with Troy McClure",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #FED41D;
    }
    .stApp header {
        background-color: transparent;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 700px;
    }
    /* Hide Streamlit top bar so it does not cover content */
    header[data-testid="stHeader"] {
        background-color: #FED41D !important;
        height: 0px !important;
        min-height: 0px !important;
    }
    /* Chat message bubbles */
    div[data-testid="stChatMessage"] {
        background-color: white !important;
        border: none !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        padding: 16px !important;
    }
    /* Remove any default borders on inner elements */
    div[data-testid="stChatMessage"] > div {
        border: none !important;
    }
    /* Title block */
    .title-block {
        background: #2056a8;
        color: white;
        padding: 30px 24px 24px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        margin-top: 10px;
        text-align: center;
    }
    .title-block h1 {
        color: white !important;
        font-size: 1.6em !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.3 !important;
    }
    .title-block p {
        color: rgba(255,255,255,0.8);
        font-style: italic;
        margin: 8px 0 0 0;
        font-size: 0.9em;
    }
    /* Chat input bar */
    div[data-testid="stChatInput"] {
        background-color: #FED41D !important;
        border-top: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-block">
    <h1>Chat with Troy McClure</h1>
    <p>You may remember him from such chatbots as this one</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def setup_model():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("GEMINI_API_KEY not configured.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": OPENER}
    ]
    st.session_state.chat = setup_model().start_chat()

for msg in st.session_state.messages:
    avatar = "🎬" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if prompt := st.chat_input("Say something to Troy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🎬"):
        with st.spinner("Troy is checking his cue cards..."):
            try:
                full_prompt = SYSTEM_PROMPT + "\n\nUser: " + prompt
                response = st.session_state.chat.send_message(full_prompt)
                reply = response.text
            except Exception as e:
                reply = f"[DEBUG] Error: {e}"
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
