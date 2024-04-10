import os
import asyncio
from elevenlabs import play, save, VoiceSettings, Voice
from elevenlabs.client import AsyncElevenLabs

import logging

logger = logging.getLogger('elevenlabs')

class ElevenLabsWrapper:
    def __init__(self, stability=0.5, similarity=0.8):
        self.client = AsyncElevenLabs(
            api_key=os.environ.get('ELEVENTLABS_API_KEY')
        )
        self.stability = stability
        self.similarity = similarity

    async def get_all_voices(self):
        response = self.client.voices.get_all()
        print(response)
        return response

    async def text2audio(self, text):
        voice=Voice(
            voice_id='EXAVITQu4vr4xnSDxMaL',
            settings=VoiceSettings(
                stability=self.stability,
                similarity_boost=self.similarity,
                style=0.0,
                use_speaker_boost=True
            )
        )
        results = await self.client.generate(
            text=text,
            # model='eleven_monolingual_v1',
            model='eleven_turbo_v2',
            voice=voice,
        )

        out = b''
        async for value in results:
            out += value
        
        return out
    
    def play(self, audio):
        play(audio)
    
    def save(self, audio, filename):
        save(audio, filename)

if __name__ == "__main__":
    input = "Living with Mamba in a studio apartment must've been quite an experience, especially while navigating the challenges of potty training and such. It shows how much you've adapted and learned together. Reflecting on those early days with her, what do you think were the most important lessons you learned from raising Mamba during that time?"
    player = ElevenLabsWrapper()
    b = asyncio.run(player.text2audio(input))
    play(b)