import io
import asyncio
import time
from pydub import AudioSegment

from llm import GPTAgent
from async_player import ElevenLabsWrapper

async def translator(input_q, output_q, player):
    while True:
        sentence= await input_q.get()
        if sentence is None:
            output_q.put_nowait(None)
            return

        print(sentence, end='', flush=True)
        byts = await player.text2audio(sentence)
        output_q.put_nowait(byts)

async def main():
    agent = GPTAgent()
    agent.init()

    stability=0.5
    similarity=0.8

    player = ElevenLabsWrapper(
        stability=stability, similarity=similarity,
    )

    audio_queue = asyncio.Queue()
    try:
        turn = 0
        while True:
            user_input = input("You: ") 
            await agent.chat(user_input)
            print('Assistant: ', end='', flush=True)
            asyncio.create_task(
                translator(agent.sentence_queue, audio_queue, player)
            )

            folder_name = f'stability_{stability}_similarity_{similarity}'
            turn_audio_bucket = []
            while True:
                start = time.perf_counter()
                audio = await audio_queue.get()
                end = time.perf_counter()
                print("diff: ", (end-start))
                if audio is None:
                    break

                # aud_seg = AudioSegment.from_file(
                #     io.BytesIO(audio),
                #     format='mp3',
                # )
                # aud_seg.export(f'{folder_name}/turn_{turn}.mp3')
                turn_audio_bucket.append(audio)
                player.play(audio)
            turn += 1

            player.save(
                iter(turn_audio_bucket),
                f'{folder_name}/turn_{turn}.mp3'
            )
    except KeyboardInterrupt:
        print("Goodbye!")
    except EOFError:
        print("Goodbye!")

if __name__ == '__main__':
    asyncio.run(main())