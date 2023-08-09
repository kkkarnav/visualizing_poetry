# audio recording
import sounddevice as sd
from scipy.io.wavfile import write

# api 1
from huggingsound import SpeechRecognitionModel

# api 2
from diffusers import StableDiffusionPipeline
import torch

import os


def record_audio(time):
    frequency = 16000  # in KHz

    # creating the recording
    recording = sd.rec(int(time * frequency),
                       samplerate=frequency, channels=2)
    print("starting recording")
    sd.wait()
    print("finished recording")

    # writing the recording to .wav
    write("./static/iml.wav", frequency, recording)


def transcribe_audio():
    # initializing speech recognition model
    speech_recognition = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
    audio_paths = ["./static/iml.wav"]

    # transcribing the audio to text
    transcriptions = speech_recognition.transcribe(audio_paths)
    speech = (transcriptions[0]['transcription'])
    print(speech)

    # split into chunks to visualize
    words = speech.split(" ")
    chunk = 7
    lines = [words[i * 7:(i + 1) * 7] for i in range((len(words) + 7 - 1) // 7)]
    print(lines)

    return lines


def generate_image(lines):
    # installation check
    print(torch.cuda.is_available())

    # initializing image generation model
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    # clear previous output
    for file in os.listdir('static'):
        if file.endswith('.png'):
            os.remove('./static/'+file)

    # convert the text to an image file
    for index, line in enumerate(lines):
        line = " ".join(line)
        image = pipe(line).images[0]
        image.save("./static/output" + str(index) + ".png")


def main(length):
    record_audio(length)
    lines = transcribe_audio()
    generate_image(lines)
