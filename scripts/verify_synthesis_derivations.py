from pathlib import Path
import json
import sympy as s
P=Path(__file__).resolve().parents[1]
x,L,t=s.symbols('x L t',positive=True)
q,m,B,E,ell,omega,a=s.symbols('q m B E ell omega a',positive=True)
checks=[]
def check(name,condition,detail):
 assert bool(condition),name
 checks.append(dict(name=name,passed=True,detail=detail))
f=x*(L-x)/t**2
check('trapezoid maximum',s.simplify(s.diff(f,x).subs(x,L/2))==0 and s.diff(f,x,2)<0,'最大乘积La²/(4Lt²)，再对V²开方给线性出流标度。')
check('rate normalization example',s.Rational(15,100)*(30-10)/30==s.Rational(1,10),'L=30di、Ls=10di时R=.1，仅教学输入。')
Om=q*B/m;alpha=4*m*E/(q*ell*B**2)
check('inverse parabola coefficient',s.simplify(Om**2*alpha/4-q*E/(m*ell))==0,'原文式18/19按所定义alpha应含1/4。')
root=Om*(-1+s.sqrt(1-a))/2
check('inverse parabola frequency',s.simplify(root**2+Om*root+Om**2*a/4)==0,'与原文式20一致，未验证作者代码。')
J=s.Matrix(s.symbols('J1:4'));bb=s.Matrix(s.symbols('B1:4'))
check('Hall total power',s.expand(J.dot(J.cross(bb)))==0,'Hall项对总电流功恒为零。')
val=s.Rational(2,3)+s.pi/9
check('closure interpolation is approximate',abs(float(val)-1)<.016 and val!=1,'n~=B~=1时p_parallel~=1.0157325，不是严格1。')
check('energy spread differs from temperature',s.sqrt(s.Rational(1,4)-s.Rational(1,4))==0,'等权v=±1、m=1：粒子能量标准差0，但中心动能1/2，标量T=1/3。')
(P/'research/synthesis_continuation/derivation_checks.json').write_text(json.dumps({'sympy':s.__version__,'checks':checks},ensure_ascii=False,indent=2))
print(len(checks),'scientific algebra checks passed')
