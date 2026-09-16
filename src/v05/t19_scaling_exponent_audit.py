"""T19 — scaling exponent audit for the D13-A ring continuum bridge.

Theory-only. Derives/tests which delta_R ~ n^-p keeps the low-mode two-step
generator finite and nonzero. No legacy Resolutive constants are used.
"""
from __future__ import annotations
import json, math


def laplacian_eigenvalue(n:int,j:int)->float:
    return -4.0*math.sin(math.pi*j/n)**2


def scaled_generator_mode(n:int,j:int,c:float,p:float)->list[list[float]]:
    lam=laplacian_eigenvalue(n,j)
    delta=n**(-p)
    # Exact two-step defect on one Laplacian eigenmode:
    # M^2-I = [[0,c lam],[c lam,c^2 lam^2]].
    return [[0.0,c*lam/delta],[c*lam/delta,c*c*lam*lam/delta]]


def fro(A): return math.sqrt(sum(x*x for row in A for x in row))


def run():
    ns=[32,64,128,256,512,1024,2048]
    ps=[1.0,1.5,2.0,2.5,3.0]
    c=0.05
    modes=[1,2,3]
    rows=[]
    for p in ps:
        for j in modes:
            vals=[]
            for n in ns:
                G=scaled_generator_mode(n,j,c,p)
                vals.append({'n':n,'norm':fro(G),'G':G})
            # log-log slope of norm vs n; finite nonzero target requires slope ~0.
            xs=[math.log(v['n']) for v in vals[-4:]]
            ys=[math.log(v['norm']) for v in vals[-4:]]
            xm=sum(xs)/len(xs); ym=sum(ys)/len(ys)
            slope=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/sum((x-xm)**2 for x in xs)
            rows.append({'p':p,'mode':j,'asymptotic_log_slope':slope,'values':vals})
    analytic={'lambda_j_asymptotic':'-4*pi^2*j^2/n^2',
              'leading_scaled_term':'c*lambda_j*n^p ~ -4*c*pi^2*j^2*n^(p-2)',
              'selection':'finite nonzero fixed-j limit iff p=2',
              'p_lt_2':'generator -> 0','p_eq_2':'finite nonzero generator','p_gt_2':'generator diverges'}
    limits=[]
    for j in modes:
        expected=-4*c*math.pi**2*j*j
        G=scaled_generator_mode(65536,j,c,2.0)
        limits.append({'mode':j,'expected_offdiag_limit':expected,
                       'numeric_offdiag_n65536':G[0][1],
                       'relative_error':abs(G[0][1]-expected)/abs(expected)})
    return {'coupling':c,'rows':rows,'analytic':analytic,'p2_limit_checks':limits,
            'guard':'p=2 is selected by the ring Laplacian low-mode scaling, not yet a universal Resolutive exponent.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
