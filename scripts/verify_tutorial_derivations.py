"""Independent algebra and numerical checks for the teaching additions.

These checks do not reproduce any research simulation or certify every model.
"""
import json
from pathlib import Path
import sympy as s

P=Path(__file__).resolve().parents[1]
checks={}
mi,me,n,u,w=s.symbols('mi me n u w',positive=True)
M=mi+me
ui=u+me*w/M
ue=u-mi*w/M
checks['center_of_mass']=s.simplify((mi*ui+me*ue)/M-u)==0
checks['relative_velocity']=s.simplify(ui-ue-w)==0
checks['drift_energy']=s.simplify((mi*n*ui**2+me*n*ue**2)/2
    -(M*n*u**2+mi*me*n*w**2/M)/2)==0

x,y,t,a,e=s.symbols('x y t a e',real=True,nonzero=True)
den=s.exp(-a*t)*(2+x*s.exp(-a*t))
vi=s.Matrix([a*x,0,x*y])
J=s.Matrix([2*y,-2*x,x*y])
theta=a
def conv(v,f):
    return f.diff(x)*v[0]+f.diff(y)*v[1]
def D(v,f):
    return f.diff(t)+conv(v,f)
checks['test_density_satisfies_continuity']=s.simplify(D(vi,den)+den*theta)==0
we=J/(e*den)
ve=vi-we
expanded=(D(vi,vi)-D(vi,J)/(e*den)-J*theta/(e*den)
    -conv(J,vi)/(e*den)+conv(J,J)/(e**2*den**2)
    -J*conv(J,den)/(e**2*den**3))
checks['density_dependent_electron_acceleration']=all(
    s.simplify(z)==0 for z in D(ve,ve)-expanded)

z,K=s.symbols('z K',real=True,positive=True)
f=s.exp(-K*z)*(K+s.tanh(z))
checks['Harris_outer_solution']=s.simplify(s.diff(f,z,2)
    -(K**2-2/s.cosh(z)**2)*f)==0
checks['Harris_log_derivative']=s.simplify(
    (s.diff(f,z)/f).subs(z,0)-(1/K-K))==0

xx,yy,zz,xy,xz,yz,B=s.symbols('xx yy zz xy xz yz B',real=True)
pressure=s.Matrix([[xx,xy,xz],[xy,yy,yz],[xz,yz,zz]])
rot=s.Matrix([[0,B,0],[-B,0,0],[0,0,0]])
source=rot*pressure+pressure*rot.T
target=s.Matrix([[2*B*xy,B*(yy-xx),B*yz],
                 [B*(yy-xx),-2*B*xy,-B*xz],[B*yz,-B*xz,0]])
checks['pressure_rotation_components']=all(s.simplify(z)==0 for z in source-target)
checks['pressure_rotation_trace']=s.trace(source)==0
bad=s.Matrix([[1,2,0],[2,1,0],[0,0,1]])
checks['pressure_counterexample']=set(bad.eigenvals())=={-1,1,3}

alpha,beta,de,r=s.symbols('alpha beta de r',positive=True)
checks['two_field_advected_combinations']=all(
    s.simplify(expr.subs({alpha:de*r,beta:r/de}))==0
    for expr in [r**2-alpha*beta,alpha-beta*de**2])

mu0=1.25663706212e-6
eps0=8.8541878128e-12
charge=1.602176634e-19
mp=1.67262192369e-27
mel=9.1093837015e-31
c=299792458.0
n0=1e6;B0=20e-9;Te=100*charge;L=1e6
VA=B0/(mu0*mp*n0)**.5
di=(mp/(mu0*n0*charge**2))**.5
d_e=(mel/(mu0*n0*charge**2))**.5
ld=(eps0*Te/(n0*charge**2))**.5
rho_sound=(mp*Te)**.5/(charge*B0)
numbers={'VA_km_s':VA/1000,'time_s':L/VA,'di_km':di/1000,
 'de_km':d_e/1000,'Debye_m':ld,'rho_sound_km':rho_sound/1000,
 'beta_e':2*mu0*n0*Te/B0**2,'displacement_ratio':(VA/c)**2,
 'relative_charge':(ld/L)**2,
 'tearing_width':1e6**(-2/5)*3**(1/5)*.5**(-2/5),
 'tearing_growth':1e6**(-3/5)*3**(4/5)*.5**(2/5)}
checks['numerical_example_rounding']=(abs(numbers['VA_km_s']-436)<1
    and abs(numbers['Debye_m']-74.3)<.1
    and abs(numbers['rho_sound_km']-51.1)<.1
    and abs(numbers['tearing_width']-.00654)<.00002
    and abs(numbers['tearing_growth']-.000458)<.000002)
report={'checks':checks,'numerical_example':numbers,
 'scope':'Algebraic identities, selected component formulas, analytic outer solution and numerical examples; not a plasma simulation.'}
out=P/'research/textbook_revision/derivation_checks.json'
out.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
assert all(checks.values()), 'A teaching derivation check failed'
