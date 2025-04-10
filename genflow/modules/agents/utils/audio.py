import openai
import os
import pygame

def text_to_speech_openai(text, output_path="genflow/outputs/summary_audio.mp3", voice="ash", model="tts-1"):
    response = openai.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(output_path)
    return output_path

def speech_to_text_openai(audio_path, model="whisper-1"):
    audio_file = open(audio_path, "rb")
    transcript = openai.audio.transcriptions.create(
        model=model,
        file=audio_file,
    )
    return transcript.text

def record_audio_from_microphone(output_path = "genflow/inputs/recorder_input.wav", duration = 10):
    import pyaudio
    import wave

    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    record_seconds = duration

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels,
                    rate=rate, input=True,
                    frames_per_buffer=chunk)

    print("[Mic] Recording...")
    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    print("[Mic] Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return output_path

def play_audio_file(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  
        pygame.time.Clock().tick(10)


