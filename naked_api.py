import io
from pydub import AudioSegment
import requests
from player import play

url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"

msg = "Living with Mamba in a studio apartment must've been quite an experience, especially while navigating the challenges of potty training and such. It shows how much you've adapted and learned together. Reflecting on those early days with her, what do you think were the most important lessons you learned from raising Mamba during that time?"
payload = {
    "text": msg,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.7,
        "similarity_boost": 0.8,
        "use_speaker_boost": False
    },
    "pronunciation_dictionary_locators": []
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

audio_seg = AudioSegment.from_file(
    io.BytesIO(response.content),
    format='mp3',
)

play(audio_seg)
