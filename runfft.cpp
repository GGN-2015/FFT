#include <cstdio>

#include "FFT.h"

Complex Arr[(int)1e6 + 10]; int ArrLen = 0;

int main() {
    /* input values from stdin. */
    double dtmp;
    while(scanf("%lf", &dtmp) != -1) {
        Arr[ArrLen ++] = dtmp;
    }
    fft(Arr, ArrLen, DFT_MODE);
    for(int i = 0; i < ArrLen; i += 1) {
        double x = Arr[i].real();
        double y = Arr[i].imag();
        double l = sqrt(x * x + y * y);
        printf("%lf ", l);
    }
    printf("\n");
    return 0;
}

