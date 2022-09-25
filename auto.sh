#!/bin/bash

LINE_WIDTH=16384
CUT_WIDTH=1024

if [ "$1" = "" ] ; then
    echo -e "[auto.Error] Usage $0 \<ID\>"
    exit 0
fi

NAME=`printf "%04d" $1`
echo -e "[auto] NAME = ${NAME}"

# --jmp means to jump WAV, TXT, FFT
if [ "$2" != "--jmp" ] ; then
    if [ ! -f "./Data/WAV/${NAME}.wav" ] ; then
        echo -e "[auto] Generating ${NAME}.wav ... "
        python3 ./Tools/Mp3Wav.py ./Data/MP3/${NAME}.mp3 ./Data/WAV/${NAME}.wav
    else
        echo -e "[auto] ${NAME}.wav Found ..."
    fi

    # echo -e "[auto] Generating $1.wav ... "
    # python3 ./Tools/Mp3Wav.py ./Data/MP3/$1.mp3 ./Data/WAV/$1.wav

    echo -e "[auto] Generating ${NAME}.txt ... "
    python3 ./Tools/WavReader.py ./Data/WAV/${NAME}.wav \
        ${LINE_WIDTH} > ./Data/TXT/${NAME}.txt

    echo -e "[auto] Generating ${NAME}.fft ... "
    ./Tools/runfft/cut2packet ./Data/TXT/${NAME}.txt ${LINE_WIDTH}
    mv ./Data/TMP/TMP.fft ./Data/FFT/${NAME}.fft
else
    echo -e "[auto] Jump Generating: WAV, TXT, FFT ..."
fi

echo -e "[auto] Generating ${NAME}.png ... "
if [ ! -f "./Data/MAN/${NAME}.man" ] ; then
    echo -e "[auto]     Without Man file ..."
    python3 ./Tools/HeatMap.py ./Data/FFT/${NAME}.fft ${CUT_WIDTH}
else
    echo -e "[auto]     With Man file ..."
    python3 ./Tools/HeatMap.py ./Data/FFT/${NAME}.fft ./Data/MAN/${NAME}.man\
        ${CUT_WIDTH}
fi
mv ./Data/TMP/TMP.png ./Data/PIC/${NAME}.png

echo -e "[auto] Done."

