import os
import time
import requests
# from player import play
from elevenlabs import play

url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
api_key = os.getenv("ELEVENTLABS_API_KEY")

msgs = [
    "Living with Mamba in a studio apartment must've been quite an experience, especially while navigating the challenges of potty training and such.",
    "It shows how much you've adapted and learned together.",
    "Reflecting on those early days with her, what do you think were the most important lessons you learned from raising Mamba during that time?"
]

def text2audio(msg, use_turbo=False):
    if use_turbo:
        # smaller model, close to polly
        model_id = "eleven_turbo_v2"
    else:
        # larger model, better performance
        model_id = "eleven_monolingual_v1"
    payload = {
        "text": msg,
        "model_id": model_id, 
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8,
            "use_speaker_boost": False
        },
        "pronunciation_dictionary_locators": []
    }
    headers = {
        "Content-Type": "application/json",
        'xi-api-key': api_key,
    }

    start = time.perf_counter()
    response = requests.request("POST", url, json=payload, headers=headers)
    end = time.perf_counter()
    print("response status:", response.status_code)
    print("request time: ", (end-start))
    return response.content

if __name__ == "__main__":
    for msg in msgs:
        # data = text2audio(msg, use_turbo=True)
        data = text2audio(msg, use_turbo=False)

        play(data)
