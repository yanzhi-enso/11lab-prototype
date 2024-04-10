# 11 labs prototype
This repo contains a prototype using 11 labs voice generation tech with llm

## scripts
- llm.py openAI basic class for generating text
- 11labs client:
  - streaming.py 11labs client in streaming mode
  - async_player.py 11labs cient in async mode
  Both of them export a class `ElevenLabsWrapper` so that the upper layer can switch between them seamlessly
  - generate_all_sounds: return a list of ids for the voices provided by 11 labs by default
- main.py a small chatting app that integrates openAI with 11labs

To quickly test differnet models, paramerters, use `audios/generate_audios.py`. it will scan a parameter grid to generate audio files across different voice_ids, voice_settings (stability and similarity) and model types.
