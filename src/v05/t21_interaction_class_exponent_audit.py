"""T21 — interaction-class audit for emergent spectral exponent z_R.

Uses translation-invariant ring symbols so very large resolutions can be tested without
dense matrices. Theory-only: z is a property of the chosen relational operator family,
not yet a universal physical constant.
"""
from __future__ import annotations
import json, math


def symbol_nearest(k):
    return -4.0*math.sin(k/2.0)**2


def symbol_biharmonic(k):
    l=symbol_nearest(k)
    return -(l*l)  # fourth-order low-k magnitude


def symbol_first_order_antisymmetric(k):
    # signed transport/advection-like generator; magnitude ~ |k|
    return 2.0*math.sin(k)


def symbol_finite_range(k, weights):
    # symmetric local graph operator sum_r 2 w_r(cos(rk)-1)
    return sum(2.0*w*(math.cos(r*k)-1.0) for r,w in weights.items())


def symbol_fractional_long_range(k, alpha, cutoff=20000):
    # symmetric power-law kernel sum_r (cos(rk)-1)/r^(1+alpha).
    # For 0<alpha<2 the infinite-range low-k symbol scales as |k|^alpha.
    s=0.0
    for r in range(1,cutoff+1):
        s += 2.0*(math.cos(r*k)-1.0)/(r**(1.0+alpha))
    return s


def fit_z(ns, vals):
    xs=[math.log(2*math.pi/n) for n in ns]
    ys=[math.log(abs(v)) for v in vals]
    xm=sum(xs)/len(xs); ym=sum(ys)/len(ys)
    return sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/sum((x-xm)**2 for x in xs)


def run():
    ns=[128,192,256,384,512,768,1024]
    families={
      'nearest_laplacian': lambda k:symbol_nearest(k),
      'finite_range_r1_r3': lambda k:symbol_finite_range(k,{1:1.0,3:0.35}),
      'biharmonic': lambda k:symbol_biharmonic(k),
      'antisymmetric_first_order': lambda k:symbol_first_order_antisymmetric(k),
    }
    out={}
    for name,fn in families.items():
        vals=[fn(2*math.pi/n) for n in ns]
        out[name]={'values':list(zip(ns,vals)),'z_fit':fit_z(ns[-5:],vals[-5:])}
    # Long-range families use moderate n/cutoff; truncation error is explicitly reported as a caveat.
    for alpha in (0.75,1.25,1.75):
        vals=[symbol_fractional_long_range(2*math.pi/n,alpha) for n in ns]
        out[f'powerlaw_alpha_{alpha}']={'values':list(zip(ns,vals)),
                                      'z_fit':fit_z(ns[-5:],vals[-5:]),
                                      'expected_infinite_range_z':alpha,
                                      'caveat':'finite kernel cutoff biases asymptotic fit'}
    return {'families':out,
            'classification':{
              'finite_symmetric_local':'generically z=2 if second moment is finite and nonzero',
              'higher_order_tuned':'can give z=4 or higher',
              'antisymmetric_transport':'can give z=1',
              'powerlaw_nonlocal':'can give fractional z in the infinite-range limit'},
            'general_scaling':'if |lambda(k)| ~ C |k|^z_R, choose delta_R ~ L^-z_R for a finite nonzero fixed-mode generator',
            'guard':'z_R labels an emergent spectral/dynamical universality class; no universal value is claimed.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
