#!/bin/bash

LINE_WIDTH=16384
CUT_WIDTH=1024

if [ "$1" = "" ] ; then
    echo -e "[auto.Error] Usage $0 \<ID\>"
    exit 0
fi

# --jmp means to jump WAV, TXT, FFT
if [ "$2" != "--jmp" ] ; then
    if [ ! -f "./Data/WAV/$1.wav" ] ; then
        echo -e "[auto] Generating $1.wav ... "
        python3 ./Tools/Mp3Wav.py ./Data/MP3/$1.mp3 ./Data/WAV/$1.wav
    else
        echo -e "[auto] $1.wav Found ..."
    fi

    # echo -e "[auto] Generating $1.wav ... "
    # python3 ./Tools/Mp3Wav.py ./Data/MP3/$1.mp3 ./Data/WAV/$1.wav

    echo -e "[auto] Generating $1.txt ... "
    python3 ./Tools/WavReader.py ./Data/WAV/$1.wav ${LINE_WIDTH} > ./Data/TXT/$1.txt

    echo -e "[auto] Generating $1.fft ... "
    ./Tools/runfft/cut2packet ./Data/TXT/$1.txt ${LINE_WIDTH}
    mv ./Data/TMP/TMP.fft ./Data/FFT/$1.fft
else
    echo -e "[auto] Jump Generating: WAV, TXT, FFT ..."
fi

echo -e "[auto] Generating $1.png ... "
if [ ! -f "./Data/MAN/$1.man" ] ; then
    echo -e "[auto]     Without Man file ..."
    python3 ./Tools/HeatMap.py ./Data/FFT/$1.fft ${CUT_WIDTH}
else
    echo -e "[auto]     With Man file ..."
    python3 ./Tools/HeatMap.py ./Data/FFT/$1.fft ./Data/MAN/$1.man\
        ${CUT_WIDTH}
fi
mv ./Data/TMP/TMP.png ./Data/PIC/$1.png

echo -e "[auto] Done."

