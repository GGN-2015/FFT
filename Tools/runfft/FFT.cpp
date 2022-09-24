#include <assert.h>
#include "FFT.h"

const int    maxl = 2094153;//nlogn的最大长度(来自leo学长的博客)
const double PI   = 3.14159265358979;//圆周率,不解释

#define cd Complex

cd a[maxl],b[maxl];//用于储存变换的中间结果
int rev[maxl];//用于储存二进制反转的结果

static void getrev(int bit){
    for(int i=0;i<(1<<bit);i++){//高位决定二进制数的大小
        rev[i]=(rev[i>>1]>>1)|((i&1)<<(bit-1));
    }//能保证(x>>1)<x,满足递推性质
}

void fft(cd* a,int n,int dft){//变换主要过程
    assert(n < maxl);

    int ntmp = n, bit = 0;
    while((ntmp & 1) == 0) {
        ntmp >>= 1;
        bit += 1;
    }
    assert(ntmp == 1);
    getrev(bit);

    for(int i=0;i<n;i++){//按照二进制反转
        if(i<rev[i])//保证只把前面的数和后面的数交换,(否则数组会被翻回来)
            swap(a[i],a[rev[i]]);
    }
    for(int step=1;step<n;step<<=1){//枚举步长的一半
        cd wn=exp(cd(0,dft*PI/step));//计算单位复根
        for(int j=0;j<n;j+=step<<1){//对于每一块
            cd wnk(1,0);//!!每一块都是一个独立序列,都是以零次方位为起始的
            for(int k=j;k<j+step;k++){//蝴蝶操作处理这一块
                cd x=a[k];
                cd y=wnk*a[k+step];
                a[k]=x+y;
                a[k+step]=x-y;
                wnk*=wn;//计算下一次的复根
            }
        }
    }
    if(dft==-1){//如果是反变换,则要将序列除以n
        for(int i=0;i<n;i++)
            a[i]/=n;
    }
}

