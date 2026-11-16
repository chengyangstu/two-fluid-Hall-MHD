# coding: utf-8
"""Original analytic/schematic teaching figures. No experimental data are plotted."""
from pathlib import Path
import math,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
P=Path(__file__).resolve().parents[1]; F=P/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':11,'axes.labelsize':10,'legend.fontsize':9,'savefig.bbox':'tight','pdf.fonttype':42,'figure.constrained_layout.use':True})
blue='#245a81';orange='#cb6b36';green='#39806a';gray='#6c7480'
manifest=[]
def save(fig,name,kind,parameters):
 fig.savefig(F/(name+'.pdf'));fig.savefig(F/(name+'.png'),dpi=165);plt.close(fig)
 manifest.append({'file':'figures/'+name+'.pdf','kind':kind,'parameters':parameters,'experimental_data':False})
# 1: contours are exact contours of a prescribed analytic flux, not an MHD solution.
y=np.linspace(0,2*np.pi,650);x=np.linspace(-1.25,1.25,320);Y,X=np.meshgrid(y,x)
fig,axs=plt.subplots(1,2,figsize=(9.3,3.4),sharex=True,sharey=True)
for ax,amp,title in zip(axs,[0,.09],['Unperturbed shear field','Perturbed field: O and X points']):
 psi=.5*X**2+amp*np.cos(Y)
 ax.contour(Y/np.pi,X,psi,levels=np.linspace(-.08,.7,20),colors=blue,linewidths=.8)
 ax.set(xlabel=r'$ky/\pi$',title=title,xlim=(0,2),ylim=(-1.2,1.2));ax.grid(alpha=.12)
axs[0].set_ylabel(r'$x$ (normalized)')
axs[1].contour(Y/np.pi,X,.5*X**2+.09*np.cos(Y),levels=[.09],colors=orange,linewidths=1.8)
axs[1].plot([0,2],[0,0],'x',color=orange,ms=7);axs[1].plot(1,0,'o',color=green,ms=5)
axs[1].text(1.05,.04,'O',color=green);axs[1].text(.07,.06,'X',color=orange)
axs[1].annotate('',xy=(1,.6),xytext=(1,-.6),arrowprops={'arrowstyle':'<->','color':'black'})
axs[1].text(1.06,-.3,r'$W=1.2$',fontsize=10)
save(fig,'tm_island','analytic magnetic flux contours',{'Bprime':1,'psi_tilde':.09,'k':1,'W_full':1.2,'convention':'B=z cross grad psi; O at ky=pi'})
# 2 exact Harris outer solution and Delta prime.
fig,axs=plt.subplots(1,2,figsize=(9.3,3.5));K=np.linspace(.15,2,450)
axs[0].plot(K,2*(1/K-K),color=blue,lw=2);axs[0].axhline(0,color=gray,lw=1);axs[0].axvline(1,color=gray,ls=':')
axs[0].set(xlabel=r'$K=ka$',ylabel=r'$\Delta^\prime a$',ylim=(-4,14),title='Harris sheet: stability drive');axs[0].text(.27,9,r'$\Delta^\prime a=2(K^{-1}-K)$')
xx=np.linspace(-5,5,700)
for kk,co in [(.5,blue),(1.5,orange)]:
 psi=np.exp(-kk*np.abs(xx))*(1+np.tanh(np.abs(xx))/kk)
 axs[1].plot(xx,psi,label=f'ka = {kk:g}',color=co,lw=1.7)
