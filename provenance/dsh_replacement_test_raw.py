import random, itertools
DX=[1,0,-1,0]; DY=[0,1,0,-1]  # E,S,W,N

def run(board, m, r, c, h, blockw):
    """Simulate on 3 x m board; return (steps, record, internal_steps).
    record = tuple of (entry_row, reply) for visits to rightmost blockw columns."""
    b=board[:]; n=m; steps=0; internal=0; rec=[]; in_block=False; entry=None
    blk_start = m - blockw
    while True:
        idx=r*n+c; color=b[idx]
        h=(h+(1 if color else 3))&3
        b[idx]=1-color
        nr,nc=r+DY[h], c+DX[h]
        start_in_block = (c >= blk_start)
        steps += 1
        if start_in_block: internal += 1
        # entry into block
        if (c == blk_start-1) and (nc == blk_start) and 0<=nr<3:
            entry = nr; in_block=True
        if start_in_block and not (0<=nr<3 and 0<=nc<n):
            rec.append((entry,-1)); return steps, tuple(rec), internal
        if start_in_block and nc == blk_start-1:
            rec.append((entry, nr)); in_block=False; entry=None
        r,c = nr,nc
        if not (0<=r<3 and 0<=c<n):
            return steps, tuple(rec), internal

def block_profile(w):
    """max internal steps for each record, width w, right-end block, left-face entry."""
    maxima={():0}
    for mask in range(1<<(3*w)):
        board=[(mask>>i)&1 for i in range(3*w)]
        for rows in ((0,2),(1,)):
            def dfs(b, prefix, steps):
                for e in rows:
                    nb=b[:]; rr=e; cc=0; h=0; st=0; out=False
                    while True:
                        idx=rr*w+cc; col=nb[idx]
                        h=(h+(1 if col else 3))&3; nb[idx]=1-col
                        nr,nc=rr+DY[h], cc+DX[h]; st+=1
                        if nc<0:  # returned west
                            rec=prefix+((e,rr),)
                            maxima[rec]=max(steps+st, maxima.get(rec,-1))
                            dfs(nb, rec, steps+st); out=True; break
                        if not(0<=nr<3 and 0<=nc<w):
                            rec=prefix+((e,-1),)
                            maxima[rec]=max(steps+st, maxima.get(rec,-1)); out=True; break
                        rr,cc=nr,nc
                    if out: pass
            dfs(board, (), 0)
    return maxima

PROF2=block_profile(2)
random.seed(42)
checked=0; fails=[]
for trial in range(400):
    n=random.choice([8,9,10])
    mask=random.getrandbits(3*n)
    board=[(mask>>i)&1 for i in range(3*n)]
    sc=random.randrange(0, n-4)   # start column outside right block
    sr=random.randrange(0,3); sh_=random.randrange(0,4)
    T_old, rec, internal = run(board, n, sr, sc, sh_, 4)
    # find width-2 coloring realizing rec with max internal steps
    best=None
    for m2 in range(1<<6):
        b2=[(m2>>i)&1 for i in range(6)]
        # simulate record visits on 2-wide block, local coords
        bb=b2[:]; ok=True; tot=0
        for (e,reply) in rec:
            rr=e; cc=0; h=0
            while True:
                idx=rr*2+cc; col=bb[idx]
                h=(h+(1 if col else 3))&3; bb[idx]=1-col
                nr,nc=rr+DY[h], cc+DX[h]; tot+=1
                if nc<0:
                    if nr!=reply: ok=False
                    break
                if not(0<=nr<3 and 0<=nc<2):
                    if reply!=-1: ok=False
                    break
                rr,cc=nr,nc
            if not ok: break
        if ok and (best is None or tot>best[0]): best=(tot,b2)
    if best is None:
        fails.append(('no realization', n, rec)); continue
    tot2,b2=best
    # new board width n-2: outside columns 0..n-5 unchanged, plus 2-wide block
    m=n-2
    newb=[0]*(3*m)
    for rr in range(3):
        for cc in range(n-4):
            newb[rr*m+cc]=board[rr*n+cc]
        for cc in range(2):
            newb[rr*m+(n-4+cc)]=b2[rr*2+cc]
    T_new, rec2, internal2 = run(newb, m, sr, sc, sh_, 2)
    checked+=1
    if not (T_new >= T_old-20) or rec2!=rec:
        fails.append((n, T_old, T_new, rec, rec2))
print('checked', checked, 'failures', len(fails))
for f in fails[:5]: print('FAIL', f)
