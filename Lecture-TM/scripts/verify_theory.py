# coding: utf-8
"""Check selected derivations and all numerical examples in TM chapters 1--4."""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
x, K = s.symbols('x K', positive=True)
f = s.exp(-K*x)*(K+s.tanh(x))
harris = s.simplify(s.diff(f,x,2)-(K**2-2/s.cosh(x)**2)*f) == 0
delta = s.simplify(2*s.diff(f,x).subs(x,0)/f.subs(x,0)-2*(1/K-K)) == 0
p = s.symbols('p', positive=True)
# Verify the variable substitution leading to modified Bessel order 1/4.
H = s.Function('H')
F = s.sqrt(p)*H(p**2/2)
z = s.symbols('z', positive=True)
res = s.diff(F,p,2)-p**2*F
expected = p**s.Rational(5,2)*(s.Subs(s.diff(H(z),z,2),z,p**2/2)
           +2/p**2*s.Subs(s.diff(H(z),z),z,p**2/2)
           -(1+1/(4*p**4))*H(p**2/2))
bessel = s.simplify(res-expected) == 0
mp.mp.dps=40
rin = lambda m:(mp.ellipk(m)-2*mp.ellipe(m))**2/mp.ellipk(m)
rout = lambda m:m**mp.mpf('-1.5')*((2/m-1)*mp.ellipk(m)-2*mp.ellipe(m)/m)**2/mp.ellipk(m)
Iin=mp.quad(rin,[0,.5,.9,.99,1])
Iout=mp.quad(rout,[mp.mpf('1e-8'),.5,.9,.99,1])
I1=4/mp.pi*(Iin+Iout)
I=2*math.pi*math.gamma(.75)/math.gamma(.25)
Cg=I**(-.8); Cd=I**(-.2)
cases=[]
for Sa,Kval in [(1e6,.5),(1e6,.05),(1e6,.01),(1e8,.5)]:
    a=.1; Va=1e5; D=a*Va/Sa; Delta=2*(1/Kval-Kval)
    eps=Cd*Sa**(-.4)*Delta**.2*Kval**(-.4)
    g=Cg*Sa**(-.6)*Delta**.8*Kval**.4
    cases.append(dict(Sa=Sa,K=Kval,Delta=Delta,a=a,VA=Va,Deta=D,
      gamma_FKR=g*Va/a,delta_star_FKR=eps*a,Delta_delta=Delta*eps,
      tau_growth_FKR=a/(Va*g),valid_constant_psi=Delta*eps<.1,
      delta_large_order=a*Sa**(-1/3)*Kval**(-1/3),
      gamma_large_order=Va/a*Sa**(-1/3)*Kval**(2/3)))
example=cases[0]
eta=4*math.pi*1e-7*.01
t_nl=2/example['gamma_FKR']*math.log(example['delta_star_FKR']/1e-5)
nu_ratio=1e-6/(example['gamma_FKR']*example['delta_star_FKR']**2)
rutherford_time=(.003-.001)*float(I1)/(.0001*30)
di=math.sqrt(1.673e-27/(4*math.pi*1e-7*1e20*(1.602e-19)**2))
de=di*math.sqrt(9.109e-31/1.673e-27)
electron_time_inertia_ratio=example['gamma_FKR']*de**2/example['Deta']
checks=dict(harris_ODE=harris,harris_delta=delta,bessel_substitution=bessel,
            Rutherford_integral=abs(float(I1)-.8227058113039288)<1e-12)
assert all(checks.values()),checks
record=dict(date='2026-11-16',checks=checks,
    constants=dict(FKR_I=I,Cgamma=Cg,Cdelta=Cd,Rutherford_I1=float(I1),
                   Rutherford_integral_inside=float(Iin),Rutherford_integral_outside=float(Iout)),
    FKR_cases=cases,other_examples=dict(eta=eta,nonlinear_onset_time=t_nl,
    viscosity_ratio_at_nu_1e_6=nu_ratio,Rutherford_growth_time=rutherford_time,
    di_n_1e20=di,de_n_1e20=de,
    electron_time_inertia_to_resistivity=electron_time_inertia_ratio),
    scope='Selected exact identities and worked arithmetic; not a full eigenvalue simulation or experimental reproduction.')
(ROOT/'research/theory_checks.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':checks,'constants':record['constants']},ensure_ascii=False,indent=2))
