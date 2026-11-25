#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int n, rows=3, cells;
int dx[4]={1,0,-1,0}, dy[4]={0,1,0,-1}; /* E,S,W,N */

static inline int nexth(int h, int right){ return (h + (right?1:3)) & 3; }

int main(int argc,char**argv){
    int maxn = atoi(argv[1]);
    for(n=1;n<=maxn;n++){
        cells=rows*n;
        if(cells>24){ printf("%d: skip (too many cells)\n", n); continue; }
        uint32_t total = 1u<<cells;
        long best=0; int bpose=0, bhead=0; uint32_t bmask=0;
        for(uint32_t mask=0; mask<total; mask++){
            for(int start=0; start<cells; start++){
                for(int h0=0; h0<4; h0++){
                    uint32_t b=mask; int x=start%n, y=start/n, h=h0; long steps=0;
                    for(;;){
                        int idx=y*n+x;
                        int right = (b>>idx)&1;
                        b ^= 1u<<idx;
                        h = nexth(h, right);
                        x += dx[h]; y += dy[h];
                        steps++;
                        if(x<0||x>=n||y<0||y>=rows){ break; }
                    }
                    if(steps>best){ best=steps; bpose=start; bhead=h0; bmask=mask; }
                }
            }
        }
        printf("n=%d S3_%d=%ld (pose row %d col %d head %d)\n", n, n, best, bpose/n, bpose%n, bhead);
    }
    return 0;
}
