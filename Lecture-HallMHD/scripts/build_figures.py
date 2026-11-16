# coding: utf-8
"""Reproducible SI teaching calculations and original analytical diagrams."""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
P=Path(__file__).resolve().parents[1];F=P/'figures';F.mkdir(exist_ok=True)
e=1.602176634e-19;me=9.1093837139e-31;mi=1.67262192595e-27;mu=1.25663706127e-6;eps=8.8541878188e-12;c=1/(mu*eps)**.5
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160,'savefig.bbox':'tight','axes.labelsize':11,'axes.titleweight':'bold'})
colors=['#205b80','#cf6939','#278475','#98589b']
def save(fig,name):
 fig.savefig(F/(name+'.pdf'));fig.savefig(F/(name+'.png'),dpi=150);plt.close(fig)
def calc(n,B,Te,Ti,L,ln):
 VA=B/(mu*n*mi)**.5;di=(mi/(mu*n*e**2))**.5;de=(me/(mu*n*e**2))**.5
 nuei=4*(2*np.pi)**.5*n*e**4*ln/(3*(4*np.pi*eps)**2*me**.5*(e*Te)**1.5)
 eta=me*nuei/(n*e**2);D=eta/mu;S=L*VA/D
 vte=(2*e*Te/me)**.5;vti=(2*e*Ti/mi)**.5;Oi=e*B/mi;Oe=e*B/me
 return dict(n=n,B=B,Te=Te,Ti=Ti,L=L,lnLambda=ln,VA=VA,di=di,de=de,lambdaD=(eps*e*Te/(n*e**2))**.5,Omega_i=Oi,Omega_e=Oe,omega_pe=(n*e**2/(eps*me))**.5,vte=vte,vti=vti,rho_i=vti/Oi,rho_e=vte/Oe,rho_s=(e*Te/mi)**.5/Oi,beta_e=2*mu*n*e*Te/B**2,beta_i=2*mu*n*e*Ti/B**2,nuei=nuei,eta_drag=eta,Deta=D,S=S,deltaSP=L/S**.5,vinSP=VA/S**.5,E_SP=B*VA/S**.5,E_A=B*VA,tauA=L/VA,taueta=L**2/D,mfp_e=vte/nuei)
params={'dense':(1e21,.05,5,5,10,7),'lab':(1e19,.05,20,20,1,10),'space':(1e7,20e-9,100,1000,1e7,20),'corona':(1e15,.005,100,100,1e7,20)}
D={k:calc(*v) for k,v in params.items()};(P/'research/calculations.json').write_text(json.dumps({'constants_SI':dict(e=e,me=me,mi=mi,mu0=mu,epsilon0=eps,c=c),'cases':D},indent=2)+'\n')
def texnum(x):
 if x==0:return '0'
 if .01<=abs(x)<1000:return f'{x:.3g}'
 power=int(math.floor(math.log10(abs(x))));return f'{x/10**power:.3g}\\times10^{{{power}}}'
