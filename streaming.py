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
        print(response)
        return response

    def play(self, text_stream):
        voice = Voice(
            voice_id='EXAVITQu4vr4xnSDxMaL',
            settings=VoiceSettings(
                stability=0.7,
                similarity_boost=0.8,
            )
        )
        audio_stream = self.client.generate(
            text=text_stream,
            model='eleven_monolingual_v1',
            voice=voice,
            stream=True
        )
        
        stream(audio_stream)

def input_text_stream(input):
    texts = input.split('.')
    for text in texts:
        yield text

input = "Living with Mamba in a studio apartment must've been quite an experience, especially while navigating the challenges of potty training and such. It shows how much you've adapted and learned together. Reflecting on those early days with her, what do you think were the most important lessons you learned from raising Mamba during that time?"
player = ElevenLabsWrapper()
player.play(input_text_stream(input))