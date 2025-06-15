import os
import subprocess
import platform
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Voice settings for therapist persona
VOICE_SETTINGS = {
    "en": {"voice_id": "21m00Tcm4TlvDq8ikWAM", "model_id": "eleven_v3"},  # Rachhel (caring tone)
    "hi": {"voice_id": "AZnzlk1XvdvUeBnXmlld", "model_id": "eleven_v3"},  # domi
    "ta": {"voice_id": "AZnzlk1XvdvUeBnXmlld", "model_id": "eleven_v3"},  # 
    "te": {"voice_id": "AZnzlk1XvdvUeBnXmlld", "model_id": "eleven_v3"},  #
    "ml": {"voice_id": "AZnzlk1XvdvUeBnXmlld", "model_id": "eleven_v3"},  # 
    "bn": {"voice_id": "AZnzlk1XvdvUeBnXmlld", "model_id": "eleven_v3"}   # 
}

def text_to_speech_with_elevenlabs(input_text, output_filepath, language="en"):
    """Fixed TTS function using correct ElevenLabs API"""
    if not ELEVENLABS_API_KEY:
        raise ValueError("ElevenLabs API key not found")
    
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        voice_settings = VOICE_SETTINGS.get(language, VOICE_SETTINGS["en"])
        
        audio = client.generate(
            text=input_text,
            voice=voice_settings["voice_id"],
            model=voice_settings["model_id"],
            voice_settings={
                "stability": 0.4,
                "similarity_boost": 0.8
            }
        )
        
        with open(output_filepath, "wb") as f:
            f.write(audio)
        
        play_audio(output_filepath)
        return output_filepath
        
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return None

def play_audio(filepath):
    """Cross-platform audio playback"""
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":
            subprocess.run(['start', filepath], shell=True)
        elif os_name == "Linux":
            subprocess.run(['aplay', filepath])
    except Exception as e:
        print(f"Playback Error: {str(e)}")