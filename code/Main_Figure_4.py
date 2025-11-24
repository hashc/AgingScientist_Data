from preload import *
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.proportion import proportion_confint

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
FN=dict(zip(FieldList,NameList))
FC=dict(zip(FieldList,color))
linewidth=3
ticklabel_fontsize=25
label_fontsize=20
title_fontsize=25
title_x_postion=-.15

plt.rcParams['font.family']=['Helvetica']

def np_move_avg(a,n,mode="valid"):
    return(np.convolve(a, np.ones((n,))/n, mode=mode))

window_size=3

fig=plt.figure(figsize=(18,5))



plt.subplot(131)
from statsmodels.stats.proportion import proportion_confint
df=pd.read_pickle('./MainData/fig4c.pkl')
X = sm.add_constant(df['field_age'])
y = df['older'].astype(int)

# Fit logistic regression
logit = sm.Logit(y, X).fit(disp=False)  
xg = np.linspace(df['field_age'].min(), df['field_age'].max(), 200)
Xg = sm.add_constant(xg)

# Predicted probability + 95% CI (delta method)
params = logit.params.values
cov    = logit.cov_params().values
eta    = Xg @ params                         # linear predictor
se_eta = np.sqrt(np.sum(Xg @ cov * Xg, axis=1))
z = 1.96
from scipy.special import expit
p_hat  = expit(eta)
p_low  = expit(eta - z*se_eta)
p_high = expit(eta + z*se_eta)

# Optional: binned proportions with binomial CIs (helps with overplotting)
df['_bin'] = pd.qcut(df['field_age'], q=5, duplicates='drop')
g = df.groupby('_bin')
x_bar = g['field_age'].mean()
k = g['older'].sum()
n = g['older'].count()
lo, hi = proportion_confint(k, n, alpha=0.05, method='wilson')
p_bar = k / n
ax=plt.gca()
ax.plot(xg, p_hat, lw=2, label='Logit fit',color='#5580B0')
ax.fill_between(xg, p_low, p_high, alpha=0.2, label='95% CI',color='#5580B0')

# binned proportions
ax.errorbar(x_bar, p_bar, yerr=[p_bar-lo, hi-p_bar], fmt='o', capsize=3,
            lw=1, label='Binned proportion ±95% CI', zorder=5,color='#5580B0')

ax.set_xlabel('Average career age of field',fontsize=label_fontsize)
ax.set_ylabel('Chance references getting older',fontsize=label_fontsize)
# ax.set_ylim(-0.05, 1.05)
ax.set_ylim(0.35, 0.75)
ax.set_xlim(5,9.5)
ax.set_xticks([5,6,7,8,9])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=tick_label_size)
ax.legend(frameon=False)

plt.title('A',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)


plt.subplot(132)
ax=plt.gca()
Field_Career_Crtique=fun_load_pickle('./MainData/Fig4_Field_Career_Crtique.pkl')
Field_Career_Crtique['Physics']=Field_Career_Crtique['Physical Science']
k=0
for field in ['Computer science','Social Sciences',
 'Earth & Environmental Science','Medicine',
 'Physics','Biology',
 'Engineering', 'Mathematics', 'Chemistry','Materials Science', 
]:

    x=range(41)
    y=Field_Career_Crtique[field]
    line_kws={'lw':3}
    y1,y2 =  y[:,0]-y[:,1],y[:,0]+y[:,1]
    y1,y2 = np_move_avg(np.append(y1[:window_size-1],y1),window_size),np_move_avg(np.append(y2[:window_size-1],y2),window_size)
    plt.fill_between(np.array(x),y1,y2,color=FC[field],alpha=.1)
    #plt.step(x, y[:,0], where='mid', label='mid',color=color[k],lw=2)
    y0= np_move_avg(np.append(y[:window_size-1,0],y[:,0]),window_size)
    plt.plot(x,y0,color=FC[field],lw=linewidth,label=field) 
    if k<=6:
        plt.text(0.5,0.47-k/35,FN[field],fontsize=18,color =FC[field]) 
    else:
        plt.text(22,0.32-k/35,FN[field],fontsize=18,color =FC[field]) 

    #plt.text(40,14-k/1.2,field,fontsize=15,color =color[k],ha='right') 
    k+=1
