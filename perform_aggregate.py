

#### Performance Aggregator Platform###

from numpy import mean, sqrt, arange
from itertools import chain
import random
#from __future__ import division
import numpy as np
import time
#time.sleep(5)


def display_function(time_value,history_P):
    width=10
    C=[]
    S=[]
    P=[]
    threshold=[]
    if time_value ==1:
        print "Prototype of the Real Time Batch Aggregator"
        history_P=[]
        for i in range(0,5):
            temp=int(TotPop/5)
            C.append(temp)
    elif time_value>1 :
        C=scaling_performance(history_P,time_value)
    for i in range(0,5):
        S_temp=generate_scores(C[i])
        S.append(S_temp)
        threshold_temp=threshold_scores(S[i])
        threshold.append(threshold_temp)
        # Now that you have Candidate Population, Call scores, thresholds & finally call performance metric execpt Acceleration scores
    (full_on_normalize_temp, history_X , history_Y,perform_metric)=perform(S,C,threshold,time_value)
    # currently doing a pure sum of all the metrics in  the normalized perform_metric
    for i in range(0,5):
        temp_sum=0
    #kth variable, ith model
        for k in range(0,9):
            temp_sum=temp_sum+full_on_normalize_temp[k][i]
        P.append(temp_sum)
    #pass scores and call this
    print "***********************************************************************************************************************************************************************"
    print "***********************************************************************************************************************************************************************"
    print "%s ######################Time %d ###################### %s " %(''.rjust(50),time_value,''.rjust(50))
    print ' %s | %s | %s |Mean Sq.| Mean | Variance | Precision| Accuracy| Velocity(V) |Velocity(C) |Acceleration(V) |Acceleration(C)' %('Model#','Time'.rjust(3),'#Candidates'.rjust(width))
    print ' %s Error %s (Score)%s (Score) %s (visit) %s(chats) %s(Visit) %s(chats) \n' %(''.rjust(30),''.rjust(0),''.rjust(1),''.rjust(25),''.rjust(5),''.rjust(5),''.rjust(10))
    for i in range(0,5):
        print 'Model# %d| %s | %s %s %s | %f | %f | %f | %f | %f | %f | %f | %f | %f \n' % (i+1,str(time_value).rjust(3),''.rjust(1),str(C[i]).rjust(8),''.rjust(1), perform_metric[i][0],perform_metric[i][1],perform_metric[i][2],perform_metric[i][3],perform_metric[i][4],perform_metric[i][5],perform_metric[i][6],perform_metric[i][7],perform_metric[i][8])
    print " %s #####################PERFORMANCE AGGREGATED METRIC ############################ %s" %(''.rjust(50),''.rjust(50))
    print '  %s %s %s %s %s | %s ' %('Model#','|'.rjust(1),'Time'.rjust(7),'|'.rjust(4),'#Candidates'.rjust(width),'Performance Metric'.rjust(20))
    print "%s \n" %('(Aggregated & Normalized)'.rjust(60))
    for i in range(0,5):
        print 'Model# %d | %s %s %s %s %s \n' % (i+1,str(time_value).rjust(5),'|'.rjust(5),str(C[i]).rjust(9),'|'.rjust(5),str(P[i]).rjust(5))
        #storing histories  before moving to next period
    history_C.append(C)
    history_S.append(S)
    history_P.append(P)
    return C,P,history_P,history_C,history_S

def generate_scores(C):
    S=[]
    for i in range(0,C):
        S.append(random.random())
    return S
	
def threshold_scores(S):
    threshold=np.percentile(S,40)
    return threshold

def scaling_performance(history_P,time_value):
    P=[]
    C=[]
    #scale performance & define next period candidate groups
    for i in range(0,5):
        PX=history_P[time_value-2][i]/sum(history_P[time_value-2])
     #   print PX
        P.append(PX)
        C_len=int(round(PX*TotPop)) #length of Candidate pop
        if i<4:
            C.append(C_len)
        elif i==4:
            C.append(TotPop-sum(C))
    #print C
    return C

    
#now define & call the performance functions

def mean_square_error(S):
    temp=0
    for i in range(0, len(S)):
        temp=(S[i]**2)+temp
    return sqrt(temp)
        
def velocity_metric(C):
    Y=random.randint(1,10)*1.5
    X=random.randint(1,10)*2
    TotVisit=C
    TotConvert=(TotVisit*Y)/100
    TotInteractive=(TotVisit*X)/100
    #re-draw till total interactive chats > total conversion(realistic estimate)
    while TotVisit ==0 or TotInteractive ==0:
        while X<Y:
            Y=random.randint(1,10)*1.5
            X=random.randint(1,10)*2
        TotConvert=(TotVisit*Y)/100
        TotInteractive=(TotVisit*X)/100
    velocity_visit= TotConvert/TotVisit
    velocity_chats=TotConvert/TotInteractive
    return velocity_visit, velocity_chats , X, Y

#Time should be a global var - in the 1st pass, acceleration is NA

def acceleration_metric(history_C,history_Y,C,X,Y,time_value):
    TotVisit=C
    TotVisit_lastPeriod=history_C[time_value-2]
    TotConvert=(TotVisit*Y)/100
    TotConvert_lastPeriod=(TotVisit*history_Y[time_value-2])/100
    TotInteractive=(TotVisit*X)/100
    TotInteractive_lastPeriod=(TotVisit*history_Y[time_value-2])/100
    if (TotVisit-TotVisit_lastPeriod) != 0:
        acceleration_visit= (TotConvert-TotConvert_lastPeriod)/(TotVisit-TotVisit_lastPeriod)
    elif(TotVisit-TotVisit_lastPeriod) ==0 :
        acceleration_visit=0
    if (TotInteractive-TotInteractive_lastPeriod) !=0 :
        acceleration_chats=(TotConvert-TotConvert_lastPeriod)/(TotInteractive-TotInteractive_lastPeriod)
    elif  (TotInteractive-TotInteractive_lastPeriod) ==0 :
        acceleration_chats=0
    #print acceleration_visit, acceleration_chats
    return acceleration_visit, acceleration_chats

 
