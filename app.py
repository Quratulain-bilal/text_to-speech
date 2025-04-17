
import streamlit as st
from gtts import gTTS
from io import BytesIO

# Streamlit App
st.set_page_config(page_title="Text to Speech Robot", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; padding: 20px; }
    .title { font-size: 3em; color: #1f77b4; text-align: center; font-weight: bold; }
    .subheader { font-size: 1.5em; color: #555; text-align: center; }
    .robot-image { display: block; margin-left: auto; margin-right: auto; width: 200px; }
    .stButton>button { background-color: #1f77b4; color: white; border-radius: 10px; padding: 10px 20px; }
    .stSlider>div>div { color: #1f77b4; }
    </style>
""", unsafe_allow_html=True)

# Title and Image
st.markdown('<div class="title">Text to Speech Robot 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Powered by Google TTS</div>', unsafe_allow_html=True)
st.markdown('<img src="https://img.icons8.com/fluency/200/000000/robot.png" class="robot-image">', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input Text")
    input_method = st.radio("Input method:", ("Type Text", "Upload File"))
    
    if input_method == "Type Text":
        text_input = st.text_area("Enter text:", height=150, placeholder="Type something to convert to speech...")
    else:
        uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
        text_input = ""
        if uploaded_file:
            text_input = uploaded_file.read().decode("utf-8")
            st.text_area("Uploaded text:", value=text_input, height=150, disabled=True)

with col2:
    st.subheader("Speech Settings")
    language = st.selectbox("Language:", ["en", "es", "fr", "de", "hi", "ar"])
    speed = st.slider("Speed:", 0.5, 2.0, 1.0, 0.1)

# Convert Button
if st.button("Convert to Speech"):
    if not text_input.strip():
        st.error("Please provide some text to convert!")
    else:
        with st.spinner("Generating speech..."):
            tts = gTTS(text=text_input, lang=language, slow=False)
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            st.success("Speech generated successfully!")
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download Audio",
                data=audio_bytes.getvalue(),
                file_name="output.mp3",
                mime="audio/mp3"
            )

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #555;">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)