plt.xlim(0,40)
plt.ylim(0.05,.48)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.xaxis.set_major_locator(plt.MultipleLocator(10))
plt.yticks([i/100 for i in range(10,41,10)],[str(i) for i in range(10,41,10)])
ax.yaxis.set_minor_locator(plt.MultipleLocator(.01))
#ax.yaxis.set_major_locator(plt.MultipleLocator(.05))
plt.xlabel('Career age (years)',fontsize=label_fontsize)
plt.ylabel('Papers citing critically(%)',fontsize=label_fontsize)

plt.title('B',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)


ax=plt.axes((0.55,0.7,0.06,0.19))
k=0
Field_Career_Q=fun_load_pickle('./MainData/Fig4_Field_Career_Q.pkl')
for field in FieldList:
    x=range(41)
    y=Field_Career_Q[field]
    line_kws={'lw':3}
    y1,y2 =  y[:,0]-y[:,1],y[:,0]+y[:,1]
    y1,y2 = np_move_avg(np.append(y1[:window_size-1],y1),window_size),np_move_avg(np.append(y2[:window_size-1],y2),window_size)
    plt.fill_between(np.array(x),y1,y2,color=FC[field],alpha=.1)
    #plt.step(x, y[:,0], where='mid', label='mid',color=color[k],lw=2)
    y0= np_move_avg(np.append(y[:window_size-1,0],y[:,0]),window_size)
    plt.plot(x,y0,color=FC[field],lw=linewidth-2) 
    k+=1
plt.xlim(0,40)
plt.ylim(0,0.15)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize-15)
ax.xaxis.set_minor_locator(plt.MultipleLocator(10))
ax.xaxis.set_major_locator(plt.MultipleLocator(20))
plt.yticks([i/100 for i in range(0,16,5)],[str(i) for i in range(0,16,5)])
ax.yaxis.set_minor_locator(plt.MultipleLocator(.01))
# ax.yaxis.set_major_locator(plt.MultipleLocator(.05))
plt.xlabel('Career age',fontsize=label_fontsize-10)
plt.ylabel('Papers cited\ncritically(%)',fontsize=label_fontsize-10)


plt.subplot(133)

ss=5
L=pd.read_pickle('./MainData/fig4b.pkl')
T1=L[(L['year']>=1994-ss)&(L['year']<=1994+ss)
    &(L['fid']=='All')
    &(L['subfid']!='All')
    &(~(L['subfid'].isin(FieldMap.keys())))
    &(L['num']>=200)
    &(L['country'].isin(['United States','United Kingdom']))
    ]
tmp = T1.groupby(['subfid'])['fid'].count().reset_index()
tmp.columns=['subfid','numy']
T1=pd.merge(T1,tmp,on='subfid')
T1=T1[T1['numy']==ss*4+2]
print(len(set(T1['subfid'])))
model=smf.ols('refage_mean ~ T * C(year, Treatment(1994)) +C(subfid)',
          data=T1).fit()
Y=[]
X=[]
Z=[]
for a,b,c,d in zip(model.params.index,model.params.values,model.conf_int()[0],model.conf_int()[1]):
    if a.startswith('T:C(year, Treatment(1994))'):
        year = int(a.split('[')[1].strip(']').split('.')[1])
        X.append(year)
        Y.append(b)
        Z.append([c,d])
X,Y,Z=np.array(X),np.array(Y),np.array(Z)
data = pd.DataFrame({'x':X,'y':Y,'z':Z[:,0]})
plt.errorbar(X,Y,yerr=Z[:,1]-Y,color='gray',
             elinewidth=1,ecolor='gray',
             capsize=1,mew=1,fmt='o',
             mfc='darkgray',mec='gray',alpha=.8)
plt.vlines(1994,-2,5,color='gray',linestyle='--')
plt.hlines(0,1970,2020,color='gray',linestyle='--')
plt.ylim(-.6,.6)
plt.xlim(1989-.5,1999+.5)
plt.ylabel('Changes in reference age (years)',fontsize=label_fontsize)
plt.xlabel('Years',fontsize=label_fontsize)
plt.text(1994,.45,'The End of\n Mandatory Retirement',ha='center',fontsize=20)
tick_label_size=15
ax = plt.gca()
ax.tick_params(axis='both', which='major', labelsize=tick_label_size)
ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.xaxis.set_major_locator(plt.MultipleLocator(2))
#plt.text(35,9.2,"%.2f"%avg,fontsize=20,alpha = 1,c='gray')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.title('C',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)


plt.subplots_adjust(hspace=.4,wspace=.3)
if not os.path.exists('./fig'):
    os.mkdir('./fig')
    
plt.savefig('./fig/Fig4.pdf',bbox_inches='tight')