axs[1].axvline(0,color=gray,ls=':',lw=1);axs[1].set(xlabel=r'$x/a$',ylabel=r'$\widetilde\psi(x)/\widetilde\psi(0)$',title='Ideal outer solutions, extrapolated');axs[1].legend()
save(fig,'tm_harris_delta','exact ideal outer solution',{'K_cases':[.5,1.5],'formula':'exp(-K|X|)(1+tanh|X|/K)','not_inner_solution':True})
# 3 a matching illustration, explicitly not a computed resistive layer.
fig,axs=plt.subplots(1,2,figsize=(9.3,3.5));xx=np.linspace(-.55,.55,650);delta=.06;D=3
outer=1+D/2*np.abs(xx);inner=1+D/2*(np.sqrt(xx**2+delta**2)-delta)
axs[0].plot(xx,outer,'--',color=orange,label='outer local extrapolation')
axs[0].plot(xx,inner,color=blue,lw=2,label='smooth schematic profile')
axs[0].axvspan(-delta,delta,color=green,alpha=.15,label='inner region');axs[0].set(xlabel=r'$x/a$',ylabel=r'$\widetilde\psi/\widetilde\psi(0)$',title='Outer slope jump must be resolved');axs[0].legend(loc='upper center',fontsize=8)
axs[1].plot(xx,D/2*np.sign(xx),'--',color=orange,label='ideal slope jump')
axs[1].plot(xx,D/2*xx/np.sqrt(xx**2+delta**2),color=blue,lw=2,label='regularized slope')
axs[1].axvspan(-delta,delta,color=green,alpha=.15);axs[1].set(xlabel=r'$x/a$',ylabel=r'$a\widetilde\psi^\prime/\widetilde\psi(0)$',title='Matching fixes the jump, not a wall');axs[1].legend(fontsize=8)
save(fig,'tm_matching','schematic asymptotic matching; not FKR eigenfunction',{'delta_over_a':delta,'Delta_prime_a':D,'smooth_profile':'1+(D/2)(sqrt(X^2+delta^2)-delta)'})
# 4 asymptotic branches, no fabricated exact interpolation.
fig,ax=plt.subplots(figsize=(7.3,4));S=1e6;kk=np.logspace(-4,-.002,650);DD=2*(1/kk-kk)
I=2*math.pi*math.gamma(.75)/math.gamma(.25);Cg=I**(-.8)
gf=Cg*S**(-.6)*kk**.4*DD**.8;gc=S**(-1/3)*kk**(2/3)
df=Cg**.25*S**(-.4)*kk**(-.4)*DD**.2;valid=DD*df<.3
validc=DD*(S*kk)**(-1/3)>3
ax.loglog(kk,gf,'--',color=blue,alpha=.35);ax.loglog(kk,gc,'--',color=orange,alpha=.35)
ax.loglog(kk[valid],gf[valid],color=blue,lw=2.2,label='FKR: constant-flux asymptote')
ax.loglog(kk[validc],gc[validc],color=orange,lw=2.2,label='large-Delta: scaling, coefficient = 1')
ax.axvline(S**(-.25),color=green,ls=':',label=r'$ka\sim S_a^{-1/4}$')
ax.set(xlabel=r'$ka$',ylabel=r'$\gamma\tau_{Aa}$',title=r'$S_a=10^6$: separated asymptotic regimes',ylim=(1e-6,.03));ax.legend(loc='upper left',fontsize=8);ax.grid(alpha=.16,which='both')
save(fig,'tm_fkr_coppi','asymptotic formulas; dashed continuation outside a selected validity window',{'S_a':S,'C_FKR':Cg,'FKR_solid_Delta_delta_lt':.3,'Coppi_solid_Delta_delta_gt':3,'Coppi_coefficient':1})
# 5 growth-rate interpretation and a separate Rutherford illustration.
fig,axs=plt.subplots(1,2,figsize=(9.3,3.5));t=np.linspace(0,6,200)
axs[0].semilogy(t,np.exp(t),color=blue,lw=2,label=r'$\widetilde\psi/\widetilde\psi_0=e^{\gamma t}$')
axs[0].semilogy(t,np.exp(t/2),color=orange,lw=2,label=r'$W/W_0=e^{\gamma t/2}$')
axs[0].set(xlabel=r'$\gamma t$',ylabel='ratio to initial value',title='Linear eigenmode: flux versus full width');axs[0].legend(fontsize=8);axs[0].grid(alpha=.15)
tr=np.linspace(0,5,100);axs[1].plot(tr,1+tr,color=green,lw=2);axs[1].set(xlabel=r'$t/t_0$',ylabel=r'$W/W_0$',title='Rutherford stage: separate schematic');axs[1].text(.3,5,r'$W=W_0+(D_\eta\Delta^\prime/I_1)t$'+'\n'+r'$t_0=I_1 W_0/(D_\eta\Delta^\prime)$',fontsize=9);axs[1].grid(alpha=.15)
save(fig,'tm_growth_observables','analytic illustrative growth; linear and nonlinear panels are not a joined solution',{'linear_gamma_units':1,'Rutherford_constant_Delta':True})
# 6 rational surfaces and field-line helical phase.
fig,axs=plt.subplots(1,2,figsize=(9.3,3.6));rr=np.linspace(0,1,300);axs[0].plot(rr,1+2*rr**2,color=blue,lw=2)
for q,co in [(1.5,green),(2,orange)]:
 rs=np.sqrt((q-1)/2);axs[0].axhline(q,color=co,ls='--',lw=1);axs[0].axvline(rs,color=co,ls=':',lw=1);axs[0].plot(rs,q,'o',color=co);axs[0].text(rs+.025,q+.05,f'q={q:g}')
