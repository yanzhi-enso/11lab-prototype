import os
from elevenlabs import VoiceSettings, Voice, save
from elevenlabs.client import ElevenLabs

import logging

logger = logging.getLogger('elevenlabs')

speaker = {
    'Adam_M': 'pNInz6obpgDQGcFmaJgB',
    'Charlie_M': 'IKne3meq5aSn9XLyUdCD',
    'Rachel_F': '21m00Tcm4TlvDq8ikWAM',
    'Dorothy_F': 'ThT5KcBeYPX3keUQqHPh',
}

params = [
    {
        'stability': 0.5,
        'similarity': 0.8,
    },{
        'stability': 0.7,
        'similarity': 0.8,
    }
]

model_ids = [
    'eleven_monolingual_v1',
    'eleven_turbo_v2',
]

class ElevenLabsWrapper:
    def __init__(self):
        self.client = ElevenLabs(
            api_key=os.environ.get('ELEVENTLABS_API_KEY')
        )

    def get_all_voices(self):
        response = self.client.voices.get_all()
        print(response)
        return response

    def play(self, text_stream, voice_name, voice_key, stability, similarity, model_id):
        voice = Voice(
            voice_id=voice_key,
            settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity,
            )
        )
        audio = self.client.generate(
            text=text_stream,
            model='eleven_monolingual_v1',
            voice=voice,
        )

        base_name = f'{voice_name}_{stability}_{similarity}'
        if model_id == 'eleven_turbo_v2':
            base_name += "_turbo"

        save(audio, base_name + '.mp3')


input = "Living with Mamba in a studio apartment must've been quite an experience, especially while navigating the challenges of potty training and such. It shows how much you've adapted and learned together. Reflecting on those early days with her, what do you think were the most important lessons you learned from raising Mamba during that time?"
player = ElevenLabsWrapper()

for param in params:
    for model_id in model_ids:
        for name, key in speaker.items():
            player.play(
                input,
                name,
                key,
                param['stability'],
                param['similarity'],
                model_id,
            )
