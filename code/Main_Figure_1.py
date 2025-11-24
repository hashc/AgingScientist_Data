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



fig = plt.figure(figsize=(18,5),facecolor='white')
#color = ['#006699','#3366CC','#3399CC','#009900','#99CC99','#CCCC66','#FF9966','#CC6633','#c45a65','#993333','black']
#color=['#134857','#1a6840','#2e317c','#0a9396','#619ac3','#e9d8a6','#ee9b00','#ca6702','#ee3f4d','#a61b29']

plt.subplot(131)
k=0
Field_Career_RefAge=fun_load_pickle('./MainData/Fig1A.pkl')
#Field_Career_RefAge['Physics']=Field_Career_RefAge['Physical Science']
for field in FieldList:
    x=range(1,41)
    y=Field_Career_RefAge[field]
    plt.plot(x,y[:,0],color=color[k],lw=linewidth,label=field)
    plt.fill_between(x,y[:,0]-y[:,1],y[:,0]+y[:,1],color=color[k],alpha=.1)

    plt.text(1,23.5-k/1,NameList[k],fontsize=16,color =color[k],ha='left') 
    k+=1
    
#plt.legend()  
plt.xlim(0,40)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.yaxis.set_major_locator(plt.MultipleLocator(5))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#ax.set_yticks([5,10,15,20])
#plt.text(35,9.2,"%.2f"%avg,fontsize=20,alpha = 1,c='gray')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Career age (years)',fontsize=label_fontsize)
plt.ylabel('Average Reference Age (years)',fontsize=label_fontsize)
plt.title('A',fontsize=title_fontsize,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=title_x_postion)
plt.ylim(8,24)

ax1=plt.axes((0.27,0.66,0.06,0.19))
Field_Career_price_fresh = fun_load_pickle('./MainData/Fig1A_insert_field.pkl')
k=0
for field in FieldList:
    x=range(1,41)
    y=Field_Career_price_fresh[field]
    plt.plot(x,y[:,0],color=color[k],lw=linewidth-2,label=field)
    plt.fill_between(x,y[:,0]-y[:,1],y[:,0]+y[:,1],color=color[k],alpha=.1)
    k+=1
    
plt.xlim(0,40)
plt.ylim(0.3,0.55)
plt.xticks([0,20,40],[0,20,40])
plt.yticks([0.3,0.4,.5],[str(i) for i in [30,40,50]])
ax1.tick_params(axis='both', which='major', labelsize=10)
ax1.xaxis.set_minor_locator(plt.MultipleLocator(10))
ax1.yaxis.set_minor_locator(plt.MultipleLocator(5))
plt.xlabel('Career age',fontsize=label_fontsize-8)
plt.ylabel('Price Index (%)',fontsize=label_fontsize-8)

#ax.set_yticks([5,10,15,20])
#plt.text(35,9.2,"%.2f"%avg,fontsize=20,alpha = 1,c='gray')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)


plt.subplot(132)
color1=['k','#66B083','#4F965E','#3B7D42']
CareerLen_RefAge=fun_load_pickle('./MainData/Fig1B.pkl')
#Field_Career_RefAge['Physics']=Field_Career_RefAge['Physical Science']
label=['Career length','10-20 years','20-30 years','$\geq$30 years']
k=0
plt.text(16,12.5,label[k],fontsize=18,color =color1[k],ha='right') 
k+=1
for cl in [10,20,30]:
    x=range(1,41)
    y=CareerLen_RefAge[cl]
    plt.plot(x,y[:,0],color=color1[k],lw=linewidth,label=label[k])
    plt.fill_between(x,y[:,0]-y[:,1],y[:,0]+y[:,1],color=color1[k],alpha=.1)
    plt.text(16,12.5-k/1.9,label[k],fontsize=16,color =color1[k],ha='right') 
    k+=1
    
