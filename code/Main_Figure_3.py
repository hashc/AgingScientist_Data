from preload import *

FieldMap={'Mathematics':[33923547],
          'Earth & Environmental Science':[127313418,205649164,39432304],
          'Social Sciences':[162324750,144024400,17744445,15744967,144133560],
          'Chemistry':[185592680],
          'Physics':[121332964],
          #'Arts & Humanities':[138885662,95457728,142362112],
          'Engineering':[127413603],
          'Materials Science':[192562407],
          'Biology':[86803240],
          'Computer science':[41008148],
          'Medicine':[71924100],
}
#color=['#2e317c','#134857','#1a6840','#2376b7','#619ac3','#0a9396','#f97d1c','#ca6702','#ee3f4d','#a61b29']
color=['#2D3074','#234755','#33674C','#6E99C1','#3D74B5','#429199','#E6DDD5','#E8843A','#DB4E5A','#9A2A2E']
FieldList=['Mathematics', 
 'Earth & Environmental Science','Social Sciences',
 'Physics','Chemistry','Materials Science', 
 'Engineering','Computer science',
'Biology','Medicine']
NameList=['Mathematics', 
 'GeoScience','Social Sciences',
'Physics','Chemistry','Materials Science', 'Engineering', 'Computer science',
'Biology','Medicine']
linewidth=3
ticklabel_fontsize=25
label_fontsize=20
title_fontsize=25
title_x_postion=-.15

plt.rcParams['font.family']=['Helvetica']


fig=plt.figure(figsize=(18,5))

fig.add_subplot(131)

x= range(60)
Y1=fun_load_pickle('./MainData/Fig3a.pkl')
Y=np.array(Y1)
plt.plot(x[1:],Y[1:,2],'-.',label='Theoretical Team',color='#1781b5',lw=3,alpha=.8)
plt.fill_between(x[1:],Y[1:,2]-Y[1:,3],Y[1:,2]+Y[1:,3],color='#1781b5',alpha=.1)

plt.plot(x[1:],Y[1:,0],label='Empirical Team',color='firebrick',alpha=.8,lw=3)
plt.fill_between(x[1:],Y[1:,0]-Y[1:,1],Y[1:,0]+Y[1:,1],color='firebrick',alpha=.1)



plt.legend(frameon=False,fontsize=15,loc=2)
plt.xlabel('Average team career age\n(years)',fontsize=label_fontsize)
plt.ylabel('Average reference age (years)',fontsize=label_fontsize)
plt.ylim(8,16)
plt.xlim(0,40)

ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
plt.title('A',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)


fig.add_subplot(132)

v='collabor_age_mean'
Field_Career_ColabAge=fun_load_pickle_no_timer('./MainData/Fig4_Field_Career%s.pkl'%v)
Field_Career_ColabAge['Physics']=Field_Career_ColabAge['Physical Science']
k=0
for field in FieldMap:
    x=range(1,41)
    y=Field_Career_ColabAge[field]
    plt.plot(x,y[:,0],color=color[k],lw=2.5,label=field)
    plt.fill_between(x,y[:,0]-y[:,1],y[:,0]+y[:,1],color=color[k],alpha=.1)
    plt.text(0.5,39.5-k*2.5,NameList[k],fontsize=16,color =color[k]) 
    k+=1  
#plt.legend()  
plt.ylim(0,40)
plt.xlim(0,40)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=20)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.yaxis.set_major_locator(plt.MultipleLocator(5))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#ax.set_yticks([5,10,15,20])
#plt.text(35,9.2,"%.2f"%avg,fontsize=20,alpha = 1,c='gray')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Career age (years)',fontsize=25)
plt.ylabel('Average coauthor career age (years)',fontsize=20)
plt.title('B',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)
ax=plt.axes((0.55,0.65,0.06,0.19))
Field_TeamAge_Year=fun_load_pickle('./MainData/Fig4_Field_TeamAge_Year.pkl')
x= range(1900,2023)
k=0
for field in FieldList:
    y=np.array([Field_TeamAge_Year[year][field] for year in x])
    plt.plot(x,y[:,1],color=color[k],lw=linewidth-1.5) 
    plt.fill_between(x,y[:,1]-1.96*y[:,3]/y[:,4]**.5,y[:,1]+1.96*y[:,3]/y[:,4]**.5,color=color[k],alpha=.1) 
    k+=1
plt.xlim(1960,2020)
ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize-10)
plt.xticks([1960,1990,2020])
plt.yticks([0,10,20,30])
plt.xlabel('Year',fontsize=label_fontsize-5) 
plt.ylabel('Oldest team member\ncareer age',fontsize=label_fontsize-7) 
plt.ylim(0,30)



fig.add_subplot(133)
from scipy import stats
def mean_ci_95(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = x.size
    m = x.mean()
    if n <= 1:
        return m, 0.0
    se = x.std(ddof=1) / np.sqrt(n)
    tcrit = stats.t.ppf(0.975, n-1)  # 95% CI
    return m, tcrit * se
series = fun_load_pickle('./MainData/fig3c.pkl')
#series = [df_merge['deltarefage'], Younger,Older,df_split['deltarefage']]

labels = ["Merge","Younger","Older","Split"]

means, yerr = [], []
for s in series:
    m, ci = mean_ci_95(s)
    means.append(m)
    yerr.append(ci)

x = [0,1,2,3]
ax = plt.gca()
bars =ax.bar(x, means, yerr=yerr, capsize=3.5,width=0.4,ecolor='black')
# colors = ['#599CB4',"#CCE4EF",'#E69191', "#C25759"]# ]
colors = ['#4F845C',"#CFE7C4",'#FBDFE2', "#B83945"]# ]
hatches = [None, None, None, None]
for bar, color, hatch in zip(bars, colors, hatches):
    bar.set_facecolor(color)
    # bar.set_edgecolor('black')
    if hatch:
        bar.set_hatch(hatch)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(-1.1,0.6)
ax.set_yticks([-1.0,-0.5,0,0.5])
ax.set_yticklabels([-1.0,-0.5,0,0.5])
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize-5)
ax.set_ylabel("Change in reference age (years)",fontsize=label_fontsize)
ax.set_xlabel("Same-team paper pairs",fontsize=label_fontsize)
ax.axhline(0,ls ='--',color='black')


# ax.set_title("Pair of Papers in Different Years")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Optional: show sample sizes above bars
ns = [np.sum(~np.isnan(np.asarray(s, float))) for s in series]
# ax.bar_label(bars, labels=[f"n={n}" for n in ns], padding=3)

plt.title('C',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)

plt.subplots_adjust(hspace=.4,wspace=.3)

if not os.path.exists('./fig'):
    os.mkdir('./fig')
plt.savefig('./fig/Fig3.pdf',bbox_inches='tight')