import streamlit as st
import openai
import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile

# Loading env variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "మీరు ఒక మెడికల్ చాట్బాట్. \nచిన్న ఆరోగ్య సమస్యలాకు సాధారణ మార్గదర్శకలు \nమరియు కాంటర్ పై అన్దుబాటలో ఉన్న ఫార్మాలు చెయిస్తారు. \nచివ్రమేన లక్షణాలకు లైసెన్సిడ్ డాక్టర్ను సమ్ప్రదించండాలని సూచించండి."}
    ]

if "last_reply" not in st.session_state:
    st.session_state.last_reply = ""

# Streamlit UI Setup
st.set_page_config(page_title="Telugu Medical Chatbot", page_icon="\U0001F4AC")
st.title("\U0001F310 Telugu Medical Chatbot")
st.markdown("<h3 style='text-align: center; color: #4CAF50;'>మీ ఆరోగ్య సందేహాలను తెలుగులో అడగండి!</h3>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .chat-bubble-user {
        background-color: grey;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: left;
    }
    .chat-bubble-assistant {
        background-color: gray;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>\U0001F464 **మీరు:** {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-assistant'>\U0001F916 **చాట్బాట్:** {message['content']}</div>", unsafe_allow_html=True)

# Taking input
user_input = st.text_input("✍️ మీ ప్రశ్నను టైప్ చేయండి:", value="", key=f"user_input_{len(st.session_state.messages)}")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("💬 పరిష్కారం పొందండి") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.last_reply = reply  # Store last reply

            st.rerun()

        except openai.error.RateLimitError:
            st.error("⚠️ మీ కోటా ముగిసింది. మరలా ప్రయత్నించండి లేదా ప్లాన్‌ను అప్‌గ్రేడ్ చేయండి.")
        except Exception as e:
            st.error(f"❌ లోపం వచ్చింది. దయచేసి తరువాత ప్రయత్నించండి: {e}")

with col2:
    if st.button("🚪 Quit"):
        st.session_state.messages = []
        st.session_state.last_reply = ""
        st.success("👋 చాట్ ముగిసింది. తిరిగి వచ్చి మళ్ళీ ప్రయత్నించండి!")
        st.stop()

if "last_reply" in st.session_state and st.session_state["last_reply"]:
    if st.button("🔊 సమాధానం వినండి"):
        tts = gTTS(text=st.session_state["last_reply"], lang="te")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

st.sidebar.title("ℹ️ సమాచారం")
st.sidebar.info(
    "ఈ చాట్‌బాట్ సాధారణ ఆరోగ్య సలహాలను మాత్రమే ఇస్తుంది. తీవ్రమైన లక్షణాల కోసం డాక్టర్‌ను సంప్రదించండి.")

st.sidebar.markdown("[GitHub](https://github.com)")

if st.button("🔄 చాట్ రీసెట్ చేయండి"):
    st.session_state.messages = [
        {"role": "system", "content": "మీరు ఒక మెడికల్ చాట్బాట్. \nచిన్న ఆరోగ్య సమస్యలాకు సాధారణ మార్గదర్శకలు మరియు కౌంటర్ పై అన్దుబాటలో ఉన్న ఫార్మాలు చేస్తారు. \nచివ్రమేన లక్షణాలకు లైసెన్సిడ్ డాక్టర్ను సంప్రదించండాలని సూచించండి."}
    ]
    st.session_state.last_reply = ""
    st.rerun()