#!/usr/bin/env python3
from __future__ import annotations
import json, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/rcms_protocol15_model_selection.json'
F=[
 {'name':'Moresco_Hz','dchi2':0.5526,'daic':-1.4474,'dbic':-2.1555},
 {'name':'PantheonPlus','dchi2':0.4438,'daic':-1.5562,'dbic':-6.9277},
 {'name':'DES_SN5YR','dchi2':1.366399,'daic':-0.633601,'dbic':-6.140193},
 {'name':'eBOSS_DR16','dchi2':3.493168218,'daic':1.493168218,'dbic':None},
 {'name':'DESI_DR2','dchi2':1.305786846,'daic':-0.694213154,'dbic':-1.259164141},
]
P11={'best_nonlog':'saturating','gap_best_control_minus_log':-0.278705302,'log_daic':-0.694214783}
def main():
 aic_pos=sum(x['daic']>0 for x in F)
 bic_app=[x for x in F if x['dbic'] is not None]
 bic_pos=sum(x['dbic']>0 for x in bic_app)
 both=sum(x['daic']>0 and x['dbic'] is not None and x['dbic']>0 for x in F)
 med_aic=statistics.median(x['daic'] for x in F)
 med_bic=statistics.median(x['dbic'] for x in bic_app)
 log_beats=P11['gap_best_control_minus_log']>=2.0
 support=aic_pos>=2 and bic_pos>=2 and both>=2 and log_beats and P11['log_daic']>0
 ref=(aic_pos==0 and bic_pos==0 and not log_beats)
 cls='LOG_MODEL_SELECTION_SUPPORTED' if support else ('REFERENCE_MODEL_SELECTION_FAVORED' if ref else 'NO_MODEL_SELECTION_PREFERENCE')
 payload={'protocol':'P15','status':'FINAL','family_inputs':F,'metrics':{'aic_positive_families':aic_pos,'bic_positive_applicable_families':bic_pos,'both_positive_families':both,'median_Delta_AIC':med_aic,'median_applicable_Delta_BIC':med_bic,'log_beats_best_control_by_2':log_beats},'p01_overlapping_combined_diagnostic':{'Delta_chi2':4.559528,'Delta_AIC':2.559528,'Delta_BIC':-2.829418},'p11':P11,'classification':cls}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print(f'AIC_POSITIVE_FAMILIES={aic_pos}'); print(f'BIC_POSITIVE_APPLICABLE_FAMILIES={bic_pos}'); print(f'BOTH_POSITIVE_FAMILIES={both}'); print(f'MEDIAN_DELTA_AIC={med_aic:.9f}'); print(f'MEDIAN_DELTA_BIC={med_bic:.9f}'); print(f'LOG_BEATS_BEST_CONTROL_BY_2={log_beats}'); print(f'P15_CLASSIFICATION={cls}')
if __name__=='__main__': main()