rows=[('n',r'$n\ (\mathrm{m^{-3}})$'),('B',r'$B\ (\mathrm T)$'),('Te',r'$T_e\ (\mathrm{eV})$'),('Ti',r'$T_i\ (\mathrm{eV})$'),('L',r'$L\ (\mathrm m)$'),('VA',r'$V_A\ (\mathrm{m/s})$'),('di',r'$d_i\ (\mathrm m)$'),('de',r'$d_e\ (\mathrm m)$'),('lambdaD',r'$\lambda_{De}\ (\mathrm m)$'),('rho_i',r'$\rho_i\ (\mathrm m)$'),('rho_s',r'$\rho_s\ (\mathrm m)$'),('beta_e',r'$\beta_e$'),('beta_i',r'$\beta_i$'),('nuei',r'$\nu_{ei}\ (\mathrm{s^{-1}})$'),('eta_drag',r'$\eta_D\ (\Omega\,\mathrm m)$'),('Deta',r'$D_\eta\ (\mathrm{m^2/s})$'),('S',r'$S_L$'),('deltaSP',r'$\delta_{SP}\ (\mathrm m)$'),('mfp_e',r'$\lambda_{\mathrm{mfp},e}\ (\mathrm m)$'),('tauA',r'$\tau_A\ (\mathrm s)$')]
s=[r'\begin{longtable}{P{38mm}rrrr}',r'\toprule 量 & 高密度 & 实验室量级 & 磁层量级 & 日冕量级\\\midrule\endfirsthead',r'\toprule 量 & 高密度 & 实验室量级 & 磁层量级 & 日冕量级\\\midrule\endhead']
for key,label in rows:s.append(label+' & '+' & '.join('$'+texnum(v[key])+'$' for v in D.values())+r'\\')
s+=[r'\bottomrule\end{longtable}'];(P/'chapters/parameter_table.tex').write_text('\n'.join(s)+'\n')
# 1: Geometry of reconnection, schematic only.
fig,ax=plt.subplots(figsize=(8,4.2));x=np.linspace(-3.8,3.8,600);y=np.linspace(-2.2,2.2,400);X,Y=np.meshgrid(x,y);A=.5*(Y**2-.28*X**2)
ax.contour(X,Y,A,levels=[-1.2,-.6,-.2,.2,.6,1.2],colors=colors[0],linewidths=1.3)
ax.plot(x,np.sqrt(.28)*x,'--',c='.4',lw=.8);ax.plot(x,-np.sqrt(.28)*x,'--',c='.4',lw=.8)
ax.add_patch(Rectangle((-1,-.32),2,.64,facecolor='#e1eff5',edgecolor=colors[0],zorder=0));ax.add_patch(Rectangle((-.38,-.09),.76,.18,facecolor='#eebc9f',edgecolor=colors[1],zorder=1))
for a,b in [((0,2),(0,.55)),((0,-2),(0,-.55)),((1.2,0),(3.3,0)),((-1.2,0),(-3.3,0))]:ax.annotate('',b,a,arrowprops=dict(arrowstyle='->',color=colors[2],lw=2))
ax.text(.1,1.4,'inflow',color=colors[2]);ax.text(2.05,.18,'outflow',color=colors[2]);ax.text(-.98,.45,'ion region');ax.annotate('electron region',(-.2,-.07),(-2.8,-1.7),arrowprops=dict(arrowstyle='->',lw=.8));ax.text(.1,.08,'X');ax.text(2.3,-1.8,r'$z$: current / guide field')
ax.set(xlim=(-3.8,3.8),ylim=(-2.2,2.2),xlabel=r'$x$: outflow',ylabel=r'$y$: inflow',title='Reconnection geometry: schematic, not a simulation');ax.set_aspect('equal');save(fig,'01_geometry')
# 2: Harris force balance.
u=np.linspace(-4,4,600);fig,axs=plt.subplots(1,2,figsize=(8,3.1));axs[0].plot(u,np.tanh(u),label=r'$B_x/B_0$');axs[0].plot(u,1/np.cosh(u)**2,label=r'$-\mu_0 aJ_z/B_0$');axs[0].set(xlabel=r'$y/a$',title='Field reversal and current');axs[0].legend()
axs[1].plot(u,np.tanh(u)**2,label='magnetic pressure');axs[1].plot(u,1/np.cosh(u)**2,label='excess thermal pressure');axs[1].plot(u,np.ones_like(u),'k--',label='sum');axs[1].set(xlabel=r'$y/a$',ylabel=r'normalized by $B_0^2/(2\mu_0)$',title='Force balance');axs[1].legend(fontsize=8);fig.tight_layout();save(fig,'02_harris')
# 3: scale hierarchy across teaching cases.
fig,ax=plt.subplots(figsize=(8,3.7));labels={'dense':'dense','lab':'laboratory scale','space':'magnetospheric scale','corona':'coronal scale'}
for j,(name,v) in enumerate(D.items()):
 vals=[v[k] for k in ['lambdaD','de','di','L']];ax.plot(np.log10(vals),np.repeat(j,4),color='.75')
 for k,(a,m,c0) in enumerate(zip(vals,['o','s','D','^'],colors)):ax.scatter(np.log10(a),j,marker=m,color=c0,s=55,label=[r'$\lambda_{De}$',r'$d_e$',r'$d_i$',r'$L$'][k] if j==0 else None)
