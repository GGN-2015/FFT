#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cassert>

char filename[200];
FILE *fp, *wp;
int Endflag = 0;
int CNT = 1024;

const int N = 16384;
double numbers[N];

#define FFT_TMP_OUTPUT "./Data/TMP/TMP.fft"
#define CUT_TMP_OUTPUT "./Data/TMP/TMP.cut"
#define FFT_EXE_FILE   "./Tools/runfft/runfft"

void init(int argc, char* argv[]) {
    assert(argc <= 3);

    if(argc == 3) {

        /* int put filename from argv[1], LineWidth from argv[2]. */
        CNT = atoi(argv[2]);
        fp = fopen(argv[1], "r");
    } else if(argc == 2) {

        /* input file name from ARGV, Default LineWidth=1024. */
        fp = fopen(argv[1], "r");
    } else {

        /* input file name in CLI, Default LineWidth=1024. */
        fprintf(stdout, "[cut2packet] fileName >>>");
        fgets(filename, sizeof(filename), stdin);

        /* delete '\n' character. */
        for(int i = 0; ; i ++) {
            if(filename[i] == '\n') {
                filename[i] = '\0';
                break;
            }
        }
        fp = fopen(filename, "r");
    }

    /* CNT moust be 2^k and less or equal than N. */
    assert(CNT <= N);
}

int judge(char tmp) {

    /* available char in a content. */
    if(tmp >= '0' && tmp <= '9') return 0;
    if(tmp == ' ' || tmp == '.') return 0;
    if(tmp == '-') return 0;
    if(tmp == '\n' || tmp == '\r') return 0;

    /* reach the end of a file. */
    if(tmp == EOF) return 1;
    return 1;
}

int main(int argc, char* argv[]) {
    init(argc, argv);
    char ch;

	/* clean the content in file */
    fclose(fopen(FFT_TMP_OUTPUT, "w"));

	/* read in from the file. */
    int linecnt = 0;
    while((ch = fgetc(fp)) != EOF) {

		/* output the cut message into CUT_TMP_OUTPUT. */
        wp = fopen(CUT_TMP_OUTPUT, "w");
        int i = 0;

        for(; i < CNT; i++) {
            int pow = 10;
            int flag1 = 1;

			/* if reach the end of file, break. */
            if(judge(ch)) break;

			/* read in the number and save it to array numbers[i]. */
            numbers[i] = 0.0;
            while(ch < '0' || ch > '9') {
                if(judge(ch)) break;
                if(ch == '-') {
                    flag1 *= -1;
                }
                ch = fgetc(fp);
            }
            while(ch >= '0' && ch <= '9') {
                numbers[i] = numbers[i] * 10 + ch - '0';
                ch = fgetc(fp);
            }

/* if the input has decimal point. */
#ifdef DECIMAL_INPUT
            if(ch == '.') {
                ch = fgetc(fp);
                while(ch >= '0' && ch <= '9') {
                    numbers[i] = numbers[i] + (ch - '0') / pow;
                    pow *= 10;
                    ch = fgetc(fp);
                }
            }else {
                /* no decimal point. */
            }
#endif

            numbers[i] *= flag1;
            fprintf(wp, "%lf ", numbers[i]);

			/* reach the end of a file. */
            if(judge(ch)) break;
        }
        i++;
        //printf("%d\n", i);
        while(i < CNT) {
            fprintf(wp, "%lf ", numbers[i]);
            i++;
            Endflag = 1;
        }
        fclose(wp);

        /* output the number of lines. */
        linecnt += 1;
        fprintf(stderr, "[cut2packet] output linecnt = %d\n", linecnt);
        
        if(Endflag == 0) {
            system(FFT_EXE_FILE " < " CUT_TMP_OUTPUT " >> " FFT_TMP_OUTPUT);
        } else {
            break;
        }
    }
    fclose(fp);
    return 0;
}
