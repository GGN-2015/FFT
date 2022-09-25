from pydub import AudioSegment

def mp3_to_wav(mp3_path, wav_path):
    song = AudioSegment.from_mp3(mp3_path).set_frame_rate(44100)
    song.export(wav_path, format="wav")

import sys

if len(sys.argv) != 3:
    sys.stderr.write("[Mp3Wav] Usage: python3 Mp3Wav.py <input.mp3> <output.wav>")
    exit()

if __name__ == '__main__':
    mp3_to_wav(sys.argv[1], sys.argv[2])