ax.set(yticks=range(4),yticklabels=[labels[k] for k in D],xlabel=r'length scale: $\log_{10}(\ell/\mathrm{m})$',title='Every point is calculated from declared teaching inputs');ax.legend(ncol=4,loc='upper left');ax.set_ylim(-.5,3.8);ax.grid(axis='x',alpha=.2);save(fig,'03_scales')
# 4: Ohm estimates at varying layer thickness, not actual vector balance.
v=D['lab'];ell=np.geomspace(v['de']/3,2,500);fig,ax=plt.subplots(figsize=(7.4,3.7));ax.loglog(ell/v['di'],v['di']/ell,label=r'Hall scale: $d_i/\ell$');ax.loglog(ell/v['di'],.5*v['beta_e']*v['di']/ell,label=r'pressure scale: $(\beta_e/2)d_i/\ell$');ax.loglog(ell/v['di'],v['Deta']/(v['VA']*ell),label=r'drag scale: $D_\eta/(V_A\ell)$');ax.loglog(ell/v['di'],(v['de']/ell)**2,label=r'inertia/Hall: $(d_e/\ell)^2$')
ax.axvline(1,c='.5',ls=':');ax.axvline(v['de']/v['di'],c='.5',ls=':');ax.axhline(1,c='.5',ls='--',lw=.8);ax.set(xlabel=r'$\ell/d_i$',ylabel='dimensionless estimate',ylim=(1e-7,1e2),title='Same-scale estimates; inertia curve has a different denominator');ax.legend(fontsize=8);ax.grid(alpha=.18);save(fig,'04_ordering')
# 5: Hall quadrupole with Ampere-inferred in-plane currents.
xx=np.linspace(-2.6,2.6,151);yy=np.linspace(-1.65,1.65,111);XX,YY=np.meshgrid(xx,yy);H=XX*YY*np.exp(-XX**2/3-YY**2);jx=XX*(1-2*YY**2)*np.exp(-XX**2/3-YY**2);jy=-YY*(1-2*XX**2/3)*np.exp(-XX**2/3-YY**2)
fig,ax=plt.subplots(figsize=(7.4,3.7));im=ax.contourf(XX,YY,H,levels=np.linspace(-.43,.43,19),cmap='RdBu_r',extend='both');ax.streamplot(xx,yy,jx,jy,color='.15',density=.9,linewidth=.7,arrowsize=.8);ax.set(xlabel=r'$x$',ylabel=r'$y$',title=r'Schematic $B_z=xy\exp(-x^2/3-y^2)$; arrows: $(J_x,J_y)$');fig.colorbar(im,ax=ax,label=r'$B_z$ (arbitrary units)');ax.set_aspect('equal');save(fig,'05_quadrupole')
# 6: Parallel Hall-MHD waves.
x=np.geomspace(.02,30,600);wp=.5*x*(np.sqrt(x*x+4)+x);wm=2*x/(np.sqrt(x*x+4)+x);wave_x=x.copy()
fig,ax=plt.subplots(figsize=(7.3,3.7));ax.loglog(x,wp,label='whistler branch');ax.loglog(x,wm,label='ion-cyclotron branch');ax.loglog(x,x,'k--',lw=.9,label=r'ideal MHD: $\omega=kV_A$');ax.loglog(x,x*x,':',color=colors[2],label=r'EMHD asymptote: $\omega/\Omega_i=(kd_i)^2$');ax.axvline(1,ls=':',c='.5');ax.set(xlabel=r'$kd_i$',ylabel=r'$\omega/\Omega_i$',title='Cold, parallel, incompressible Hall-MHD limit');ax.legend(fontsize=8);ax.grid(alpha=.2);save(fig,'06_dispersion')
# 7: SP threshold, globally large S does not settle local model.
x=np.geomspace(1e2,1e14,500);fig,ax=plt.subplots(figsize=(7.2,3.5));ax.loglog(x,x**-.5,c=colors[0],label=r'$\delta_{SP}/L=S_L^{-1/2}$')
for j,(k,v) in enumerate(D.items()):ax.scatter(v['S'],v['deltaSP']/v['L'],color=colors[j]);ax.annotate(k,(v['S'],v['deltaSP']/v['L']),xytext=(4,5),textcoords='offset points',fontsize=8)
for r in [1e-2,1e-4]:ax.axhline(r,ls='--',lw=.8,label=rf'$d_i/L={r:g}$')
ax.set(xlabel=r'$S_L$',ylabel='relative width',title='SP layer compared with a kinetic length');ax.legend(fontsize=8);ax.grid(alpha=.18);save(fig,'07_sp')
# 8: Maxwellian mixture variance identity, analytic distribution.
vx=np.linspace(-5,5,1000);sig=.6;u0=1.7;f=lambda z:np.exp(-z*z/(2*sig**2))/(np.sqrt(2*np.pi)*sig)
fig,ax=plt.subplots(figsize=(7.2,3.3));ax.plot(vx,.5*f(vx-u0),ls='--',c=colors[2],zorder=4,label='population 1');ax.plot(vx,.5*f(vx+u0),ls='--',c=colors[3],zorder=4,label='population 2');ax.plot(vx,.5*(f(vx-u0)+f(vx+u0)),c=colors[0],lw=2,label='sum');ss=np.sqrt(sig**2+u0**2);ax.plot(vx,np.exp(-vx**2/(2*ss**2))/(np.sqrt(2*np.pi)*ss),c=colors[1],label='Gaussian with same variance');ax.set(xlabel='velocity (arbitrary units)',ylabel='normalized distribution',title='Same second moment does not mean the same distribution');ax.legend(fontsize=8);save(fig,'08_multibeam')
# Checks for derived identities and positivity of branch solutions.
checks={'VA_over_Omega_i_equals_di':all(np.isclose(v['VA']/v['Omega_i'],v['di']) for v in D.values()),'de_di_ratio':all(np.isclose(v['de']/v['di'],np.sqrt(me/mi)) for v in D.values()),'rho_i_beta':all(np.isclose(v['rho_i']/v['di'],np.sqrt(v['beta_i'])) for v in D.values()),'rho_s_beta':all(np.isclose(v['rho_s']/v['di'],np.sqrt(v['beta_e']/2)) for v in D.values()),'sp_electric_matching':all(np.isclose(v['eta_drag']*v['B']/(mu*v['deltaSP']),v['E_SP']) for v in D.values()),'hall_dispersion_plus':np.max(np.abs((wp**2-wave_x**2*wp-wave_x**2)/(1+wp**2)))<1e-12,'hall_dispersion_minus':np.max(np.abs(wm**2+wave_x**2*wm-wave_x**2)/(1+wave_x**2))<1e-12}
assert all(checks.values());(P/'research/numerical_checks.json').write_text(json.dumps({k:bool(v) for k,v in checks.items()},indent=2)+'\n')
for k,v in D.items():print(k,{a:float(f'{v[a]:.5g}') for a in ['VA','di','de','lambdaD','rho_i','rho_s','beta_e','beta_i','nuei','eta_drag','Deta','S','deltaSP','mfp_e','tauA','E_SP']})
