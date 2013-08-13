# Usage : needs inputs - history_P and history_C, which are the state wise information vectors of previous period performance and #candidates the model was rolled out to, per model
# We use 5 models here, across 6 time periods, so , history_P[0]=[1.4155322812819471, 4.9723842851306213, 3.6831354714462456, 3.0345047089322521, 5.3355879766963819], reflects the performance of M1 in time period 1, M2 in time period 1.. M5 in time period 1 , as likewise for history C

#Plotting file for Aggregated performance data, per period 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
#placing anchored text within the figure
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
rc('mathtext', default='regular')

#input text
history_P=[[1.4155322812819471, 4.9723842851306213, 3.6831354714462456, 3.0345047089322521, 5.3355879766963819], [2.3240101637275856, 4.7804345245879354, 7.0829471987293973, 6.1050663075245852, 3.6087166298399973], [3.5770722538162265, 3.4516290562530587, 4.4851829512197678, 5.1158026103364733, 3.7873662329909235], [4.7137003352158136, 5.0792119756378593, 4.4624078437179504, 3.1790266221827754, 4.8711126648436895], [4.8043291762010414, 5.6979872315568576, 3.4869780377350339, 3.892755123606721, 3.8142509389863095], [4.8072846135271492, 4.2055137431209033, 5.0441056822018417, 4.1014759291893306, 5.327936039526822]]
history_C=[[14000, 14000, 14000, 14000, 14000], [5373, 18874, 13981, 11519, 20253], [6806, 14001, 20744, 17880, 10569], [12264, 11834, 15377, 17540, 12985], [14793, 15940, 14004, 9977, 15286], [15500, 18384, 11250, 12559, 12307]]

N = 5 #N = no. of models in this case
ind = np.arange(N)  # the x locations for the groups
width = 0.35

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),ha='center', va='bottom')
        
alphab = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

for k in range(0,5):
    colors=[]
    Current_Period=history_C[k]
    Next_Period = history_C[k+1]
    perform_1=history_P[k]
    perform_2=history_P[k+1]

    for i in range(0,5):
        if perform_1[i]==max(perform_1) :
            colors.append('g')
            best=i
        elif perform_1[i]==min(perform_1):
            colors.append('r')
            worst=i
        elif (perform_1[i] != min(perform_1) or perform_1[i] != max(perform_1)):
            colors.append('b')

    fig, ax = plt.subplots()
    #plt.legend(numpoints=1)
    fig.subplots_adjust(right=0.75)

    par1 = ax.twinx()
    #par2 = ax.twinx()
    make_patch_spines_invisible(par1)

    rects1 = ax.bar(ind, Current_Period, width, color=colors)
    rects2 = ax.bar(ind+width, Next_Period, width, color='c')
    lines_1=par1.plot(ind + 0.5*width, perform_1,linestyle='', marker='o', markerfacecolor ='k', markeredgewidth='1')
    lines_2=par1.plot(ind + 1.5*width, perform_2,linestyle='', marker='*',markerfacecolor ='m',markeredgewidth='1')
    ax.set_xlabel("Model #",style='italic',size='large')
    ax.set_ylabel("Candidate #",style='italic',size='large')
    par1.set_ylabel("Performance",style='italic',size='large')


    ax.set_title('Aggregated Performace Rolled out to candidates, per period',style='italic')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('M1', 'M2', 'M3', 'M4', 'M5') )
    plt.legend(numpoints=1)
    ax.annotate('Worst Performer', xy=(worst,0),  xycoords='data',xytext=(-30, 30), textcoords='offset points',size=12, va="center", ha="center",arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.2"))
    ax.annotate('Best Performer', xy=(best,0),  xycoords='data',xytext=(-30, 30), textcoords='offset points',size=12, va="center", ha="center",arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.2"))
    ax.legend((rects1[0], rects2[0],lines_1[0],lines_2[0]), ('Current time period', 'Next time Period','Current Period Performance', 'Next Period Performance'),prop=dict(size=10), numpoints=1 )

    #placing anchored text within the figure, per Period
    at = AnchoredText("Time Period :"+str(k+1),prop=dict(size=10), frameon=True,loc=2,)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    par1.set_ylim(0, 10)
    #plt.legend(numpoints=1)
    autolabel(rects1)
    autolabel(rects2)
    plt.legend()
    plt.legend(numpoints=1)
    plt.show()

