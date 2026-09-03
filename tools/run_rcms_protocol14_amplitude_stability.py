#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/rcms_protocol14_amplitude_stability.json'
FAMILIES=[
 {'name':'Moresco_Hz','best':-1.2800,'lo':-2.58,'hi':0.54},
 {'name':'PantheonPlus','best':0.2139,'lo':-0.1087,'hi':0.5274},
 {'name':'DES_SN5YR','best':0.382099,'lo':0.055322,'hi':0.707729},
 {'name':'eBOSS_DR16','best':1.662222508,'lo':0.650565914,'hi':3.103626193},
 {'name':'DESI_DR2','best':0.210244178,'lo':0.03,'hi':0.40},
]
RADIAL={'best':-0.580,'lo':-0.830,'hi':-0.240}
TRANS={'best':0.860,'lo':0.100,'hi':1.000}
def delta(p,a):
 s=p['best']-p['lo'] if a<p['best'] else p['hi']-p['best']
 return ((a-p['best'])/s)**2
def synth(ps):
 lo=min(p['lo'] for p in ps)-1; hi=max(p['hi'] for p in ps)+1
 n=200001; step=(hi-lo)/(n-1); best=(1e99,None); vals=[]
 for i in range(n):
  a=lo+i*step; s=sum(delta(p,a) for p in ps); vals.append((a,s))
  if s<best[0]: best=(s,a)
 q,amin=best; inside=[a for a,s in vals if s<=q+1]
 return {'A_common':amin,'Q':q,'lo':inside[0],'hi':inside[-1]}
def main():
 full=synth(FAMILIES); df=4
 i2=0.0 if full['Q']<=0 else max(0.0,(full['Q']-df)/full['Q'])
 loo=[]
 for i,p in enumerate(FAMILIES):
  sub=synth([x for j,x in enumerate(FAMILIES) if j!=i]); sh=sub['A_common']-full['A_common']; loo.append({'omitted':p['name'],**sub,'shift':sh})
 maxshift=max(abs(x['shift']) for x in loo)
 inter={p['name']:max(p['lo'],full['lo'])<=min(p['hi'],full['hi']) for p in FAMILIES}; allint=all(inter.values())
 sign=(RADIAL['best']>0)==(TRANS['best']>0); overlap=max(RADIAL['lo'],TRANS['lo'])<=min(RADIAL['hi'],TRANS['hi'])
 gap=0.0 if overlap else max(TRANS['lo']-RADIAL['hi'],RADIAL['lo']-TRANS['hi'],0.0)
 sep=TRANS['best']-RADIAL['best']; sr=RADIAL['hi']-RADIAL['best']; st=TRANS['best']-TRANS['lo']; ds=abs(sep)/math.sqrt(sr*sr+st*st)
 layer=full['Q']<=9.488 and maxshift<=0.10 and allint
 cls='AMPLITUDE_STABLE' if layer and sign and overlap else ('AMPLITUDE_FAMILY_STABLE_CHANNEL_TENSION' if layer else 'AMPLITUDE_FAMILY_HETEROGENEOUS')
 payload={'protocol':'P14','status':'FINAL','independence_assumed':False,'family_layer':{'full':full,'df_descriptive':df,'I2_descriptive':i2,'leave_one_out':loo,'max_abs_leave_one_out_shift':maxshift,'family_interval_intersects_common':inter,'all_family_intervals_intersect_common':allint},'channel_layer':{'radial':RADIAL,'transverse_volume':TRANS,'sign_agreement':sign,'interval_overlap':overlap,'interval_gap':gap,'descriptive_separation_sigma_diagonal_approx':ds,'formal_p_value_allowed':False},'classification':cls}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print(f"A_common={full['A_common']:.9f} interval=[{full['lo']:.9f},{full['hi']:.9f}] Q={full['Q']:.9f} I2={i2:.9f}")
 print(f'MAX_LOO_SHIFT={maxshift:.9f}'); print(f'ALL_FAMILY_INTERVALS_INTERSECT_COMMON={allint}'); print(f'CHANNEL_SIGN_AGREEMENT={sign}'); print(f'CHANNEL_INTERVAL_OVERLAP={overlap}'); print(f'CHANNEL_INTERVAL_GAP={gap:.9f}'); print(f'CHANNEL_SEPARATION_DIAG_SIGMA={ds:.9f}'); print(f'P14_CLASSIFICATION={cls}')
if __name__=='__main__': main()
