FFT.o: FFT.cpp
	g++ -c -o $@ $^


runfft.o: runfft.cpp
	g++ -c -o $@ $^


runfft: FFT.o runfft.o
	g++ -o $@ $^


# direct compile
cut2packet: cut2packet.cpp
	g++ -o $@ $^


clean:
	rm *.o


.PHONY: clean
