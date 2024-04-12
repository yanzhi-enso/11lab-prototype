from pydub import AudioSegment
import pyaudio

def play(audio):
    # Play the audio
    chunk = 1024
    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(audio.sample_width),
        channels=audio.channels,
        rate=audio.frame_rate,
        output=True
    )

    # Play the audio in chunks
    for i in range(0, len(audio), chunk):
        stream.write(audio.raw_data[i:i+chunk])

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    audio = AudioSegment.from_file("audios/Adam_M_0.5_0.8_turbo.mp3", format='mp3')
    play(audio)