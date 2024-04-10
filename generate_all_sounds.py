import os
from elevenlabs import stream, VoiceSettings, Voice
from elevenlabs.client import ElevenLabs

import logging

logger = logging.getLogger('elevenlabs')

class ElevenLabsWrapper:
    def __init__(self):
        self.client = ElevenLabs(
            api_key=os.environ.get('ELEVENTLABS_API_KEY')
        )

    def get_all_voices(self):
        response = self.client.voices.get_all()
        for voice in response.voices:
            print("===============")
            print(voice.name, voice.labels)
        
        print("total voicces:", len(response.voices))

input = "Living with Mamba in a studio apartment must've been quite an experience, especially while navigating the challenges of potty training and such. It shows how much you've adapted and learned together. Reflecting on those early days with her, what do you think were the most important lessons you learned from raising Mamba during that time?"
player = ElevenLabsWrapper()
player.get_all_voices()