def precision_accuracy(S,threshold,C,Y):
    all_list=[]
    TP=0
    FP=0
    FN=0
    TN=0
    TotVisit=C
    #TotConvert, TotNonConvert
    TotConvert=int((TotVisit*Y)/100)
    TotNonConvert=TotVisit-TotConvert
    TotConvert_list=TotConvert*[1]
    TotNonConvert_list=TotNonConvert*[0]
    all_list=[TotNonConvert_list,TotConvert_list]
    FN=int((random.randint(10,15)*TotConvert)/100)
    TP=TotConvert-FN
    FP=int((random.randint(30,70)*TotNonConvert)/100)
    #unchain this first
    """all_list=list(chain.from_iterable(all_list))
    random.shuffle(all_list) #all_listis now shuffled
    for i in range(0,len(S)):
        if S[i] >threshold and all_list[i]==1 :# TP
            TP=TP+1
        elif S[i] >threshold and all_list[i]==0 : # FP
            FP=FP+1
        elif S[i] <threshold and all_list[i]==1 :# FN
            FN=FN+1"""
    TN=(TotNonConvert+TotConvert)-(TP+FP+FN)
    if (TP+FP) !=0:
        precision= float(TP)/float(TP+FP)
    elif (TP+FP) ==0:
        precision=0
    if C!=0 :
        accuracy=float((TP+TN))/float((TotNonConvert+TotConvert))
    elif C==0 :
        accuracy=0
    return precision,accuracy
    
def perform(S,C,threshold,time_value) :
    perform_metric=[]
    full_on_normalize_temp=[]
    #print len(C[0])
    if time_value ==1 :
        for i in range(0,5):
            mean_sq=mean_square_error(S[i])
            (velocity_visit, velocity_chats, X, Y)= velocity_metric(C[i])
        #initialize history_ before this for acceleration function
            (acceleration_visit, acceleration_chats)= (0, 0)
            #"1st Period, hence Acceleration scores NA" , "1st Period, hence Acceleration scores NA"
            (precision, accuracy)=precision_accuracy(S[i],threshold[i],C[i],Y)
            mean_score=mean(S[i])
            variance_score=sum((mean_score - element) ** 2 for element in S[i]) / len(S[i])
            temp_perform_metric=[mean_sq,mean_score,variance_score,precision,accuracy,velocity_visit,velocity_chats,acceleration_visit, acceleration_chats]
            perform_metric.append(temp_perform_metric)
            #normalizing the scores now
        full_on_normalize_temp=normalize(perform_metric)
    elif time_value >1 :
        for i in range(0,5):
            mean_sq=mean_square_error(S[i])
            (velocity_visit, velocity_chats, X, Y)= velocity_metric(C[i])
            #initialize history_ before this for acceleration function
            (acceleration_visit, acceleration_chats)=acceleration_metric(history_C[time_value-2],history_Y,C[i],X,Y,time_value)
            (precision, accuracy)=precision_accuracy(S[i],threshold[i],C[i],Y)
            mean_score=mean(S[i])
            variance_score=sum((mean_score - element) ** 2 for element in S[i]) / len(S[i])
            temp_perform_metric=[mean_sq,mean_score,variance_score,precision,accuracy,velocity_visit,velocity_chats,acceleration_visit, acceleration_chats]
            perform_metric.append(temp_perform_metric)
            #normalize the metric now
        full_on_normalize_temp=normalize(perform_metric)
    history_X.append(X)
    history_Y.append(Y)
    return full_on_normalize_temp , history_X , history_Y,perform_metric

def normalize(perform_metric):
    normalize=[]
    normalize_temp=[]
#normalize_full=[]
    sub_array=[]
#list_subs=[]
    full_on_sub_array=[]
    full_on_normalize_temp=[]
    for k in range(0,9):
        sub_array=[]
        normalize_temp=[]
        for i in range(0,5):
            sub_array.append(perform_metric[0:5][i][k])
        #print" T %d " %(t)
        for i in range(0,5):
            if (max(sub_array)-min(sub_array))!=0:
                normalize_temp.append((sub_array[i]-min(sub_array))/(max(sub_array)-min(sub_array)))
            elif (max(sub_array)-min(sub_array))==0:
                normalize_temp.append(0)
        full_on_sub_array.append(sub_array)
        full_on_normalize_temp.append(normalize_temp)
    return full_on_normalize_temp

#initialization conditions
history_X=[]
history_Y=[]
history_C=[]
history_S=[]
history_P=[]

time_x =[1,2,3,4,5,6]
TotPop=70000
for time_value in time_x:
    if time_value ==1:
        (C,P,history_P,history_C,history_S)=display_function(time_value,history_P)
    elif time_value >1 :
        (C,P,history_P,history_C,history_S)=display_function(time_value,history_P)
    print " ***********************************************************************"
    print " delta t - Waiting to Aggregate,Process & Roll the next period decisions"
    print " ***********************************************************************"
time.sleep(5)
#inserted a sleep time on purpose, to be able to validate performance each period

    