#plt.legend()  
plt.xlim(0,40)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.yaxis.set_major_locator(plt.MultipleLocator(2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#ax.set_yticks([5,10,15,20])
#plt.text(35,9.2,"%.2f"%avg,fontsize=20,alpha = 1,c='gray')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Career age (years)',fontsize=label_fontsize)
plt.ylabel('Average Reference Age (years)',fontsize=label_fontsize)
plt.title('B',fontsize=title_fontsize,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=title_x_postion)
plt.ylim(6,13)

ax1=plt.axes((0.54,0.22,0.07,0.2))

color1=['#C3D8BC','#66B083','#4F965E','#3B7D42']
Cohort_Career_RefAge=fun_load_pickle('./MainData/Fig1B_insert.pkl')
#Field_Career_RefAge['Physics']=Field_Career_RefAge['Physical Science']
k=0

for year in [1990,1980,1970,1960]:
    x=range(1,41)
    y=Cohort_Career_RefAge[year]
    plt.plot(x,y[:,0],color=color1[k],lw=linewidth,label=str(year)+'s')
    plt.fill_between(x,y[:,0]-y[:,1],y[:,0]+y[:,1],color=color1[k],alpha=.1)
    plt.text(40,9.2-k/1.1,str(year)+'s',fontsize=10,color =color1[k],ha='right') 
    k+=1

plt.xlim(0,40)
plt.xticks([0,20,40],[0,20,40])
plt.ylim(6,13)
ax1.tick_params(axis='both', which='major', labelsize=15)
ax1.xaxis.set_minor_locator(plt.MultipleLocator(10))
ax1.yaxis.set_major_locator(plt.MultipleLocator(2))
plt.xlabel('Career age',fontsize=label_fontsize-5)
plt.ylabel('Reference age',fontsize=label_fontsize-5)
plt.text(1,12,'Historical\nCohorts',fontsize=label_fontsize-5)
#ax.set_yticks([5,10,15,20])
#plt.text(35,9.2,"%.2f"%avg,fontsize=20,alpha = 1,c='gray')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)


plt.subplot(133)
legend_height=.0035
def add_space(i):
    if len(str(i))==1:
        return '  '+str(i)
    else:
        return str(i)
        
Y=fun_load_pickle('./MainData/Fig1_most_ref.pkl')
plt.plot([0,0],[0,0.1],alpha=.2,lw=2)

labels=['Career length','0-10 years','10-20 years','20-30 years','30-40 years','$\geq$40 years','All Scientists']
k=0
plt.text(40,.105,labels[k],color='k',fontsize=18,ha='right')

for i in [0,10,20,30]:
    k+=1
    a,b= Y[i]
    plt.plot((b[1:]+b[:-1])/2,a/sum(a),color=plt.cm.BuGn((30-i)/100+0.5),lw=linewidth,alpha=.8,label='%s to %d Years'%(add_space(i),i+10))
    plt.text(40,.095-i/5*legend_height,labels[k],color=plt.cm.BuGn((30-i)/100+0.5),fontsize=15,ha='right')
k+=1
i=40
a,b= Y[i]
plt.plot((b[1:]+b[:-1])/2,a/sum(a),color=plt.cm.BuGn((30-i)/100+0.5),lw=linewidth,alpha=.8,label='%d Years or more'%(i))
plt.text(40,.095-i/5*legend_height,labels[k],color=plt.cm.BuGn((30-i)/100+0.5),fontsize=15,horizontalalignment ='right')

a,b= Y['all']
plt.plot((b[1:]+b[:-1])/2,a/sum(a),'--',color='k',lw=2,alpha=.6,label='All')
plt.xlim(-40,40)
plt.ylim(0,0.11)
plt.yticks([0.,0.05,0.1],[0,5,10])
i=50
plt.text(40,.095-i/5*legend_height,'All Scientists',color='k',fontsize=15,horizontalalignment ='right')

#plt.legend(frameon=False,fontsize=10)
ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
ax.yaxis.set_minor_locator(plt.MultipleLocator(0.01))
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
plt.ylabel('Share of Scientists(%)',fontsize=label_fontsize)
plt.xlabel('Most-cited reference publication\n(Years relative to career)',fontsize=label_fontsize)


plt.title('C',fontsize=title_fontsize,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=title_x_postion)


plt.subplots_adjust(hspace=.4,wspace=.3)
plt.savefig('./fig/Fig1.pdf',bbox_inches='tight')
