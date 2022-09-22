#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cassert>

char filename[200];
FILE *fp, *wp;
int Endflag = 0;
int CNT = 1024;
double numbers[16384];

void init(int args, char* argv[]) { //
	if(args >= 3) {
		int len = strlen(argv[2]);
		CNT = 0;
		for(int i = 0; i < len; i++) {
			CNT = CNT * 10 + argv[2][i] - '0';
		}
		fp = fopen(argv[1], "r");
	} else if(args == 2) {
		fp = fopen(argv[1], "r");
	} else {
		scanf("%s", filename);
		fp = fopen(filename, "r");
	}
	assert(CNT <= 16384);
}

int judge(char tmp) {
	if(tmp >= '0' && tmp <= '9') return 0;
	if(tmp == ' ' || tmp == '.') return 0;
	if(tmp == '-') return 0;
	if(tmp == '\n' || tmp == '\r') return 0;
	if(tmp == EOF) return 1;
	//printf("%c\n", tmp);
	return 1;
}

int main(int args, char* argv[]) {
	init(args, argv);
	char ch;
	fclose(fopen("FFT_tmp.fft", "w"));
	while((ch = fgetc(fp)) != EOF) {
		wp = fopen("cut_tmp.txt", "w");
		int i = 0;
		for(; i < CNT; i++) {
			int pow = 10;
			int flag1 = 1;
			if(judge(ch)) break;
			numbers[i] = 0.0;
			while(ch < '0' || ch > '9') {
				if(judge(ch)) break;
				if(ch == '-') {
					flag1 *= -1;
				}
				ch = fgetc(fp);
			}
			//printf("11111");
			while(ch >= '0' && ch <= '9') {
				numbers[i] = numbers[i] * 10 + ch - '0';
				ch = fgetc(fp);
			}
			if(ch == '.') {
				ch = fgetc(fp);
			}
			while(ch >= '0' && ch <= '9') {
				numbers[i] = numbers[i] + (ch - '0') / pow;
				pow *= 10;
				ch = fgetc(fp);
			}
			numbers[i] *= flag1;
			fprintf(wp, "%lf ", numbers[i]);
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
		
		if(Endflag == 0) {
			
			system("FFT.exe cut_tmp.txt >>FFT_tmp.fft");
		} else {
			break;
		}
	}
	fclose(fp);
	return 0;
}
