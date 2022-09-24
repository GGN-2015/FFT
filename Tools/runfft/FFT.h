#ifndef __FFT_H__
#define __FFT_H__

#include <complex>
typedef std::complex<double> Complex;

/* solve fft for Arr, and store it back to Arr. */
#define  DFT_MODE ( 1)
#define IDFT_MODE (-1)
void fft(Complex* Arr, int n, int MODE);

#endif