axs[0].set(xlabel=r'$r/a$',ylabel=r'$q(r)$',title=r'Teaching profile: $q=1+2(r/a)^2$')
for r,co,ls in [(1,gray,'-'),(.707,orange,'--'),(.5,green,'--')]:axs[1].add_patch(Circle((0,0),r,fill=False,color=co,ls=ls,lw=1.5))
theta=np.array([15,75,135,195,255,315])*np.pi/180;axs[1].scatter(1.08*np.cos(theta),1.08*np.sin(theta),marker='s',c=blue,s=30,label='Mirnov coil positions')
axs[1].plot([-1.2,1.2],[.1,.1],color=orange,lw=1.2,label='schematic ECE viewing chord');axs[1].text(-.4,-.05,'magnetic axis',fontsize=8);axs[1].plot(0,0,'+',color='black')
axs[1].set(aspect='equal',xlim=(-1.35,1.35),ylim=(-1.25,1.25),title='Poloidal section and complementary diagnostics');axs[1].axis('off');axs[1].legend(loc='lower center',bbox_to_anchor=(.5,-.08),fontsize=8)
save(fig,'tm_rational_diagnostics','schematic tokamak surfaces and diagnostics; not a reconstruction',{'q_profile':'1+2(r/a)^2','q_3_2_radius':.5,'q_2_1_radius':float(np.sqrt(.5))})
# 7 local pressure flattening and the bootstrap current deficit.
fig,axs=plt.subplots(2,1,figsize=(7.5,5.6),sharex=True);xx=np.linspace(-1.3,1.3,700);w=.4;g=1-np.exp(-(xx/w)**8);integ=np.cumsum(g)*(xx[1]-xx[0]);integ-=integ[len(xx)//2]
p0=2-.4*xx;p=2-.4*integ
axs[0].plot(xx,p0,'--',color=gray,label='unperturbed pressure');axs[0].plot(xx,p,color=blue,lw=2,label='flattened island pressure');axs[0].axvspan(-w,w,color=green,alpha=.1);axs[0].set(ylabel='pressure (arbitrary units)',title='Local schematic: pressure flattening reduces bootstrap current');axs[0].legend(fontsize=8)
axs[1].plot(xx,np.ones_like(xx),'--',color=gray,label='reference bootstrap current');axs[1].plot(xx,g,color=blue,lw=2,label='bootstrap current with flattening');axs[1].plot(xx,np.exp(-(xx/w)**2),color=orange,lw=2,label='localized ECCD contribution');axs[1].axvspan(-w,w,color=green,alpha=.1);axs[1].set(xlabel=r'$(r-r_s)$ (normalized)',ylabel='current (normalized)');axs[1].legend(fontsize=8)
save(fig,'tm_bootstrap','schematic pressure and current; not neoclassical transport calculation',{'island_halfwidth':w,'gradient_function':'1-exp(-(x/w)^8)','ECCD':'exp(-(x/w)^2)'})
# 8 phase fitting, illustrative pure single mode; signal is B, not pickup voltage.
fig,axs=plt.subplots(1,2,figsize=(9.3,3.6));tt=np.linspace(0,2,600)
for theta,co in [(0,blue),(np.pi/4,orange),(np.pi/2,green)]:
 axs[0].plot(tt,np.cos(2*theta-2*np.pi*tt),color=co,label=f'theta={theta/np.pi:g} pi')
axs[0].set(xlabel=r'$t f_{\rm rot}$',ylabel=r'$\delta B/B_1$',title=r'Synthetic single mode: $m=2,n=1,\zeta=0$');axs[0].legend(fontsize=8)
ang=np.linspace(0,2*np.pi,8,endpoint=False);wrapped=np.angle(np.exp(2j*ang));axs[1].plot(ang/np.pi,2*ang/np.pi,'o-',color=blue,label='unwrapped phase');axs[1].scatter(ang/np.pi,wrapped/np.pi,marker='x',s=50,c=orange,label='phase modulo 2 pi')
axs[1].set(xlabel=r'$\theta/\pi$',ylabel=r'$\varphi/\pi$',title='Mode number requires spatial phase unwrapping');axs[1].legend(fontsize=8);axs[1].grid(alpha=.15)
save(fig,'tm_mirnov_phase','synthetic magnetic signals; not experiment',{'m':2,'n':1,'toroidal_angle':0,'signal':'cos(m theta - n zeta - omega t)','coils':8})
(P/'research/figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Generated',len(manifest),'vector PDF figures')
