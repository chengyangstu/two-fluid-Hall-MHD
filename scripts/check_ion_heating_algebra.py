"""Selected symbolic teaching checks, not validation of physical closures."""
from pathlib import Path
import json
import sympy as s
P=Path(__file__).resolve().parents[1]
ui=s.Matrix(s.symbols('uix uiy uiz',real=True)); j=s.Matrix(s.symbols('Jx Jy Jz',real=True)); b=s.Matrix(s.symbols('Bx By Bz',real=True))
e,n,alpha,m,V,T=s.symbols('e n alpha m V T',positive=True)
ue=ui-j/(e*n); eh=j.cross(b)/(e*n)
hall=s.simplify(j.dot(eh)); works=s.simplify(e*n*ui.dot(eh)-e*n*ue.dot(eh))
re=alpha*(ui-ue); ri=-re
friction=s.simplify(ui.dot(ri)+ue.dot(re)+alpha*j.dot(j)/(e*n)**2)
p1,p2,p3,nu=s.symbols('Pxx Pyy Pzz nu',real=True); p=(p1+p2+p3)/3
trace=s.simplify(nu*((p1-p)+(p2-p)+(p3-p)))
mean=(V-V)/2; second=((T/m+V**2)+(T/m+(-V)**2))/2
beam=s.simplify((m*(second-mean**2)+2*T)/3-(T+m*V**2/3))
checks={'Hall_total_work_zero':hall,'Hall_species_sum_zero':works,'friction_energy_recovery':friction,'ten_moment_relaxation_trace_zero':trace,'two_beam_scalar_temperature':beam}
# Local signed-gradient orbit equation and the pickup central-moment trace.
q,G,B0,dxdt=s.symbols('q G B0 dxdt',real=True)
yacc=-q*B0*dxdt/m
xjerk=q*G*dxdt/m+q*B0*yacc/m
checks['signed_gradient_orbit']=s.simplify(xjerk-(q*G/m-(q*B0/m)**2)*dxdt)
BL,BM,v0=s.symbols('BL BM v0',real=True)
tpar=m*v0**2*BL**2/(BL**2+BM**2)
tperp=m*v0**2*BM**2/(2*(BL**2+BM**2))
checks['pickup_temperature_trace']=s.simplify((tpar+2*tperp)/3-m*v0**2/3)
assert all(x==0 for x in checks.values())
result={'date':'2026-11-13','checks':{k:str(x) for k,x in checks.items()},'passed':True,'limits':'Symbolic identities only; no plasma simulations or validation of closures/entropy production.'}
(P/'research/ion_heating/algebra_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(result)
