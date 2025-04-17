import streamlit as st
import pyttsx3
import os

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to get available voices with descriptive labels
def get_voices():
    voices = engine.getProperty('voices')
    voice_list = []
    for voice in voices:
        name = voice.name
        # Simple heuristic to categorize voices (customize based on your system voices)
        if "female" in name.lower() or "zira" in name.lower() or "samantha" in name.lower():
            label = f"{name} (Female)"
        elif "child" in name.lower() or "hazel" in name.lower():
            label = f"{name} (Child-like)"
        elif "male" in name.lower() or "david" in name.lower() or "ravi" in name.lower():
            label = f"{name} (Male)"
        elif "old" in name.lower() or "mark" in name.lower():
            label = f"{name} (Older Male)"
        else:
            label = f"{name} (Generic)"
        voice_list.append((label, voice.id))
    return voice_list

# Function to convert text to speech
def text_to_speech(text, voice_id, rate, volume):
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume / 100)
    audio_file = "output.mp3"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    return audio_file

# Function to read audio file
def get_audio_file(audio_file):
    with open(audio_file, "rb") as f:
        data = f.read()
    return data

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
st.markdown('<div class="subheader">Choose from many voice </div>', unsafe_allow_html=True)
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
    voices = get_voices()
    voice_names = [label for label, _ in voices]
    selected_voice = st.selectbox("Select Voice:", voice_names, help="Choose a voice like Bachi, Larka, or Old Man!")
    voice_id = next(id for label, id in voices if label == selected_voice)
    rate = st.slider("Speech Rate:", 100, 300, 200, help="Adjust how fast the voice speaks")
    volume = st.slider("Volume (%):", 0, 100, 100, help="Adjust loudness")

# Convert Button
if st.button("Convert to Speech"):
    if not text_input.strip():
        st.error("Please provide some text to convert!")
    else:
        with st.spinner("Generating speech..."):
            audio_file = text_to_speech(text_input, voice_id, rate, volume)
            st.success("Speech generated successfully!")
            audio_bytes = get_audio_file(audio_file)
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download Audio",
                data=audio_bytes,
                file_name="output.mp3",
                mime="audio/mp3"
            )

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #555;">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)