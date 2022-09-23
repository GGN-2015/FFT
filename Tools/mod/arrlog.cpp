#include <cassert>
#include <cmath>
#include <cstdio>

int main(int argc, char* argv[]) {
    
    /* argc[1]: lineWidth. */
    if(argc != 2) {
        fprintf(stderr, "[arrlog.Error] Usage: %s <lineWidth>\n", argv[0]);
        return 1;
    }

    /* get arguments from argv[]. */
    int cnt = 0;
    int lineWidth = atoi(argv[1]);

    /* input double data from stdin and output log data to stdout. */
    double dtmp;
    while(scanf("%lf", &dtmp) != -1) {
        
        /* input value must be >= 0. */
        assert(dtmp >= 0);
        printf("%lf ", std::log10(dtmp + 1));

        /* create a new line if necessary. */
        cnt += 1;
        if(cnt == lineWidth) {
            printf("\n");
            cnt = 0;
        }
    }

    return 0;
}
