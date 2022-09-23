#!/bin/bash

if [ "$1" = "" ] ; then
    echo -e "[auto.Error] Usage $0 \<ID\> "
    exit 0
fi

if [ ! -f "./Data/WAV/$1.wav" ] ; then
    echo -e "[auto] Generating $1.wav ... "
    python3 ./Tools/Mp3Wav.py ./Data/MP3/$1.mp3 ./Data/WAV/$1.wav
else
    echo -e "[auto] $1.wav Found ..."
fi

echo -e "[auto] Generating $1.txt ... "
python3 ./Tools/WavReader.py ./Data/WAV/$1.wav 16384 > ./Data/TXT/$1.txt

echo -e "[auto] Generating $1.fft ... "
./Tools/runfft/cut2packet ./Data/TXT/$1.txt 16384
mv ./Data/TMP/TMP.fft ./Data/FFT/$1.fft

echo -e "[auto] Generating $1.png ... "
python3 ./Tools/HeatMap.py ./Data/FFT/$1.fft 1024
mv ./Data/TMP/TMP.png ./Data/PIC/$1.png

echo -e "[auto] Done."

