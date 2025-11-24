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
FN=dict(zip(FieldList,NameList))
FC=dict(zip(FieldList,color))

linewidth=3
ticklabel_fontsize=25
label_fontsize=20
title_fontsize=25
title_x_postion=-.15

plt.rcParams['font.family']=['Helvetica']

fig = plt.figure(figsize=(18,5),facecolor='white')
plt.subplot(131)
k=0
file='./MainData/Fig2_Field_Career_Z10_40.pkl'
tmp = fun_load_pickle(file)
for field in FieldList:
    x=range(41)
    y=tmp[field]
    line_kws={'lw':2.5}
    plt.fill_between(np.array(x),y[:,0]-y[:,1],y[:,0]+y[:,1],color=color[k],alpha=.1)
    #plt.step(x, y[:,0], where='mid', label='mid',color=color[k],lw=2)
    plt.plot(x,y[:,0],color=color[k],lw=linewidth,label=field) 
    k+=1
    
#plt.ylim(0.48,0.52)
plt.xlim(0,40)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Career age (years)',fontsize=25)
plt.ylabel('Top10% novel papers(%)',fontsize=22)
plt.title('A',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)
#plt.yticks([i/100 for i in range(0,26,5)],[str(i)+'%' for i in range(0,26,5)])
plt.yticks([i/100 for i in range(0,71,10)],[str(i) for i in range(0,71,10)])


ax1=plt.axes((0.16,0.7,0.06,0.19))

file='./MainData/Fig2_Field_Career_Word_Repeat_40.pkl'
tmp=fun_load_pickle(file)
#Field_Career_repeat['Physics']=Field_Career_repeat['Physical Science']

#color = ['#006699','#3366CC','#3399CC','#009900','#99CC99','#CCCC66','#FF9966','#CC6633','#c45a65','#993333','black']
k=0
#Field_Career_RefAge=fun_load_pickle('/Users/hachi/Data/MAG_Dec_2021_snapshot/Fig/Fig1_Field_Career_RefAge.pkl')
for field in FieldList:
    x=range(2,41)
    y=tmp[field]
    y[:,0]=1-y[:,0]
    line_kws={'lw':2.5}
    y1,y2 = y[:,0]-y[:,1],y[:,0]+y[:,1]
    y1,y2 = np_move_avg(np.append(y1[:window_size-1],y1),window_size),np_move_avg(np.append(y2[:window_size-1],y2),window_size)
    #y1,y2 = np_move_avg(np.append(y1[:window_size-1],y1),window_size),np_move_avg(np.append(y2[:window_size-1],y2),window_size)
    plt.fill_between(np.array(x),y1,y2,color=color[k],alpha=.1)
    #plt.step(x, y[:,0], where='mid', label='mid',color=color[k],lw=2)
    #y0= np_move_avg(np.append(y[:window_size-1,0],y[:,0]),window_size)
    y0= np_move_avg(np.append(y[:window_size-1,0],y[:,0]),window_size)
    plt.plot(x,y0,color=color[k],lw=1,label=field) 
    k+=1
    
#plt.legend()  
plt.ylim(0.4,0.8)
plt.xlim(0,40)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize-10)
ax.xaxis.set_minor_locator(plt.MultipleLocator(10))
#ax.yaxis.set_major_locator(plt.MultipleLocator(5))
#ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax.set_xticks([0,20,40])
ax.set_yticks([0.4,.6,.8])
plt.text(10,0.7,'Year-to-year\n'+' '*5+'semantic distance',fontsize=18,alpha = 1,c='k')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Career age',fontsize=label_fontsize-5)



plt.subplot(132)
k=0
tmp=fun_load_pickle('./MainData/Fig2_Field_Career_DisruptiveTop10_40.pkl')
for field in ['Engineering','Computer science','Materials Science', 'Social Sciences','Mathematics',
 'Earth & Environmental Science', 'Chemistry', 'Physics','Medicine','Biology',

]:
    x=range(41)
    y=tmp[field]
    line_kws={'lw':2.5}
    plt.fill_between(np.array(x),y[:,0]-y[:,1],y[:,0]+y[:,1],color=FC[field],alpha=.1)
    #plt.step(x, y[:,0], where='mid', label='mid',color=color[k],lw=2)
    plt.plot(x,y[:,0],color=FC[field],lw=linewidth,label=field) 
    if k<=7:
        plt.text(40,.55-k/24,FN[field],fontsize=18,color =FC[field],ha='right') 
    else:
        plt.text(1,.4-k/24,FN[field],fontsize=18,color =FC[field],ha='left') 
    k+=1

#plt.ylim(0.42,0.52)
plt.xlim(0,40)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Career age (years)',fontsize=25)
plt.ylabel('Top10% disruptive papers(%)',fontsize=22)
plt.title('B',fontsize=25,fontweight='heavy',
          horizontalalignment='right',verticalalignment='bottom',x=-.2)
plt.yticks([i/100 for i in range(0,51,10)],[str(i) for i in range(0,51,10)])




plt.subplot(133)
Year_Field_Country_Age=fun_load_pickle('./MainData/Year_Field_Country_Age.pkl')
countrylist = ['United States','India','China']
color=['#6E86E1','#D9AA79','#CD6574']
cmap = dict(zip(countrylist,color))
k=0
X,Y,Z=[],[],[]
year=2020
tmp2=fun_load_pickle('./MainData/Country_Disrupt_v0703_country_p.pickle')

for country in Year_Field_Country_Age:
    try:
        print(country,year,end='\r')
        tmp1 = Year_Field_Country_Age[country][country][year]
        x = sum(tmp1[:100]*np.arange(100))/sum(tmp1[:100])
        y = sum(tmp2[country])/len(tmp2[country])
        if len(tmp2[country])>=50:
            X.append(x)
            Y.append(y)
            Z.append(country)
        #plt.plot(X,Y,'.-',label=country,alpha=.6)
        if country in countrylist:
            plt.scatter(x,y,color=cmap[country],zorder=100,s=300)
            print(country)
    except:
        pass


plt.text(3,0.32,'China',zorder=100,color=cmap['China'],fontsize=25)
plt.text(7,0.35,'India',zorder=100,color=cmap['India'],fontsize=25)
plt.text(10,0.12,'USA',zorder=100,color=cmap['United States'],fontsize=25)


sns.regplot(data=pd.DataFrame({'x':X,'y':Y,'country':Z}),x='x',y='y',order=1,
            color='k',scatter_kws={'alpha':.2,'s':100})
#plt.legend(fontsize=8,frameon=False)   
plt.ylabel('Disruptive papers(%)',fontsize=label_fontsize)
plt.xlabel('Average career age (years)',fontsize=label_fontsize)
plt.ylim(0,0.5)
plt.xlim(2,12)
ax= plt.gca()
ax.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.xaxis.set_major_locator(plt.MultipleLocator(2))
ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.title('C',fontsize=title_fontsize,
          horizontalalignment='right',verticalalignment='bottom',x=title_x_postion)

plt.subplots_adjust(hspace=.4,wspace=.3)
if not os.path.exists('./fig'):
    os.mkdir('./fig')
plt.savefig('./fig/Fig2.pdf',bbox_inches='tight')