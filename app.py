import streamlit as st
from io import BytesIO
from app.main import MusicLLM
from app.utils import *
from dotenv import load_dotenv
import numpy as np

load_dotenv()

# ---- Page Config ----
st.set_page_config(page_title="AI Music Composer 🎵", layout="wide", page_icon="🎹")

# ---- CSS Styling for Dark Mode & Gradients ----
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(90deg,#ff6a00,#ee0979);
        color: white;
        border-radius: 10px;
        height: 50px;
        width: 200px;
        font-size: 18px;
        font-weight: bold;
    }
    .stSlider>div>div>div>div {
        background: #ff6a00;
    }
    .stTextInput>div>input {
        background: #1f1f2e;
        color: #fff;
        border-radius: 8px;
        height: 40px;
    }
    .stSelectbox>div>div>div>div {
        background: #1f1f2e;
        color: #fff;
        border-radius: 8px;
        height: 40px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🎹 AI Music Composer")
st.markdown("Generate music with AI in your favorite style!")

# ---- Input Section ----
col1, col2 = st.columns([2, 1])
with col1:
    music_input = st.text_input("Describe your music (e.g., 'calm jazz with piano')")
with col2:
    style = st.selectbox("Select style", ["Sad", "Happy", "Jazz", "Romantic", "Extreme"])

# ---- Sliders for Advanced Controls ----
tempo = st.slider("Tempo (BPM)", 60, 200, 120)
mood = st.slider("Mood Intensity", 0, 10, 5)
volume = st.slider("Volume", 0, 100, 70)

# ---- Generate Music ----
if st.button("🎼 Generate Music") and music_input:
    generator = MusicLLM()
    with st.spinner("Generating music..."):
        # AI Melody, Harmony, Rhythm
        melody = generator.generate_melody(music_input)
        harmony = generator.generate_harmony(melody)
        rhythm = generator.generate_rythm(melody)
        composition = generator.adapt_style(style, melody, harmony, rhythm)

        # Convert notes to frequencies
        melody_freqs = note_to_frequencies(melody.split())
        harmony_notes = []
        for chord in harmony.split():
            harmony_notes.extend(chord.split('-'))
        harmony_freqs = note_to_frequencies(harmony_notes)

        all_freqs = melody_freqs + harmony_freqs
        wav_bytes = generate_wav_bytes_from_notes_freqs(all_freqs, tempo=tempo, volume=volume)

    # ---- Audio Player with Waveform ----
    st.audio(BytesIO(wav_bytes), format='audio/wav')
    st.success("Music generated successfully!")

    # Animated waveform placeholder (simple representation)
    st.markdown("### 🎵 Waveform Preview")
    waveform = np.sin(2 * np.pi * np.arange(len(all_freqs) * 100) * 440 / 44100)
    st.line_chart(waveform[:5000])  # partial waveform for visualization

    # ---- Composition Summary ----
    with st.expander("Composition Summary"):
        st.text(composition)
