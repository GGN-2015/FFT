#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* at most 16384 column. */
const int MAXN = 16384;

double sum[MAXN]; // sum for every column
double sqr[MAXN]; // sqrsum for every column

double Mean[MAXN], Var[MAXN];

/* list node: one node for each line. */
typedef struct _ListNode {
    double val[MAXN];
    _ListNode* nxt; // next row
} ListNode;

ListNode* head = NULL;
ListNode* tail = NULL;

static void CreateNewLine() {
    /* ask for a new node from dump. */
    ListNode* node = (ListNode*)malloc(sizeof(ListNode)); 
    node -> nxt    = NULL;

    if(head == NULL) {
        head = tail = node;
    }else {
        tail -> nxt = node;
        tail        = node; // become new tail
    }
}

/* insert a value into current line. */
static void InsertValue(int pos, double value) {
    assert(tail != NULL);
    assert(0 <= pos && pos < MAXN);

    tail -> val[pos] = value;
}

/* free the memory of the whole list. */
static void FreeListMemory() {
    ListNode* ptmp;
    ListNode* pnow = head; // free from the beginning

    head = tail = NULL;

    /* free memory. */
    while(pnow != NULL) {
        ptmp = pnow;
        pnow = pnow -> nxt;
        free(ptmp);
    }
}

int main(int argc, char* argv[]) {
    /* check if argc == 2 */
    if(argc != 2) {
        fprintf(stderr, "[zstd] Usage: %s <LineWidth>\n", argv[0]);
        return 1;
    }

    int LineWidth = atoi(argv[1]);
    int cnt       = 0;
    int lineCnt   = 0;
    assert(0 < LineWidth && LineWidth <= MAXN);
    
    /* input all the data. */
    CreateNewLine();
    double dtmp;
    while(scanf("%lf", &dtmp) > 0) {

        /* this is not a good method to calculate. */
        /* because it lose accuracy. */
        sum[cnt] += dtmp;
        sqr[cnt] += dtmp * dtmp;

        /* add a value into current line. */
        InsertValue(cnt, dtmp);

        cnt += 1;
        if(cnt == LineWidth) {
            CreateNewLine();
            cnt = 0;
            lineCnt += 1;
        }
    }
    /* every row must be full. */
    assert(cnt == 0);

    /* solve Var and Mean for each column. */
    assert(lineCnt > 0);
    for(int i = 0; i < LineWidth; i += 1) {
        Mean[i] = sum[i] / lineCnt;
        Var [i] = sqrt((sqr[i] / lineCnt) - Mean[i] * Mean[i]);
    }

    /* output solution */
    int line = 0;
    for(ListNode* pnow = head; line < lineCnt; line += 1, pnow = pnow -> nxt) {
        for(int i = 0; i < LineWidth; i += 1) {
            printf("%.20lf ", (pnow -> val[i] - Mean[i])/Var[i]);
        }
        putchar('\n');
    }

    /* free memory for the list. */
    FreeListMemory();
    return 0;
}

