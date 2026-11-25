import sys
from collections import Counter
sys.path.insert(0,'/mnt/c/Users/PC/Documents/Codex/2026-11-25/jie/outputs')
from verify_three_row_ant import profiles

def visit(board, w, entry):
    b = board[:]; r = entry; c = 0; h = 0
    dx=[1,0,-1,0]; dy=[0,1,0,-1]; steps = 0
    while True:
        idx = r*w + c; bit = b[idx]
        h = (h + (1 if bit else 3)) % 4
        b[idx] = 1 - bit
        c += dx[h]; r += dy[h]; steps += 1
        if c < 0: return b, r, steps, True
        if c >= w or r < 0 or r >= 3: return b, -1, steps, False

def enum_indep(w, maxvisits=6):
    maxima = {(): 0}; violations = 0
    for mask in range(1 << (3*w)):
        board0 = [(mask >> i) & 1 for i in range(3*w)]
        for parity in (0,1):
            rows = (0,2) if parity==0 else (1,)
            def dfs(b, prefix, steps, visits):
                nonlocal violations
                for e in rows:
                    nb, reply, st, returned = visit(b, w, e)
                    rec = prefix + ((e, reply),)
                    maxima[rec] = max(steps+st, maxima.get(rec, -1))
                    if returned:
                        if visits >= 4: violations += 1
                        elif visits+1 < maxvisits: dfs(nb, rec, steps+st, visits+1)
            dfs(board0, (), 0, 0)
    return maxima, violations

for w in (2,4):
    ref = profiles(w); ind, viol = enum_indep(w)
    print('width', w, '| ref records', len(ref), '| ind records', len(ind), '| keys equal', set(ref)==set(ind), '| guard violations', viol)
    if set(ref)==set(ind):
        print('   P values identical:', all(ref[k]==ind[k] for k in ref))
    else:
        print('   extra:', sorted(set(ind)-set(ref))[:5], 'missing:', sorted(set(ref)-set(ind))[:5])

P2 = profiles(2); P4 = profiles(4)
dist = Counter(P4[k]-P2[k] for k in P4)
print('distribution:', dict(sorted(dist.items())), '| max diff', max(P4[k]-P2[k] for k in P4))
print('example (0>1,0>X): P2=%s P4=%s' % (P2[((0,1),(0,-1))], P4[((0,1),(0,-1))]))
print('all diffs nonneg:', all(P4[k]>=P2[k] for k in P4))
