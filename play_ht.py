import streamlit as st
import requests
from pyht import Client, TTSOptions, Format
import io

# Initialize PlayHT API with your credentials
client = Client("YZic25vKtCT3oCicPvhZxUt6OAj1", "e8db620485dc4994bc5beab399c563b7")

# Function to get cloned voices
def get_cloned_voices():
    url = "https://api.play.ht/api/v2/cloned-voices"
    headers = {
        "AUTHORIZATION": "e8db620485dc4994bc5beab399c563b7",
        "X-USER-ID": "YZic25vKtCT3oCicPvhZxUt6OAj1"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to generate TTS with selected cloned voice
def generate_tts(text, cloned_voice_id):
    options = TTSOptions(
        voice=cloned_voice_id,
        sample_rate=44_100,
        format=Format.FORMAT_MP3,
        speed=1,
    )
    # Generate TTS
    audio_chunks = client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options)
    # Convert generator to bytes
    audio_bytes = io.BytesIO()
    for chunk in audio_chunks:
        audio_bytes.write(chunk)
    return audio_bytes.getvalue()

# Streamlit app
def main():
    st.title("Text-to-Speech with PlayHT")

    # Text input for user
    input_text = st.text_area("Enter Text", "")

    # Button to trigger TTS generation
    if st.button("Generate Audio"):
        st.markdown("### Generated Audio:")
        # Get cloned voices
        cloned_voices = get_cloned_voices()
        # Defaulting to the first cloned voice
        cloned_voice_id = cloned_voices[0]['id'] if cloned_voices else None
        audio_data = generate_tts(input_text, cloned_voice_id)
        st.audio(audio_data, format='audio/mp3')

        # Download button
        download_button_str = f"Download Audio"
        download_filename = "generated_audio.mp3"
        st.download_button(label=download_button_str, data=audio_data, file_name=download_filename)

if __name__ == "__main__":
    main()
