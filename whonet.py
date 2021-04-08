# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 22:03:11 2019

@author: onyekpeu
"""
#Best
import numpy as np

from function_files import *
from IO_VNB_Dataset import *

'Parameters'



new_opt_runshr=np.zeros((4,len(par)))
new_opt_runsra=np.zeros((8,len(par)))

new_opt_runscia=np.zeros((8,len(par)))
new_opt_runshb=np.zeros((8,len(par)))

new_opt_runsslr=np.zeros((12,len(par)))
new_opt_runswr=np.zeros((12,len(par)))

new_opt_runs030=np.zeros((36,len(par)))
new_opt_runs060=np.zeros((36,len(par)))
new_opt_runs120=np.zeros((36,len(par)))
new_opt_runs180=np.zeros((36,len(par)))



dropout=0.05

input_dim = 4*10
output_dim = 1
num_epochs = 80
layer_dim = 1
learning_rate = 0.0007
batch_size =128
test_split =0
decay_rate=0
decay_steps=10000
momentum=0.8
samplefreq=10
Ts=int(samplefreq*1*1)
seq_dim=int(1*(10/Ts))
seq_dim_=int(seq_dim*Ts)
avg=1
l1_=0
l2_=0
h2 = 72
Z=1
outage1=100
outage2=300
outage3=600
outage4=900
outage5=1200
outage6=1800
number_of_runs=1
splitvalue=0.30# from 5% to 30%
mode='RNN'

  
#############################################################################
#############################################################################
#############################################################################
'Dataloading and indexing'
#############################################################################
#############################################################################
#############################################################################

TrainDat=[V_S1[:1380], V_S1[1580:], V_S3a, V_S2[:19640], V_S2[21360:52960], V_S2[53580:], V_Y1, V_Y2[:481], V_Y2[508:1417],V_Y2[1438:1950],V_Y2[1989:2164],V_Y2[2198:2368],
          V_Y2[2468:2779],V_Y2[2790:], V_St1[:1885], V_St1[1989:2335], V_St1[2482:],
          V_M[:2491], V_M[2511:2734], V_M[2742:], V_S4[:4741], V_S4[4856:], V_S3c[:1260],
           V_S3c[1426:1623], V_S3c[1647:], V_St6, V_Vw16a, V_Vta2, V_Vta1a, V_Vw5, V_Vta8,
          V_Vta10, V_Vta9, V_Vta13, V_Vta16, V_Vta17, V_Vta20, V_Vta21, V_Vta22, V_Vta27, V_Vta28, V_Vta29[:800], V_Vta29[1080:6780],
          V_Vta29[7220:], V_Vta30[:12900], V_Vta30[13180:], V_Vtb1, V_Vtb2, V_Vtb3, V_Vtb5[:1255], V_Vtb5[1267:3720], V_Vtb5[4160:4380], V_Vtb5[4860:6760], 
          V_Vtb5[7220:], V_Vtb9, V_Vw4[:4900], V_Vw4[5760:6220], V_Vw4[7420:33340], V_Vw4[33460:80660], V_Vw4[81000:116180], V_Vw4[117160:], V_Vw14b, V_Vw14c[:14060], V_Vw14c[15600:],
          V_Vfa01, V_Vfa02[:59860], V_Vfa02[59860:], V_Vfb01a[:1520], V_Vfb01a[1980:5360], V_Vfb01a[5740:9360], V_Vfb01a[11660:], V_Vfb01b, V_Vfb02b]
'''Bias Estimation'''
Acc1_bias, Acc2_bias, gyro1_bias, Brkpr_bias=calib1(Bias)


'''Testset'''
#Challenging Scenarios
RAdat1=[V_Vta11]
RAdat2=[V_Vfb02d]

#Quick changes in acceleration scenario
CIAdat1=[V_Vfb02e]
CIAdat2=[V_Vta12]

#Hard brake scenario
HBdat1=[V_Vw16b]
HBdat2=[V_Vw17]

#Sharp cornering and successive left and right scenario
SLRdat1=[V_Vw6]
SLRdat2=[V_Vw8]
SLRdat3=[V_Vw7]  

#Motorway scenario
HRdat=[V_Vw12]

#wet toad scenario
WRdat1=[V_Vtb8]
WRdat2=[V_Vtb11]
WRdat3=[V_Vtb13]

#Longer term Outages
AGdat1=[V_Vtb3]
AGdat2=[V_Vfb01c]
AGdat3=[V_Vfb02a]
AGdat4=[V_Vta1a] 
AGdat5=[V_Vfb02b]
AGdat6=[V_Vfb02g]
DFdat1=[V_St6]
DFdat2=[V_St7[:17000]]
DFdat3=[V_S3a]

amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn= maxmin17(V_Vw12,Ts, Acc1_bias, gyro1_bias)

'''Data processing for training'''
gtr,itr,x, y=data_process13t(TrainDat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)

'''Data processing for evaluation'''
#Motorway Scenario
gthr,ithr,xthr, ythr=data_process13t(HRdat, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
#Roundabout Scenario    
gtra1,itra1,xtra1, ytra1=data_process13t(RAdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtra2,itra2,xtra2, ytra2=data_process13t(RAdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode,)
#Hard brake Scenario
gthb1,ithb1,xthb1, ythb1=data_process13t(HBdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn,Z, mode) 
gthb2,ithb2,xthb2, ythb2=data_process13t(HBdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn,Z, mode)  
#Quick changes in acceleration Scenario
gtcia1,itcia1,xtcia1, ytcia1=data_process13t(CIAdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode) 
gtcia2,itcia2,xtcia2, ytcia2=data_process13t(CIAdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)       
#Sharp cornering and successive left and right turns Scenario
gtslr1,itslr1,xtslr1, ytslr1=data_process13t(SLRdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)           
gtslr2,itslr2,xtslr2, ytslr2=data_process13t(SLRdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)  
gtslr3,itslr3,xtslr3, ytslr3=data_process13t(SLRdat3, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)       
#Wet Road Scenario
gtwr1,itwr1,xtwr1, ytwr1=data_process13t(WRdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)      
gtwr2,itwr2,xtwr2, ytwr2=data_process13t(WRdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode) 
gtwr3,itwr3,xtwr3, ytwr3=data_process13t(WRdat3, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode) 
 #Longer-term GNSS Outages Scenario   
gtag1,itag1,xtag1, ytag1=data_process13t(AGdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtag2,itag2,xtag2, ytag2=data_process13t(AGdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtag3,itag3,xtag3, ytag3=data_process13t(AGdat3, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtag4,itag4,xtag4, ytag4=data_process13t(AGdat4, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtag5,itag5,xtag5, ytag5=data_process13t(AGdat5, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtag6,itag6,xtag6, ytag6=data_process13t(AGdat6, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtdf1,itdf1,xtdf1, ytdf1=data_process13t(DFdat1, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtdf2,itdf2,xtdf2, ytdf2=data_process13t(DFdat2, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)
gtdf3,itdf3,xtdf3, ytdf3=data_process13t(DFdat3, seq_dim, input_dim, output_dim, Ts, Acc1_bias, Acc2_bias, gyro1_bias, batch_size, amx, amn, dimx, dimn, dgmx, dgmn, gymx, gymn, Z, mode)



'array creation to store maximum NN model CTE for each scenario after each full training'   
cte_runshrNN=np.zeros((int(number_of_runs),4))
cte_runsra_1NN=np.zeros((int(number_of_runs),4))
cte_runsra_2NN=np.zeros((int(number_of_runs),4))
cte_runscia_1NN=np.zeros((int(number_of_runs),4))
cte_runscia_2NN=np.zeros((int(number_of_runs),4))
cte_runshb_1NN=np.zeros((int(number_of_runs),4))
cte_runshb_2NN=np.zeros((int(number_of_runs),4))        
cte_runsslr_1NN=np.zeros((int(number_of_runs),4)) 
cte_runsslr_2NN=np.zeros((int(number_of_runs),4))     
cte_runsslr_3NN=np.zeros((int(number_of_runs),4)) 
cte_runswr_1NN=np.zeros((int(number_of_runs),4))
cte_runswr_2NN=np.zeros((int(number_of_runs),4))    
cte_runswr_3NN=np.zeros((int(number_of_runs),4))    
cte_runsag30_1NN=np.zeros((int(number_of_runs),4)) 
cte_runsag30_2NN=np.zeros((int(number_of_runs),4)) 
cte_runsag30_3NN=np.zeros((int(number_of_runs),4)) 
cte_runsag30_4NN=np.zeros((int(number_of_runs),4)) 
cte_runsag30_5NN=np.zeros((int(number_of_runs),4))     
cte_runsag30_6NN=np.zeros((int(number_of_runs),4)) 

cte_runsag60_1NN=np.zeros((int(number_of_runs),4)) 
cte_runsag60_2NN=np.zeros((int(number_of_runs),4))
cte_runsag60_3NN=np.zeros((int(number_of_runs),4))
cte_runsag60_4NN=np.zeros((int(number_of_runs),4))
cte_runsag60_5NN=np.zeros((int(number_of_runs),4))    
cte_runsag60_6NN=np.zeros((int(number_of_runs),4))  

cte_runsag120_1NN=np.zeros((int(number_of_runs),4)) 
cte_runsag120_2NN=np.zeros((int(number_of_runs),4)) 
cte_runsag120_3NN=np.zeros((int(number_of_runs),4)) 
cte_runsag120_4NN=np.zeros((int(number_of_runs),4)) 
cte_runsag120_5NN=np.zeros((int(number_of_runs),4))     
cte_runsag120_6NN=np.zeros((int(number_of_runs),4)) 

cte_runsag180_1NN=np.zeros((int(number_of_runs),4)) 
cte_runsag180_2NN=np.zeros((int(number_of_runs),4)) 
cte_runsag180_3NN=np.zeros((int(number_of_runs),4)) 
cte_runsag180_4NN=np.zeros((int(number_of_runs),4)) 
cte_runsag180_5NN=np.zeros((int(number_of_runs),4))     
cte_runsag180_6NN=np.zeros((int(number_of_runs),4))

    
cte_runsdf30_1NN=np.zeros((int(number_of_runs),4))
cte_runsdf30_2NN=np.zeros((int(number_of_runs),4))
cte_runsdf30_3NN=np.zeros((int(number_of_runs),4))

cte_runsdf60_1NN=np.zeros((int(number_of_runs),4))
cte_runsdf60_2NN=np.zeros((int(number_of_runs),4))
cte_runsdf60_3NN=np.zeros((int(number_of_runs),4))

cte_runsdf120_1NN=np.zeros((int(number_of_runs),4))
cte_runsdf120_2NN=np.zeros((int(number_of_runs),4))
cte_runsdf120_3NN=np.zeros((int(number_of_runs),4))

cte_runsdf180_1NN=np.zeros((int(number_of_runs),4))
cte_runsdf180_2NN=np.zeros((int(number_of_runs),4))
cte_runsdf180_3NN=np.zeros((int(number_of_runs),4))

    
'array creation to store maximum INS physical model CTE for each scenario after each full training'
cte_runshrINS_DR=np.zeros((int(number_of_runs),4))

cte_runsra_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsra_2INS_DR=np.zeros((int(number_of_runs),4))

cte_runscia_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runscia_2INS_DR=np.zeros((int(number_of_runs),4))    

cte_runshb_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runshb_2INS_DR=np.zeros((int(number_of_runs),4))

cte_runsslr_1INS_DR=np.zeros((int(number_of_runs),4)) 
cte_runsslr_2INS_DR=np.zeros((int(number_of_runs),4)) 
cte_runsslr_3INS_DR=np.zeros((int(number_of_runs),4)) 

cte_runswr_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runswr_2INS_DR=np.zeros((int(number_of_runs),4))
cte_runswr_3INS_DR=np.zeros((int(number_of_runs),4))
    
cte_runsag30_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag30_2INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag30_3INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag30_4INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag30_5INS_DR=np.zeros((int(number_of_runs),4))    
cte_runsag30_6INS_DR=np.zeros((int(number_of_runs),4))

cte_runsag60_1INS_DR=np.zeros((int(number_of_runs),4))  
cte_runsag60_2INS_DR=np.zeros((int(number_of_runs),4)) 
cte_runsag60_3INS_DR=np.zeros((int(number_of_runs),4)) 
cte_runsag60_4INS_DR=np.zeros((int(number_of_runs),4)) 
cte_runsag60_5INS_DR=np.zeros((int(number_of_runs),4)) 
cte_runsag60_6INS_DR=np.zeros((int(number_of_runs),4)) 

cte_runsag120_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag120_2INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag120_3INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag120_4INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag120_5INS_DR=np.zeros((int(number_of_runs),4))    
cte_runsag120_6INS_DR=np.zeros((int(number_of_runs),4))
   
cte_runsag180_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag180_2INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag180_3INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag180_4INS_DR=np.zeros((int(number_of_runs),4))
cte_runsag180_5INS_DR=np.zeros((int(number_of_runs),4))    
cte_runsag180_6INS_DR=np.zeros((int(number_of_runs),4))

cte_runsdf30_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsdf30_2INS_DR=np.zeros((int(number_of_runs),4))        
cte_runsdf30_3INS_DR=np.zeros((int(number_of_runs),4))  

cte_runsdf60_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsdf60_2INS_DR=np.zeros((int(number_of_runs),4))    
cte_runsdf60_3INS_DR=np.zeros((int(number_of_runs),4)) 

cte_runsdf120_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsdf120_2INS_DR=np.zeros((int(number_of_runs),4))
cte_runsdf120_3INS_DR=np.zeros((int(number_of_runs),4))

cte_runsdf180_1INS_DR=np.zeros((int(number_of_runs),4))
cte_runsdf180_2INS_DR=np.zeros((int(number_of_runs),4))
cte_runsdf180_3INS_DR=np.zeros((int(number_of_runs),4))

'array creation to store maximum NN model CRSE for each scenario after each full training'
           
crse_runshrNN=np.zeros((int(number_of_runs),4))
crse_runsra_1NN=np.zeros((int(number_of_runs),4))
crse_runsra_2NN=np.zeros((int(number_of_runs),4))
crse_runscia_1NN=np.zeros((int(number_of_runs),4))
crse_runscia_2NN=np.zeros((int(number_of_runs),4))
crse_runshb_1NN=np.zeros((int(number_of_runs),4))
crse_runshb_2NN=np.zeros((int(number_of_runs),4))        
crse_runsslr_1NN=np.zeros((int(number_of_runs),4)) 
crse_runsslr_2NN=np.zeros((int(number_of_runs),4))     
crse_runsslr_3NN=np.zeros((int(number_of_runs),4)) 
crse_runswr_1NN=np.zeros((int(number_of_runs),4))
crse_runswr_2NN=np.zeros((int(number_of_runs),4))    
crse_runswr_3NN=np.zeros((int(number_of_runs),4))    
crse_runsag30_1NN=np.zeros((int(number_of_runs),4)) 
crse_runsag30_2NN=np.zeros((int(number_of_runs),4)) 
crse_runsag30_3NN=np.zeros((int(number_of_runs),4)) 
crse_runsag30_4NN=np.zeros((int(number_of_runs),4)) 
crse_runsag30_5NN=np.zeros((int(number_of_runs),4))     
crse_runsag30_6NN=np.zeros((int(number_of_runs),4))   
   
crse_runsag60_1NN=np.zeros((int(number_of_runs),4)) 
crse_runsag60_2NN=np.zeros((int(number_of_runs),4))
crse_runsag60_3NN=np.zeros((int(number_of_runs),4))
crse_runsag60_4NN=np.zeros((int(number_of_runs),4))
crse_runsag60_5NN=np.zeros((int(number_of_runs),4))    
crse_runsag60_6NN=np.zeros((int(number_of_runs),4))  

crse_runsag120_1NN=np.zeros((int(number_of_runs),4)) 
crse_runsag120_2NN=np.zeros((int(number_of_runs),4)) 
crse_runsag120_3NN=np.zeros((int(number_of_runs),4)) 
crse_runsag120_4NN=np.zeros((int(number_of_runs),4)) 
crse_runsag120_5NN=np.zeros((int(number_of_runs),4))     
crse_runsag120_6NN=np.zeros((int(number_of_runs),4)) 

crse_runsag180_1NN=np.zeros((int(number_of_runs),4)) 
crse_runsag180_2NN=np.zeros((int(number_of_runs),4)) 
crse_runsag180_3NN=np.zeros((int(number_of_runs),4)) 
crse_runsag180_4NN=np.zeros((int(number_of_runs),4)) 
crse_runsag180_5NN=np.zeros((int(number_of_runs),4))     
crse_runsag180_6NN=np.zeros((int(number_of_runs),4))

crse_runsdf30_1NN=np.zeros((int(number_of_runs),4))
crse_runsdf30_2NN=np.zeros((int(number_of_runs),4))
crse_runsdf30_3NN=np.zeros((int(number_of_runs),4))

crse_runsdf60_1NN=np.zeros((int(number_of_runs),4))
crse_runsdf60_2NN=np.zeros((int(number_of_runs),4))
crse_runsdf60_3NN=np.zeros((int(number_of_runs),4))

crse_runsdf120_1NN=np.zeros((int(number_of_runs),4))
crse_runsdf120_2NN=np.zeros((int(number_of_runs),4))
crse_runsdf120_3NN=np.zeros((int(number_of_runs),4))

crse_runsdf180_1NN=np.zeros((int(number_of_runs),4))
crse_runsdf180_2NN=np.zeros((int(number_of_runs),4))
crse_runsdf180_3NN=np.zeros((int(number_of_runs),4))   

'array creation to store  maximum INS physical model CRSE for each scenario after each full training. '
crse_runshrINS_DR=np.zeros((int(number_of_runs),4))

crse_runsra_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsra_2INS_DR=np.zeros((int(number_of_runs),4))

crse_runscia_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runscia_2INS_DR=np.zeros((int(number_of_runs),4))    

crse_runshb_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runshb_2INS_DR=np.zeros((int(number_of_runs),4))

crse_runsslr_1INS_DR=np.zeros((int(number_of_runs),4)) 
crse_runsslr_2INS_DR=np.zeros((int(number_of_runs),4)) 
crse_runsslr_3INS_DR=np.zeros((int(number_of_runs),4)) 

crse_runswr_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runswr_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runswr_3INS_DR=np.zeros((int(number_of_runs),4))

crse_runsag30_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag30_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag30_3INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag30_4INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag30_5INS_DR=np.zeros((int(number_of_runs),4))    
crse_runsag30_6INS_DR=np.zeros((int(number_of_runs),4))

crse_runsag60_1INS_DR=np.zeros((int(number_of_runs),4))  
crse_runsag60_2INS_DR=np.zeros((int(number_of_runs),4)) 
crse_runsag60_3INS_DR=np.zeros((int(number_of_runs),4)) 
crse_runsag60_4INS_DR=np.zeros((int(number_of_runs),4)) 
crse_runsag60_5INS_DR=np.zeros((int(number_of_runs),4)) 
crse_runsag60_6INS_DR=np.zeros((int(number_of_runs),4)) 

crse_runsag90_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag90_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag90_3INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag90_4INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag90_5INS_DR=np.zeros((int(number_of_runs),4))    
crse_runsag90_6INS_DR=np.zeros((int(number_of_runs),4))

crse_runsag120_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag120_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag120_3INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag120_4INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag120_5INS_DR=np.zeros((int(number_of_runs),4))    
crse_runsag120_6INS_DR=np.zeros((int(number_of_runs),4))

crse_runsag180_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag180_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag180_3INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag180_4INS_DR=np.zeros((int(number_of_runs),4))
crse_runsag180_5INS_DR=np.zeros((int(number_of_runs),4))    
crse_runsag180_6INS_DR=np.zeros((int(number_of_runs),4))

crse_runsdf30_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf30_2INS_DR=np.zeros((int(number_of_runs),4))        
crse_runsdf30_3INS_DR=np.zeros((int(number_of_runs),4))  

crse_runsdf60_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf60_2INS_DR=np.zeros((int(number_of_runs),4))    
crse_runsdf60_3INS_DR=np.zeros((int(number_of_runs),4)) 

crse_runsdf90_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf90_2INS_DR=np.zeros((int(number_of_runs),4))    
crse_runsdf90_3INS_DR=np.zeros((int(number_of_runs),4)) 

crse_runsdf120_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf120_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf120_3INS_DR=np.zeros((int(number_of_runs),4))

crse_runsdf180_1INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf180_2INS_DR=np.zeros((int(number_of_runs),4))
crse_runsdf180_3INS_DR=np.zeros((int(number_of_runs),4))
for nfr in range(number_of_runs):
    print('full training run: '+ str(nfr))

    #############################################################################
    #############################################################################
    #############################################################################
    'GRU TRAINING'
    #############################################################################
    #############################################################################
    #############################################################################

    Run_time, regress=RNN_model(np.array(x),np.array(y), input_dim,output_dim, seq_dim, batch_size, num_epochs, dropout, h2, learning_rate, l1_, l2_, nfr, decay_rate, momentum, decay_steps)

    'challenging scenarios'   

    dist_travldhrcs, perf_metrhr_crsepcs, perf_metrhr_crsedrcs, perf_metrhr_caepcs, perf_metrhr_caedrcs, perf_metrhr_aepspcs, perf_metrhr_aepsdrcs,newPpredshrcs, inshrcs, gpshrcs=predictcs(xthr,ythr, ithr, gthr, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Motorway Scenario',outage1) 

    dist_travldra1cs, perf_metrra1_crsepcs, perf_metrra1_crsedrcs, perf_metrra1_caepcs, perf_metrra1_caedrcs,perf_metrra1_aepspcs, perf_metrra1_aepsdrcs,newPpredsra1cs, insra1cs, gpsra1cs=predictcs(xtra1,ytra1, itra1, gtra1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Roundabout Scenario V_Vta11',outage1)  
    dist_travldra2cs, perf_metrra2_crsepcs, perf_metrra2_crsedrcs, perf_metrra2_caepcs, perf_metrra2_caedrcs,perf_metrra2_aepspcs, perf_metrra2_aepsdrcs,newPpredsra2cs, insra2cs, gpsra2cs=predictcs(xtra2,ytra2, itra2, gtra2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Roundabout Scenario V_Vfb02d',outage1) 

    dist_travldcia1cs, perf_metrcia1_crsepcs, perf_metrcia1_crsedrcs,perf_metrcia1_caepcs, perf_metrcia1_caedrcs,perf_metrcia1_aepspcs, perf_metrcia1_aepsdrcs,newPpredscia1cs, insciac1s, gpsciac1s=predictcs(xtcia1,ytcia1, itcia1, gtcia1, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Quick Changes in \n Acceleration Scenario V_Vfb02e',outage1) 
    dist_travldcia2cs, perf_metrcia2_crsepcs, perf_metrcia2_crsedrcs,perf_metrcia2_caepcs, perf_metrcia2_caedrcs,perf_metrcia2_aepspcs, perf_metrcia2_aepsdrcs,newPpredscia2cs, insciac2s, gpsciac2s=predictcs(xtcia2,ytcia2, itcia2, gtcia2, regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Quick Changes in \n Acceleration Scenario V_Vta12',outage1) 

    dist_travldhb1cs, perf_metrhb1_crsepcs, perf_metrhb1_crsedrcs,perf_metrhb1_caepcs, perf_metrhb1_caedrcs,perf_metrhb1_aepspcs, perf_metrhb1_aepsdrcs,newPpredshb1cs, inshb1cs, gpshb1cs=predictcs(xthb1,ythb1, ithb1, gthb1, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Hard Brake Scenario V_Vw16b',outage1) 
    dist_travldhb2cs, perf_metrhb2_crsepcs, perf_metrhb2_crsedrcs,perf_metrhb2_caepcs, perf_metrhb2_caedrcs,perf_metrhb2_aepspcs, perf_metrhb2_aepsdrcs,newPpredshb2cs, inshb2cs, gpshb2cs=predictcs(xthb2,ythb2, ithb2, gthb2, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Hard Brake Scenario V_Vw17',outage1) 

    dist_travldslr1cs, perf_metrslr1_crsepcs, perf_metrslr1_crsedrcs,perf_metrslr1_caepcs, perf_metrslr1_caedrcs,perf_metrslr1_aepspcs, perf_metrslr1_aepsdrcs,newPpredsslr1cs, insslr1cs, gpsslr1cs=predictcs(xtslr1,ytslr1, itslr1, gtslr1, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Sharp Cornering and \n Successive Left and Right Turns Scenario V_Vw6',outage1) 
    dist_travldslr2cs, perf_metrslr2_crsepcs, perf_metrslr2_crsedrcs,perf_metrslr2_caepcs, perf_metrslr2_caedrcs,perf_metrslr2_aepspcs, perf_metrslr2_aepsdrcs,newPpredsslr2cs, insslr2cs, gpsslr2cs=predictcs(xtslr2,ytslr2, itslr2, gtslr2, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Sharp Cornering and \n Successive Left and Right Turns Scenario V_Vw8',outage1) 
    dist_travldslr3cs, perf_metrslr3_crsepcs, perf_metrslr3_crsedrcs,perf_metrslr3_caepcs, perf_metrslr3_caedrcs,perf_metrslr3_aepspcs, perf_metrslr3_aepsdrcs,newPpredsslr3cs, insslr3cs, gpsslr3cs=predictcs(xtslr3,ytslr3, itslr3, gtslr3, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Sharp Cornering and \n Successive Left and Right Turns Scenario V_Vw7',outage1) 

    dist_travldwr1cs, perf_metrwr1_crsepcs, perf_metrwr1_crsedrcs,perf_metrwr1_caepcs, perf_metrwr1_caedrcs,perf_metrwr1_aepspcs, perf_metrwr1_aepsdrcs,newPpredswr1cs, inswr1cs, gpswr1cs=predictcs(xtwr1,ytwr1, itwr1, gtwr1, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Wet Road Scenario V_Vtb8',outage1) 
    dist_travldwr2cs, perf_metrwr2_crsepcs, perf_metrwr2_crsedrcs,perf_metrwr2_caepcs, perf_metrwr2_caedrcs,perf_metrwr2_aepspcs, perf_metrwr2_aepsdrcs,newPpredswr2cs, inswr2cs, gpswr2cs=predictcs(xtwr2,ytwr2, itwr2, gtwr2, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Wet Road Scenario V_Vtb11',outage1) 
    dist_travldwr3cs, perf_metrwr3_crsepcs, perf_metrwr3_crsedrcs,perf_metrwr3_caepcs, perf_metrwr3_caedrcs,perf_metrwr3_aepspcs, perf_metrwr3_aepsdrcs,newPpredswr3cs, inswr3cs, gpswr3cs=predictcs(xtwr3,ytwr3, itwr3, gtwr3, regress, seq_dim, input_dim, mode,Ts, dgmx, dgmn, Z, 'Wet Road Scenario V_Vtb13',outage1) 

    '30s outage'  
    dist_travldag1_30s, perf_metrag1_crsep30s, perf_metrag1_crsedr30s, perf_metrag1_caep30s, perf_metrag1_caedr30s,perf_metrag1_aepsp30s, perf_metrag1_aepsdr30s, newPpredsag1_30s, insag1_30s, gpsag1_30s=predictcs(xtag1,ytag1, itag1, gtag1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vta1a',outage2)   
    dist_travldag2_30s, perf_metrag2_crsep30s, perf_metrag2_crsedr30s, perf_metrag2_caep30s, perf_metrag2_caedr30s,perf_metrag2_aepsp30s, perf_metrag2_aepsdr30s, newPpredsag2_30s, insag2_30s, gpsag2_30s=predictcs(xtag2,ytag2, itag2, gtag2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vw2',outage2)    
    dist_travldag3_30s, perf_metrag3_crsep30s, perf_metrag3_crsedr30s, perf_metrag3_caep30s, perf_metrag3_caedr30s,perf_metrag3_aepsp30s, perf_metrag3_aepsdr30s, newPpredsag3_30s, insag3_30s, gpsag3_30s=predictcs(xtag3,ytag3, itag3, gtag3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vtb1',outage2)   
    dist_travldag4_30s, perf_metrag4_crsep30s, perf_metrag4_crsedr30s, perf_metrag4_caep30s, perf_metrag4_caedr30s,perf_metrag4_aepsp30s, perf_metrag4_aepsdr30s, newPpredsag4_30s, insag4_30s, gpsag4_30s=predictcs(xtag4,ytag4, itag4, gtag4,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb01d',outage2)   
    dist_travldag5_30s, perf_metrag5_crsep30s, perf_metrag5_crsedr30s, perf_metrag5_caep30s, perf_metrag5_caedr30s,perf_metrag5_aepsp30s, perf_metrag5_aepsdr30s, newPpredsag5_30s, insag5_30s, gpsag5_30s=predictcs(xtag5,ytag5, itag5, gtag5,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02a',outage2)   
    dist_travldag6_30s, perf_metrag6_crsep30s, perf_metrag6_crsedr30s, perf_metrag6_caep30s, perf_metrag6_caedr30s,perf_metrag6_aepsp30s, perf_metrag6_aepsdr30s, newPpredsag6_30s, insag6_30s, gpsag6_30s=predictcs(xtag6,ytag6, itag6, gtag6,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02g',outage2)   
    dist_travlddf1_30s, perf_metrdf1_crsep30s, perf_metrdf1_crsedr30s, perf_metrdf1_caep30s, perf_metrdf1_caedr30s,perf_metrdf1_aepsp30s, perf_metrdf1_aepsdr30s, newPpredsdf1_30s, insdf1_30s, gpsdf1_30s=predictcs(xtdf1, ytdf1, itdf1, gtdf1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_S3b',outage2)   
    dist_travlddf2_30s, perf_metrdf2_crsep30s, perf_metrdf2_crsedr30s, perf_metrdf2_caep30s, perf_metrdf2_caedr30s,perf_metrdf2_aepsp30s, perf_metrdf2_aepsdr30s, newPpredsdf2_30s, insdf2_30s, gpsdf2_30s=predictcs(xtdf2,ytdf2, itdf2, gtdf2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage2)   
    dist_travlddf3_30s, perf_metrdf3_crsep30s, perf_metrdf3_crsedr30s, perf_metrdf3_caep30s, perf_metrdf3_caedr30s,perf_metrdf3_aepsp30s, perf_metrdf3_aepsdr30s, newPpredsdf3_30s, insdf3_30s, gpsdf3_30s=predictcs(xtdf3,ytdf3, itdf3, gtdf3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage2)   

    '60s outage' 
    dist_travldag1_60s, perf_metrag1_crsep60s, perf_metrag1_crsedr60s, perf_metrag1_caep60s, perf_metrag1_caedr60s,perf_metrag1_aepsp60s, perf_metrag1_aepsdr60s, newPpredsag1_60s, insag1_60s, gpsag1_60s=predictcs(xtag1,ytag1, itag1, gtag1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vta1a',outage3)   
    dist_travldag2_60s, perf_metrag2_crsep60s, perf_metrag2_crsedr60s, perf_metrag2_caep60s, perf_metrag2_caedr60s,perf_metrag2_aepsp60s, perf_metrag2_aepsdr60s, newPpredsag2_60s, insag2_60s, gpsag2_60s=predictcs(xtag2,ytag2, itag2, gtag2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vw2',outage3)   
    dist_travldag3_60s, perf_metrag3_crsep60s, perf_metrag3_crsedr60s, perf_metrag3_caep60s, perf_metrag3_caedr60s,perf_metrag3_aepsp60s, perf_metrag3_aepsdr60s, newPpredsag3_60s, insag3_60s, gpsag3_60s=predictcs(xtag3,ytag3, itag3, gtag3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vtb1',outage3)   
    dist_travldag4_60s, perf_metrag4_crsep60s, perf_metrag4_crsedr60s, perf_metrag4_caep60s, perf_metrag4_caedr60s,perf_metrag4_aepsp60s, perf_metrag4_aepsdr60s, newPpredsag4_60s, insag4_60s, gpsag4_60s=predictcs(xtag4,ytag4, itag4, gtag4,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb01d',outage3)   
    dist_travldag5_60s, perf_metrag5_crsep60s, perf_metrag5_crsedr60s, perf_metrag5_caep60s, perf_metrag5_caedr60s,perf_metrag5_aepsp60s, perf_metrag5_aepsdr60s, newPpredsag5_60s, insag5_60s, gpsag5_60s=predictcs(xtag5,ytag5, itag5, gtag5,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02a',outage3)   
    dist_travldag6_60s, perf_metrag6_crsep60s, perf_metrag6_crsedr60s, perf_metrag6_caep60s, perf_metrag6_caedr60s,perf_metrag6_aepsp60s, perf_metrag6_aepsdr60s, newPpredsag6_60s, insag6_60s, gpsag6_60s=predictcs(xtag6,ytag6, itag6, gtag6,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02g',outage3)   
    dist_travlddf1_60s, perf_metrdf1_crsep60s, perf_metrdf1_crsedr60s, perf_metrdf1_caep60s, perf_metrdf1_caedr60s,perf_metrdf1_aepsp60s, perf_metrdf1_aepsdr60s, newPpredsdf1_60s, insdf1_60s, gpsdf1_60s=predictcs(xtdf1,ytdf1, itdf1, gtdf1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_S3b',outage3)   
    dist_travlddf2_60s, perf_metrdf2_crsep60s, perf_metrdf2_crsedr60s, perf_metrdf2_caep60s, perf_metrdf2_caedr60s,perf_metrdf2_aepsp60s, perf_metrdf2_aepsdr60s, newPpredsdf2_60s, insdf2_60s, gpsdf2_60s=predictcs(xtdf2,ytdf2, itdf2, gtdf2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage3)   
    dist_travlddf3_60s, perf_metrdf3_crsep60s, perf_metrdf3_crsedr60s, perf_metrdf3_caep60s, perf_metrdf3_caedr60s,perf_metrdf3_aepsp60s, perf_metrdf3_aepsdr60s, newPpredsdf3_60s, insdf3_60s, gpsdf3_60s=predictcs(xtdf3,ytdf3, itdf3, gtdf3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage3)   

    '90s outage'  
    dist_travldag1_90s, perf_metrag1_crsep90s, perf_metrag1_crsedr90s, perf_metrag1_caep90s, perf_metrag1_caedr90s,perf_metrag1_aepsp90s, perf_metrag1_aepsdr90s, newPpredsag1_90s, insag1_90s, gpsag1_90s=predictcs(xtag1,ytag1, itag1, gtag1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vta1a',outage4)   
    dist_travldag2_90s, perf_metrag2_crsep90s, perf_metrag2_crsedr90s, perf_metrag2_caep90s, perf_metrag2_caedr90s,perf_metrag2_aepsp90s, perf_metrag2_aepsdr90s, newPpredsag2_90s, insag2_90s, gpsag2_90s=predictcs(xtag2,ytag2, itag2, gtag2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vw2',outage4)   
    dist_travldag3_90s, perf_metrag3_crsep90s, perf_metrag3_crsedr90s, perf_metrag3_caep90s, perf_metrag3_caedr90s,perf_metrag3_aepsp90s, perf_metrag3_aepsdr90s, newPpredsag3_90s, insag3_90s, gpsag3_90s=predictcs(xtag3,ytag3, itag3, gtag3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vtb1',outage4)   
    dist_travldag4_90s, perf_metrag4_crsep90s, perf_metrag4_crsedr90s, perf_metrag4_caep90s, perf_metrag4_caedr90s,perf_metrag4_aepsp90s, perf_metrag4_aepsdr90s, newPpredsag4_90s, insag4_90s, gpsag4_90s=predictcs(xtag4,ytag4, itag4, gtag4,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb01d',outage4)   
    dist_travldag5_90s, perf_metrag5_crsep90s, perf_metrag5_crsedr90s, perf_metrag5_caep90s, perf_metrag5_caedr90s,perf_metrag5_aepsp90s, perf_metrag5_aepsdr90s, newPpredsag5_90s, insag5_90s, gpsag5_90s=predictcs(xtag5,ytag5, itag5, gtag5,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02a',outage4)   
    dist_travldag6_90s, perf_metrag6_crsep90s, perf_metrag6_crsedr90s, perf_metrag6_caep90s, perf_metrag6_caedr90s,perf_metrag6_aepsp90s, perf_metrag6_aepsdr90s, newPpredsag6_90s, insag6_90s, gpsag6_90s=predictcs(xtag6,ytag6, itag6, gtag6,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02g',outage4)   
    dist_travlddf1_90s, perf_metrdf1_crsep90s, perf_metrdf1_crsedr90s, perf_metrdf1_caep90s, perf_metrdf1_caedr90s,perf_metrdf1_aepsp90s, perf_metrdf1_aepsdr90s, newPpredsdf1_90s, insdf1_90s, gpsdf1_90s=predictcs(xtdf1,ytdf1, itdf1, gtdf1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_S3b',outage4)   
    dist_travlddf2_90s, perf_metrdf2_crsep90s, perf_metrdf2_crsedr90s, perf_metrdf2_caep90s, perf_metrdf2_caedr90s,perf_metrdf2_aepsp90s, perf_metrdf2_aepsdr90s, newPpredsdf2_90s, insdf2_90s, gpsdf2_90s=predictcs(xtdf2,ytdf2, itdf2, gtdf2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage4)   
    dist_travlddf3_90s, perf_metrdf3_crsep90s, perf_metrdf3_crsedr90s, perf_metrdf3_caep90s, perf_metrdf3_caedr90s,perf_metrdf3_aepsp90s, perf_metrdf3_aepsdr90s, newPpredsdf3_90s, insdf3_90s, gpsdf3_90s=predictcs(xtdf3,ytdf3, itdf3, gtdf3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage4)   

    '120s outage'  
    dist_travldag1_120s, perf_metrag1_crsep120s, perf_metrag1_crsedr120s, perf_metrag1_caep120s, perf_metrag1_caedr120s,perf_metrag1_aepsp120s, perf_metrag1_aepsdr120s, newPpredsag1_120s, insag1_120s, gpsag1_120s=predictcs(xtag1,ytag1, itag1, gtag1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vta1a',outage5)   
    dist_travldag2_120s, perf_metrag2_crsep120s, perf_metrag2_crsedr120s, perf_metrag2_caep120s, perf_metrag2_caedr120s,perf_metrag2_aepsp120s, perf_metrag2_aepsdr120s, newPpredsag2_120s, insag2_120s, gpsag2_120s=predictcs(xtag2,ytag2, itag2, gtag2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vw2',outage5)   
    dist_travldag3_120s, perf_metrag3_crsep120s, perf_metrag3_crsedr120s, perf_metrag3_caep120s, perf_metrag3_caedr120s,perf_metrag3_aepsp120s, perf_metrag3_aepsdr120s, newPpredsag3_120s, insag3_120s, gpsag3_120s=predictcs(xtag3,ytag3, itag3, gtag3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vtb1',outage5)   
    dist_travldag4_120s, perf_metrag4_crsep120s, perf_metrag4_crsedr120s, perf_metrag4_caep120s, perf_metrag4_caedr120s,perf_metrag4_aepsp120s, perf_metrag4_aepsdr120s, newPpredsag4_120s, insag4_120s, gpsag4_120s=predictcs(xtag4,ytag4, itag4, gtag4,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb01d',outage5)   
    dist_travldag5_120s, perf_metrag5_crsep120s, perf_metrag5_crsedr120s, perf_metrag5_caep120s, perf_metrag5_caedr120s,perf_metrag5_aepsp120s, perf_metrag5_aepsdr120s, newPpredsag5_120s, insag5_120s, gpsag5_120s=predictcs(xtag5,ytag5, itag5, gtag5,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02a',outage5)   
    dist_travldag6_120s, perf_metrag6_crsep120s, perf_metrag6_crsedr120s, perf_metrag6_caep120s, perf_metrag6_caedr120s,perf_metrag6_aepsp120s, perf_metrag6_aepsdr120s, newPpredsag6_120s, insag6_120s, gpsag6_120s=predictcs(xtag6,ytag6, itag6, gtag6,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Agrressive driving 120s Outage V_Vfb02g',outage5)   
    dist_travlddf1_120s, perf_metrdf1_crsep120s, perf_metrdf1_crsedr120s, perf_metrdf1_caep120s, perf_metrdf1_caedr120s,perf_metrdf1_aepsp120s, perf_metrdf1_aepsdr120s, newPpredsdf1_120s, insdf1_120s, gpsdf1_120s=predictcs(xtdf1,ytdf1, itdf1, gtdf1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_S3b',outage5)   
    dist_travlddf2_120s, perf_metrdf2_crsep120s, perf_metrdf2_crsedr120s, perf_metrdf2_caep120s, perf_metrdf2_caedr120s,perf_metrdf2_aepsp120s, perf_metrdf2_aepsdr120s, newPpredsdf2_120s, insdf2_120s, gpsdf2_120s=predictcs(xtdf2,ytdf2, itdf2, gtdf2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage5)   
    dist_travlddf3_120s, perf_metrdf3_crsep120s, perf_metrdf3_crsedr120s, perf_metrdf3_caep120s, perf_metrdf3_caedr120s,perf_metrdf3_aepsp120s, perf_metrdf3_aepsdr120s, newPpredsdf3_120s, insdf3_120s, gpsdf3_120s=predictcs(xtdf3,ytdf3, itdf3, gtdf3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, 'Defensive driving 120s Outage V_St4',outage5)   

    '180s outage'  
    dist_travldag1_180s, perf_metrag1_crsep180s, perf_metrag1_crsedr180s, perf_metrag1_caep180s, perf_metrag1_caedr180s,perf_metrag1_aepsp180s, perf_metrag1_aepsdr180s, newPpredsag1_180s, insag1_180s, gpsag1_180s=predictcs(xtag1,ytag1, itag1, gtag1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_Vtb3)',outage6)   
    dist_travldag2_180s, perf_metrag2_crsep180s, perf_metrag2_crsedr180s, perf_metrag2_caep180s, perf_metrag2_caedr180s,perf_metrag2_aepsp180s, perf_metrag2_aepsdr180s, newPpredsag2_180s, insag2_180s, gpsag2_180s=predictcs(xtag2,ytag2, itag2, gtag2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_Vfb01c)',outage6)   
    dist_travldag3_180s, perf_metrag3_crsep180s, perf_metrag3_crsedr180s, perf_metrag3_caep180s, perf_metrag3_caedr180s,perf_metrag3_aepsp180s, perf_metrag3_aepsdr180s, newPpredsag3_180s, insag3_180s, gpsag3_180s=predictcs(xtag3,ytag3, itag3, gtag3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_Vfb02a)',outage6)   
    dist_travldag4_180s, perf_metrag4_crsep180s, perf_metrag4_crsedr180s, perf_metrag4_caep180s, perf_metrag4_caedr180s,perf_metrag4_aepsp180s, perf_metrag4_aepsdr180s, newPpredsag4_180s, insag4_180s, gpsag4_180s=predictcs(xtag4,ytag4, itag4, gtag4,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_Vta1a)',outage6)   
    dist_travldag5_180s, perf_metrag5_crsep180s, perf_metrag5_crsedr180s, perf_metrag5_caep180s, perf_metrag5_caedr180s,perf_metrag5_aepsp180s, perf_metrag5_aepsdr180s, newPpredsag5_180s, insag5_180s, gpsag5_180s=predictcs(xtag5,ytag5, itag5, gtag5,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_Vfb02b)',outage6)   
    dist_travldag6_180s, perf_metrag6_crsep180s, perf_metrag6_crsedr180s, perf_metrag6_caep180s, perf_metrag6_caedr180s,perf_metrag6_aepsp180s, perf_metrag6_aepsdr180s, newPpredsag6_180s, insag6_180s, gpsag6_180s=predictcs(xtag6,ytag6, itag6, gtag6,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_Vfb02g)',outage6)   
    dist_travlddf1_180s, perf_metrdf1_crsep180s, perf_metrdf1_crsedr180s, perf_metrdf1_caep180s, perf_metrdf1_caedr180s,perf_metrdf1_aepsp180s, perf_metrdf1_aepsdr180s, newPpredsdf1_180s, insdf1_180s, gpsdf1_180s=predictcs(xtdf1,ytdf1, itdf1, gtdf1,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_St6)',outage6)   
    dist_travlddf2_180s, perf_metrdf2_crsep180s, perf_metrdf2_crsedr180s, perf_metrdf2_caep180s, perf_metrdf2_caedr180s,perf_metrdf2_aepsp180s, perf_metrdf2_aepsdr180s, newPpredsdf2_180s, insdf2_180s, gpsdf2_180s=predictcs(xtdf2,ytdf2, itdf2, gtdf2,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_St7)',outage6)   
    dist_travlddf3_180s, perf_metrdf3_crsep180s, perf_metrdf3_crsedr180s, perf_metrdf3_caep180s, perf_metrdf3_caedr180s,perf_metrdf3_aepsp180s, perf_metrdf3_aepsdr180s, newPpredsdf3_180s, insdf3_180s, gpsdf3_180s=predictcs(xtdf3,ytdf3, itdf3, gtdf3,regress, seq_dim, input_dim, mode, Ts, dgmx, dgmn, Z, '180 s GNSS Outage (V_S3a)',outage6)   


    'indexes the maximum prediction crse across each 10 seconds array'
    crse_runshrNN[nfr]=perf_metrhr_crsepcs[:]

    crse_runsra_1NN[nfr]=perf_metrra1_crsepcs[:]  
    crse_runsra_2NN[nfr]=perf_metrra2_crsepcs[:]         

    crse_runscia_1NN[nfr]=perf_metrcia1_crsepcs[:] 
    crse_runscia_2NN[nfr]=perf_metrcia2_crsepcs[:]         

    crse_runshb_1NN[nfr]=perf_metrhb1_crsepcs[:]
    crse_runshb_2NN[nfr]=perf_metrhb2_crsepcs[:]        

    crse_runsslr_1NN[nfr]=perf_metrslr1_crsepcs[:]  
    crse_runsslr_2NN[nfr]=perf_metrslr2_crsepcs[:]         
    crse_runsslr_3NN[nfr]=perf_metrslr3_crsepcs[:] 

    crse_runswr_1NN[nfr]=perf_metrwr1_crsepcs[:]
    crse_runswr_2NN[nfr]=perf_metrwr2_crsepcs[:]        
    crse_runswr_3NN[nfr]=perf_metrwr3_crsepcs[:]        

    crse_runsag30_1NN[nfr]=perf_metrag1_crsep30s[:]
    crse_runsag30_2NN[nfr]=perf_metrag2_crsep30s[:]        
    crse_runsag30_3NN[nfr]=perf_metrag3_crsep30s[:]        
    crse_runsag30_4NN[nfr]=perf_metrag4_crsep30s[:]        
    crse_runsag30_5NN[nfr]=perf_metrag5_crsep30s[:] 
    crse_runsag30_6NN[nfr]=perf_metrag6_crsep30s[:]        
  
    crse_runsag60_1NN[nfr]=perf_metrag1_crsep60s[:]
    crse_runsag60_2NN[nfr]=perf_metrag2_crsep60s[:]        
    crse_runsag60_3NN[nfr]=perf_metrag3_crsep60s[:]        
    crse_runsag60_4NN[nfr]=perf_metrag4_crsep60s[:]        
    crse_runsag60_5NN[nfr]=perf_metrag5_crsep60s[:] 
    crse_runsag60_6NN[nfr]=perf_metrag6_crsep60s[:]        

    crse_runsag90_1NN[nfr]=perf_metrag1_crsep90s[:]
    crse_runsag90_2NN[nfr]=perf_metrag2_crsep90s[:]        
    crse_runsag90_3NN[nfr]=perf_metrag3_crsep90s[:]        
    crse_runsag90_4NN[nfr]=perf_metrag4_crsep90s[:]        
    crse_runsag90_5NN[nfr]=perf_metrag5_crsep90s[:]   
    crse_runsag90_6NN[nfr]=perf_metrag6_crsep90s[:]        

    crse_runsag120_1NN[nfr]=perf_metrag1_crsep120s[:]
    crse_runsag120_2NN[nfr]=perf_metrag2_crsep120s[:]        
    crse_runsag120_3NN[nfr]=perf_metrag3_crsep120s[:]        
    crse_runsag120_4NN[nfr]=perf_metrag4_crsep120s[:]        
    crse_runsag120_5NN[nfr]=perf_metrag5_crsep120s[:] 
    crse_runsag120_6NN[nfr]=perf_metrag6_crsep120s[:]        

    crse_runsag180_1NN[nfr]=perf_metrag1_crsep180s[:]
    crse_runsag180_2NN[nfr]=perf_metrag2_crsep180s[:]        
    crse_runsag180_3NN[nfr]=perf_metrag3_crsep180s[:]        
    crse_runsag180_4NN[nfr]=perf_metrag4_crsep180s[:]        
    crse_runsag180_5NN[nfr]=perf_metrag5_crsep180s[:] 
    crse_runsag180_6NN[nfr]=perf_metrag6_crsep180s[:]

    crse_runsdf30_1NN[nfr]=perf_metrdf1_crsep30s[:]
    crse_runsdf30_2NN[nfr]=perf_metrdf2_crsep30s[:]               
    crse_runsdf30_3NN[nfr]=perf_metrdf3_crsep30s[:] 

    crse_runsdf60_1NN[nfr]=perf_metrdf1_crsep60s[:]
    crse_runsdf60_2NN[nfr]=perf_metrdf2_crsep60s[:]               
    crse_runsdf60_3NN[nfr]=perf_metrdf3_crsep60s[:]   

    crse_runsdf90_1NN[nfr]=perf_metrdf1_crsep90s[:]
    crse_runsdf90_2NN[nfr]=perf_metrdf2_crsep90s[:]               
    crse_runsdf90_3NN[nfr]=perf_metrdf3_crsep90s[:] 

    crse_runsdf120_1NN[nfr]=perf_metrdf1_crsep120s[:]   
    crse_runsdf120_2NN[nfr]=perf_metrdf2_crsep120s[:]                 
    crse_runsdf120_3NN[nfr]=perf_metrdf3_crsep120s[:] 

    crse_runsdf180_1NN[nfr]=perf_metrdf1_crsep180s[:]   
    crse_runsdf180_2NN[nfr]=perf_metrdf2_crsep180s[:]  
    crse_runsdf180_3NN[nfr]=perf_metrdf3_crsep180s[:]  


        cae_runshrNN[nfr]=perf_metrhr_caepcs[:]
        
        cae_runsra_1NN[nfr]=perf_metrra1_caepcs[:]  
        cae_runsra_2NN[nfr]=perf_metrra2_caepcs[:]         
                
        cae_runscia_1NN[nfr]=perf_metrcia1_caepcs[:] 
        cae_runscia_2NN[nfr]=perf_metrcia2_caepcs[:]         
        
        cae_runshb_1NN[nfr]=perf_metrhb1_caepcs[:]
        cae_runshb_2NN[nfr]=perf_metrhb2_caepcs[:]        
        
        cae_runsslr_1NN[nfr]=perf_metrslr1_caepcs[:]  
        cae_runsslr_2NN[nfr]=perf_metrslr2_caepcs[:]         
        cae_runsslr_3NN[nfr]=perf_metrslr3_caepcs[:] 
        
        cae_runswr_1NN[nfr]=perf_metrwr1_caepcs[:]
        cae_runswr_2NN[nfr]=perf_metrwr2_caepcs[:]        
        cae_runswr_3NN[nfr]=perf_metrwr3_caepcs[:]        
        
        cae_runsag30_1NN[nfr]=perf_metrag1_caep30s[:]
        cae_runsag30_2NN[nfr]=perf_metrag2_caep30s[:]        
        cae_runsag30_3NN[nfr]=perf_metrag3_caep30s[:]        
        cae_runsag30_4NN[nfr]=perf_metrag4_caep30s[:]        
        cae_runsag30_5NN[nfr]=perf_metrag5_caep30s[:] 
        cae_runsag30_6NN[nfr]=perf_metrag6_caep30s[:]        
#        cae_runsag30_7NN[nfr]=perf_metrag7_caep30s[:]  
        
        cae_runsag60_1NN[nfr]=perf_metrag1_caep60s[:]
        cae_runsag60_2NN[nfr]=perf_metrag2_caep60s[:]        
        cae_runsag60_3NN[nfr]=perf_metrag3_caep60s[:]        
        cae_runsag60_4NN[nfr]=perf_metrag4_caep60s[:]        
        cae_runsag60_5NN[nfr]=perf_metrag5_caep60s[:] 
        cae_runsag60_6NN[nfr]=perf_metrag6_caep60s[:]        
#        cae_runsag60_7NN[nfr]=perf_metrag7_caep60s[:] 

        cae_runsag90_1NN[nfr]=perf_metrag1_caep90s[:]
        cae_runsag90_2NN[nfr]=perf_metrag2_caep90s[:]        
        cae_runsag90_3NN[nfr]=perf_metrag3_caep90s[:]        
        cae_runsag90_4NN[nfr]=perf_metrag4_caep90s[:]        
        cae_runsag90_5NN[nfr]=perf_metrag5_caep90s[:]   
        cae_runsag90_6NN[nfr]=perf_metrag6_caep90s[:]        
#        cae_runsag90_7NN[nfr]=perf_metrag7_caep90s[:]   
        
        cae_runsag120_1NN[nfr]=perf_metrag1_caep120s[:]
        cae_runsag120_2NN[nfr]=perf_metrag2_caep120s[:]        
        cae_runsag120_3NN[nfr]=perf_metrag3_caep120s[:]        
        cae_runsag120_4NN[nfr]=perf_metrag4_caep120s[:]        
        cae_runsag120_5NN[nfr]=perf_metrag5_caep120s[:] 
        cae_runsag120_6NN[nfr]=perf_metrag6_caep120s[:]        
#        cae_runsag120_7NN[nfr]=perf_metrag7_caep120s[:]  
        
        cae_runsag180_1NN[nfr]=perf_metrag1_caep180s[:]
        cae_runsag180_2NN[nfr]=perf_metrag2_caep180s[:]        
        cae_runsag180_3NN[nfr]=perf_metrag3_caep180s[:]        
        cae_runsag180_4NN[nfr]=perf_metrag4_caep180s[:]        
        cae_runsag180_5NN[nfr]=perf_metrag5_caep180s[:] 
        cae_runsag180_6NN[nfr]=perf_metrag6_caep180s[:]
#        cae_runsag180_7NN[nfr]=perf_metrag7_caep180s[:]
        
        cae_runsdf30_1NN[nfr]=perf_metrdf1_caep30s[:]
        cae_runsdf30_2NN[nfr]=perf_metrdf2_caep30s[:]               
        cae_runsdf30_3NN[nfr]=perf_metrdf3_caep30s[:]  
        
        cae_runsdf60_1NN[nfr]=perf_metrdf1_caep60s[:]
        cae_runsdf60_2NN[nfr]=perf_metrdf2_caep60s[:]               
        cae_runsdf60_3NN[nfr]=perf_metrdf3_caep60s[:] 
        
        cae_runsdf90_1NN[nfr]=perf_metrdf1_caep90s[:]
        cae_runsdf90_2NN[nfr]=perf_metrdf2_caep90s[:]               
        cae_runsdf90_3NN[nfr]=perf_metrdf3_caep90s[:]  
        
        cae_runsdf120_1NN[nfr]=perf_metrdf1_caep120s[:]   
        cae_runsdf120_2NN[nfr]=perf_metrdf2_caep120s[:]
        cae_runsdf120_3NN[nfr]=perf_metrdf3_caep120s[:]
        
        cae_runsdf180_1NN[nfr]=perf_metrdf1_caep180s[:]   
        cae_runsdf180_2NN[nfr]=perf_metrdf2_caep180s[:]
        cae_runsdf180_3NN[nfr]=perf_metrdf3_caep180s[:]

        
        'indexes the maximum prediction crse across each 10 seconds array'
 
        crse_runshrINS_DR[nfr]=perf_metrhr_crsedrcs[:]
        
        
        crse_runsra_1INS_DR[nfr]=perf_metrra1_crsedrcs[:] 
        crse_runsra_2INS_DR[nfr]=perf_metrra2_crsedrcs[:]         
        
        
        crse_runscia_1INS_DR[nfr]=perf_metrcia1_crsedrcs[:]
        crse_runscia_2INS_DR[nfr]=perf_metrcia2_crsedrcs[:]        
        
        crse_runshb_1INS_DR[nfr]=perf_metrhb1_crsedrcs[:]
        crse_runshb_2INS_DR[nfr]=perf_metrhb2_crsedrcs[:]        
        
        crse_runsslr_1INS_DR[nfr]=perf_metrslr1_crsedrcs[:] 
        crse_runsslr_2INS_DR[nfr]=perf_metrslr2_crsedrcs[:]         
        crse_runsslr_3INS_DR[nfr]=perf_metrslr3_crsedrcs[:]         
        
        crse_runswr_1INS_DR[nfr]=perf_metrwr1_crsedrcs[:]
        crse_runswr_2INS_DR[nfr]=perf_metrwr2_crsedrcs[:]        
        crse_runswr_3INS_DR[nfr]=perf_metrwr3_crsedrcs[:]

        crse_runsag30_1INS_DR[nfr]=perf_metrag1_crsedr30s[:]
        crse_runsag30_2INS_DR[nfr]=perf_metrag2_crsedr30s[:]        
        crse_runsag30_3INS_DR[nfr]=perf_metrag3_crsedr30s[:]        
        crse_runsag30_4INS_DR[nfr]=perf_metrag4_crsedr30s[:]        
        crse_runsag30_5INS_DR[nfr]=perf_metrag5_crsedr30s[:]
        crse_runsag30_6INS_DR[nfr]=perf_metrag6_crsedr30s[:]        
#        crse_runsag30_7INS_DR[nfr]=perf_metrag7_crsedr30s[:]
        
        crse_runsag60_1INS_DR[nfr]=perf_metrag1_crsedr60s[:]
        crse_runsag60_2INS_DR[nfr]=perf_metrag2_crsedr60s[:]        
        crse_runsag60_3INS_DR[nfr]=perf_metrag3_crsedr60s[:]        
        crse_runsag60_4INS_DR[nfr]=perf_metrag4_crsedr60s[:]        
        crse_runsag60_5INS_DR[nfr]=perf_metrag5_crsedr60s[:]
        crse_runsag60_6INS_DR[nfr]=perf_metrag6_crsedr60s[:]        
#        crse_runsag60_7INS_DR[nfr]=perf_metrag7_crsedr60s[:] 
        
        crse_runsag90_1INS_DR[nfr]=perf_metrag1_crsedr90s[:]
        crse_runsag90_2INS_DR[nfr]=perf_metrag2_crsedr90s[:]        
        crse_runsag90_3INS_DR[nfr]=perf_metrag3_crsedr90s[:]        
        crse_runsag90_4INS_DR[nfr]=perf_metrag4_crsedr90s[:]
        crse_runsag90_5INS_DR[nfr]=perf_metrag5_crsedr90s[:]
        crse_runsag90_6INS_DR[nfr]=perf_metrag6_crsedr90s[:]        
#        crse_runsag90_7INS_DR[nfr]=perf_metrag7_crsedr90s[:] 
        
        crse_runsag120_1INS_DR[nfr]=perf_metrag1_crsedr120s[:]
        crse_runsag120_2INS_DR[nfr]=perf_metrag2_crsedr120s[:]        
        crse_runsag120_3INS_DR[nfr]=perf_metrag3_crsedr120s[:]        
        crse_runsag120_4INS_DR[nfr]=perf_metrag4_crsedr120s[:]
        crse_runsag120_5INS_DR[nfr]=perf_metrag5_crsedr120s[:]
        crse_runsag120_6INS_DR[nfr]=perf_metrag6_crsedr120s[:]        
#        crse_runsag120_7INS_DR[nfr]=perf_metrag7_crsedr120s[:] 
        
        crse_runsag180_1INS_DR[nfr]=perf_metrag1_crsedr180s[:]
        crse_runsag180_2INS_DR[nfr]=perf_metrag2_crsedr180s[:]        
        crse_runsag180_3INS_DR[nfr]=perf_metrag3_crsedr180s[:]        
        crse_runsag180_4INS_DR[nfr]=perf_metrag4_crsedr180s[:]
        crse_runsag180_5INS_DR[nfr]=perf_metrag5_crsedr180s[:]
        crse_runsag180_6INS_DR[nfr]=perf_metrag6_crsedr180s[:]        
#        crse_runsag180_7INS_DR[nfr]=perf_metrag7_crsedr180s[:] 
        
        crse_runsdf30_1INS_DR[nfr]=perf_metrdf1_crsedr30s[:]
        crse_runsdf30_2INS_DR[nfr]=perf_metrdf2_crsedr30s[:]              
        crse_runsdf30_3INS_DR[nfr]=perf_metrdf3_crsedr30s[:]  
        
        crse_runsdf60_1INS_DR[nfr]=perf_metrdf1_crsedr60s[:]
        crse_runsdf60_2INS_DR[nfr]=perf_metrdf2_crsedr60s[:]               
        crse_runsdf60_3INS_DR[nfr]=perf_metrdf3_crsedr60s[:] 
        
        crse_runsdf90_1INS_DR[nfr]=perf_metrdf1_crsedr90s[:]
        crse_runsdf90_2INS_DR[nfr]=perf_metrdf2_crsedr90s[:]                
        crse_runsdf90_3INS_DR[nfr]=perf_metrdf3_crsedr90s[:] 
        
        crse_runsdf120_1INS_DR[nfr]=perf_metrdf1_crsedr120s[:] 
        crse_runsdf120_2INS_DR[nfr]=perf_metrdf2_crsedr120s[:]                  
        crse_runsdf120_3INS_DR[nfr]=perf_metrdf3_crsedr120s[:]  
        
        crse_runsdf180_1INS_DR[nfr]=perf_metrdf1_crsedr180s[:] 
        crse_runsdf180_2INS_DR[nfr]=perf_metrdf2_crsedr180s[:]                  
        crse_runsdf180_3INS_DR[nfr]=perf_metrdf3_crsedr180s[:] 




        cae_runshrINS_DR[nfr]=perf_metrhr_caedrcs[:]
        
        cae_runsra_1INS_DR[nfr]=perf_metrra1_caedrcs[:] 
        cae_runsra_2INS_DR[nfr]=perf_metrra2_caedrcs[:]         
        
        cae_runscia_1INS_DR[nfr]=perf_metrcia1_caedrcs[:]
        cae_runscia_2INS_DR[nfr]=perf_metrcia2_caedrcs[:]        
        
        cae_runshb_1INS_DR[nfr]=perf_metrhb1_caedrcs[:]
        cae_runshb_2INS_DR[nfr]=perf_metrhb2_caedrcs[:]        
        
        cae_runsslr_1INS_DR[nfr]=perf_metrslr1_caedrcs[:] 
        cae_runsslr_2INS_DR[nfr]=perf_metrslr2_caedrcs[:]         
        cae_runsslr_3INS_DR[nfr]=perf_metrslr3_caedrcs[:]         
        
        cae_runswr_1INS_DR[nfr]=perf_metrwr1_caedrcs[:]
        cae_runswr_2INS_DR[nfr]=perf_metrwr2_caedrcs[:]        
        cae_runswr_3INS_DR[nfr]=perf_metrwr3_caedrcs[:]

        cae_runsag30_1INS_DR[nfr]=perf_metrag1_caedr30s[:]
        cae_runsag30_2INS_DR[nfr]=perf_metrag2_caedr30s[:]        
        cae_runsag30_3INS_DR[nfr]=perf_metrag3_caedr30s[:]        
        cae_runsag30_4INS_DR[nfr]=perf_metrag4_caedr30s[:]        
        cae_runsag30_5INS_DR[nfr]=perf_metrag5_caedr30s[:]
        cae_runsag30_6INS_DR[nfr]=perf_metrag6_caedr30s[:]        
#        cae_runsag30_7INS_DR[nfr]=perf_metrag7_caedr30s[:]
        
        cae_runsag60_1INS_DR[nfr]=perf_metrag1_caedr60s[:]
        cae_runsag60_2INS_DR[nfr]=perf_metrag2_caedr60s[:]        
        cae_runsag60_3INS_DR[nfr]=perf_metrag3_caedr60s[:]        
        cae_runsag60_4INS_DR[nfr]=perf_metrag4_caedr60s[:]        
        cae_runsag60_5INS_DR[nfr]=perf_metrag5_caedr60s[:]
        cae_runsag60_6INS_DR[nfr]=perf_metrag6_caedr60s[:]        
#        cae_runsag60_7INS_DR[nfr]=perf_metrag7_caedr60s[:]   
        
        cae_runsag90_1INS_DR[nfr]=perf_metrag1_caedr90s[:]
        cae_runsag90_2INS_DR[nfr]=perf_metrag2_caedr90s[:]        
        cae_runsag90_3INS_DR[nfr]=perf_metrag3_caedr90s[:]        
        cae_runsag90_4INS_DR[nfr]=perf_metrag4_caedr90s[:]
        cae_runsag90_5INS_DR[nfr]=perf_metrag5_caedr90s[:]
        cae_runsag90_6INS_DR[nfr]=perf_metrag6_caedr90s[:]        
#        cae_runsag90_7INS_DR[nfr]=perf_metrag7_caedr90s[:]  
        
        cae_runsag120_1INS_DR[nfr]=perf_metrag1_caedr120s[:]
        cae_runsag120_2INS_DR[nfr]=perf_metrag2_caedr120s[:]        
        cae_runsag120_3INS_DR[nfr]=perf_metrag3_caedr120s[:]        
        cae_runsag120_4INS_DR[nfr]=perf_metrag4_caedr120s[:]
        cae_runsag120_5INS_DR[nfr]=perf_metrag5_caedr120s[:]
        cae_runsag120_6INS_DR[nfr]=perf_metrag6_caedr120s[:]        
#        cae_runsag120_7INS_DR[nfr]=perf_metrag7_caedr120s[:]   
        
        cae_runsag180_1INS_DR[nfr]=perf_metrag1_caedr180s[:]
        cae_runsag180_2INS_DR[nfr]=perf_metrag2_caedr180s[:]        
        cae_runsag180_3INS_DR[nfr]=perf_metrag3_caedr180s[:]        
        cae_runsag180_4INS_DR[nfr]=perf_metrag4_caedr180s[:]
        cae_runsag180_5INS_DR[nfr]=perf_metrag5_caedr180s[:]
        cae_runsag180_6INS_DR[nfr]=perf_metrag6_caedr180s[:]        
#        cae_runsag180_7INS_DR[nfr]=perf_metrag7_caedr180s[:]  
        
        cae_runsdf30_1INS_DR[nfr]=perf_metrdf1_caedr30s[:]
        cae_runsdf30_2INS_DR[nfr]=perf_metrdf2_caedr30s[:]              
        cae_runsdf30_3INS_DR[nfr]=perf_metrdf3_caedr30s[:] 
        
        cae_runsdf60_1INS_DR[nfr]=perf_metrdf1_caedr60s[:]
        cae_runsdf60_2INS_DR[nfr]=perf_metrdf2_caedr60s[:]               
        cae_runsdf60_3INS_DR[nfr]=perf_metrdf3_caedr60s[:]  
        
        cae_runsdf90_1INS_DR[nfr]=perf_metrdf1_caedr90s[:]
        cae_runsdf90_2INS_DR[nfr]=perf_metrdf2_caedr90s[:]                
        cae_runsdf90_3INS_DR[nfr]=perf_metrdf3_caedr90s[:]   
        
        cae_runsdf120_1INS_DR[nfr]=perf_metrdf1_caedr120s[:] 
        cae_runsdf120_2INS_DR[nfr]=perf_metrdf2_caedr120s[:]        
        cae_runsdf120_3INS_DR[nfr]=perf_metrdf3_caedr120s[:]  
        
        cae_runsdf180_1INS_DR[nfr]=perf_metrdf1_caedr180s[:] 
        cae_runsdf180_2INS_DR[nfr]=perf_metrdf2_caedr180s[:]        
        cae_runsdf180_3INS_DR[nfr]=perf_metrdf3_caedr180s[:]
 
     
    'indexes the best results across the optimisation runs'       
    ahrNN=np.amin(crse_runshrNN,axis=0)
    
    ara_1NN=np.amin(crse_runsra_1NN,axis=0)
    ara_2NN=np.amin(crse_runsra_2NN,axis=0)
    
    acia_1NN=np.amin(crse_runscia_1NN,axis=0)
    acia_2NN=np.amin(crse_runscia_2NN,axis=0)
    
    ahb_1NN=np.amin(crse_runshb_1NN,axis=0)
    ahb_2NN=np.amin(crse_runshb_2NN,axis=0)
       
    aslr_1NN=np.amin(crse_runsslr_1NN,axis=0)
    aslr_2NN=np.amin(crse_runsslr_2NN,axis=0)
    aslr_3NN=np.amin(crse_runsslr_3NN,axis=0)
    
    awr_1NN=np.amin(crse_runswr_1NN,axis=0)
    awr_2NN=np.amin(crse_runswr_2NN,axis=0)
    awr_3NN=np.amin(crse_runswr_3NN,axis=0)
    
    aag030_1NN=np.amin(crse_runsag30_1NN,axis=0)
    aag030_2NN=np.amin(crse_runsag30_2NN,axis=0)
    aag030_3NN=np.amin(crse_runsag30_3NN,axis=0)
    aag030_4NN=np.amin(crse_runsag30_4NN,axis=0)
    aag030_5NN=np.amin(crse_runsag30_5NN,axis=0)
    aag030_6NN=np.amin(crse_runsag30_6NN,axis=0)
#    aag030_7NN=np.amin(crse_runsag30_7NN,axis=0)
    
    aag060_1NN=np.amin(crse_runsag60_1NN,axis=0)
    aag060_2NN=np.amin(crse_runsag60_2NN,axis=0)
    aag060_3NN=np.amin(crse_runsag60_3NN,axis=0)
    aag060_4NN=np.amin(crse_runsag60_4NN,axis=0)
    aag060_5NN=np.amin(crse_runsag60_5NN,axis=0)
    aag060_6NN=np.amin(crse_runsag60_6NN,axis=0)
#    aag060_7NN=np.amin(crse_runsag60_7NN,axis=0)
    
    aag090_1NN=np.amin(crse_runsag90_1NN,axis=0)
    aag090_2NN=np.amin(crse_runsag90_2NN,axis=0)
    aag090_3NN=np.amin(crse_runsag90_3NN,axis=0)
    aag090_4NN=np.amin(crse_runsag90_4NN,axis=0)
    aag090_5NN=np.amin(crse_runsag90_5NN,axis=0)
    aag090_6NN=np.amin(crse_runsag90_6NN,axis=0)
#    aag090_7NN=np.amin(crse_runsag90_7NN,axis=0)
    
    aag120_1NN=np.amin(crse_runsag120_1NN,axis=0)
    aag120_2NN=np.amin(crse_runsag120_2NN,axis=0)
    aag120_3NN=np.amin(crse_runsag120_3NN,axis=0)
    aag120_4NN=np.amin(crse_runsag120_4NN,axis=0)
    aag120_5NN=np.amin(crse_runsag120_5NN,axis=0)
    aag120_6NN=np.amin(crse_runsag120_6NN,axis=0)
#    aag120_7NN=np.amin(crse_runsag120_7NN,axis=0)
    
    aag180_1NN=np.amin(crse_runsag180_1NN,axis=0)
    aag180_2NN=np.amin(crse_runsag180_2NN,axis=0)
    aag180_3NN=np.amin(crse_runsag180_3NN,axis=0)
    aag180_4NN=np.amin(crse_runsag180_4NN,axis=0)
    aag180_5NN=np.amin(crse_runsag180_5NN,axis=0)
    aag180_6NN=np.amin(crse_runsag180_6NN,axis=0)
#    aag180_7NN=np.amin(crse_runsag180_7NN,axis=0)
    
    adf030_1NN=np.amin(crse_runsdf30_1NN,axis=0)
    adf030_2NN=np.amin(crse_runsdf30_2NN,axis=0)
    adf030_3NN=np.amin(crse_runsdf30_3NN,axis=0)
    
    adf060_1NN=np.amin(crse_runsdf60_1NN,axis=0)
    adf060_2NN=np.amin(crse_runsdf60_2NN,axis=0)
    adf060_3NN=np.amin(crse_runsdf60_3NN,axis=0)
    
    adf090_1NN=np.amin(crse_runsdf90_1NN,axis=0)
    adf090_2NN=np.amin(crse_runsdf90_2NN,axis=0)
    adf090_3NN=np.amin(crse_runsdf90_3NN,axis=0)
    
    adf120_1NN=np.amin(crse_runsdf120_1NN,axis=0)
    adf120_2NN=np.amin(crse_runsdf120_2NN,axis=0)
    adf120_3NN=np.amin(crse_runsdf120_3NN,axis=0)
    
    adf180_1NN=np.amin(crse_runsdf180_1NN,axis=0)
    adf180_2NN=np.amin(crse_runsdf180_2NN,axis=0)
    adf180_3NN=np.amin(crse_runsdf180_3NN,axis=0)
    
    ahrINS_DR=np.amin(crse_runshrINS_DR,axis=0)
    
    ara_1INS_DR=np.amin(crse_runsra_1INS_DR,axis=0)
    ara_2INS_DR=np.amin(crse_runsra_2INS_DR,axis=0)
    
    acia_1INS_DR=np.amin(crse_runscia_1INS_DR,axis=0)
    acia_2INS_DR=np.amin(crse_runscia_2INS_DR,axis=0)
    
    
    ahb_1INS_DR=np.amin(crse_runshb_1INS_DR,axis=0)
    ahb_2INS_DR=np.amin(crse_runshb_2INS_DR,axis=0)
    
    aslr_1INS_DR=np.amin(crse_runsslr_1INS_DR,axis=0)
    aslr_2INS_DR=np.amin(crse_runsslr_2INS_DR,axis=0)
    aslr_3INS_DR=np.amin(crse_runsslr_3INS_DR,axis=0)
    
    awr_1INS_DR=np.amin(crse_runswr_1INS_DR,axis=0)
    awr_2INS_DR=np.amin(crse_runswr_2INS_DR,axis=0)
    awr_3INS_DR=np.amin(crse_runswr_3INS_DR,axis=0)
    
    aag030_1INS_DR=np.amin(crse_runsag30_1INS_DR,axis=0)
    aag030_2INS_DR=np.amin(crse_runsag30_2INS_DR,axis=0)
    aag030_3INS_DR=np.amin(crse_runsag30_3INS_DR,axis=0)
    aag030_4INS_DR=np.amin(crse_runsag30_4INS_DR,axis=0)
    aag030_5INS_DR=np.amin(crse_runsag30_5INS_DR,axis=0)    
    aag030_6INS_DR=np.amin(crse_runsag30_6INS_DR,axis=0)
     
    aag060_1INS_DR=np.amin(crse_runsag60_1INS_DR,axis=0)
    aag060_2INS_DR=np.amin(crse_runsag60_2INS_DR,axis=0)    
    aag060_3INS_DR=np.amin(crse_runsag60_3INS_DR,axis=0)    
    aag060_4INS_DR=np.amin(crse_runsag60_4INS_DR,axis=0)
    aag060_5INS_DR=np.amin(crse_runsag60_5INS_DR,axis=0)    
    aag060_6INS_DR=np.amin(crse_runsag60_6INS_DR,axis=0)    
    
    aag090_1INS_DR=np.amin(crse_runsag90_1INS_DR,axis=0)
    aag090_2INS_DR=np.amin(crse_runsag90_2INS_DR,axis=0)    
    aag090_3INS_DR=np.amin(crse_runsag90_3INS_DR,axis=0)
    aag090_4INS_DR=np.amin(crse_runsag90_4INS_DR,axis=0)
    aag090_5INS_DR=np.amin(crse_runsag90_5INS_DR,axis=0)
    aag090_6INS_DR=np.amin(crse_runsag90_6INS_DR,axis=0)    
    
    aag120_1INS_DR=np.amin(crse_runsag120_1INS_DR,axis=0)
    aag120_2INS_DR=np.amin(crse_runsag120_2INS_DR,axis=0)
    aag120_3INS_DR=np.amin(crse_runsag120_3INS_DR,axis=0)
    aag120_4INS_DR=np.amin(crse_runsag120_4INS_DR,axis=0)
    aag120_5INS_DR=np.amin(crse_runsag120_5INS_DR,axis=0)
    aag120_6INS_DR=np.amin(crse_runsag120_6INS_DR,axis=0)
    
    aag180_1INS_DR=np.amin(crse_runsag180_1INS_DR,axis=0)
    aag180_2INS_DR=np.amin(crse_runsag180_2INS_DR,axis=0)
    aag180_3INS_DR=np.amin(crse_runsag180_3INS_DR,axis=0)
    aag180_4INS_DR=np.amin(crse_runsag180_4INS_DR,axis=0)
    aag180_5INS_DR=np.amin(crse_runsag180_5INS_DR,axis=0)
    aag180_6INS_DR=np.amin(crse_runsag180_6INS_DR,axis=0)
    
    adf030_1INS_DR=np.amin(crse_runsdf30_1INS_DR,axis=0)
    adf030_2INS_DR=np.amin(crse_runsdf30_2INS_DR,axis=0)    
    adf030_3INS_DR=np.amin(crse_runsdf30_3INS_DR,axis=0) 
     
    adf060_1INS_DR=np.amin(crse_runsdf60_1INS_DR,axis=0)
    adf060_2INS_DR=np.amin(crse_runsdf60_2INS_DR,axis=0)   
    adf060_3INS_DR=np.amin(crse_runsdf60_3INS_DR,axis=0) 
    
    adf090_1INS_DR=np.amin(crse_runsdf90_1INS_DR,axis=0)
    adf090_2INS_DR=np.amin(crse_runsdf90_2INS_DR,axis=0)  
    adf090_3INS_DR=np.amin(crse_runsdf90_3INS_DR,axis=0) 
    
    adf120_1INS_DR=np.amin(crse_runsdf120_1INS_DR,axis=0)
    adf120_2INS_DR=np.amin(crse_runsdf120_2INS_DR,axis=0)   
    adf120_3INS_DR=np.amin(crse_runsdf120_3INS_DR,axis=0)
    
    adf180_1INS_DR=np.amin(crse_runsdf180_1INS_DR,axis=0)
    adf180_2INS_DR=np.amin(crse_runsdf180_2INS_DR,axis=0)   
    adf180_3INS_DR=np.amin(crse_runsdf180_3INS_DR,axis=0) 
    
    dhrNN=np.amin(cae_runshrNN,axis=0)
    
    dra_1NN=np.amin(cae_runsra_1NN,axis=0)
    dra_2NN=np.amin(cae_runsra_2NN,axis=0)
    
    dcia_1NN=np.amin(cae_runscia_1NN,axis=0)
    dcia_2NN=np.amin(cae_runscia_2NN,axis=0)
    
    dhb_1NN=np.amin(cae_runshb_1NN,axis=0)
    dhb_2NN=np.amin(cae_runshb_2NN,axis=0)
       
    dslr_1NN=np.amin(cae_runsslr_1NN,axis=0)
    dslr_2NN=np.amin(cae_runsslr_2NN,axis=0)
    dslr_3NN=np.amin(cae_runsslr_3NN,axis=0)
    
    dwr_1NN=np.amin(cae_runswr_1NN,axis=0)
    dwr_2NN=np.amin(cae_runswr_2NN,axis=0)
    dwr_3NN=np.amin(cae_runswr_3NN,axis=0)
    
    dag030_1NN=np.amin(cae_runsag30_1NN,axis=0)
    dag030_2NN=np.amin(cae_runsag30_2NN,axis=0)
    dag030_3NN=np.amin(cae_runsag30_3NN,axis=0)
    dag030_4NN=np.amin(cae_runsag30_4NN,axis=0)
    dag030_5NN=np.amin(cae_runsag30_5NN,axis=0)
    dag030_6NN=np.amin(cae_runsag30_6NN,axis=0)
    
    dag060_1NN=np.amin(cae_runsag60_1NN,axis=0)
    dag060_2NN=np.amin(cae_runsag60_2NN,axis=0)
    dag060_3NN=np.amin(cae_runsag60_3NN,axis=0)
    dag060_4NN=np.amin(cae_runsag60_4NN,axis=0)
    dag060_5NN=np.amin(cae_runsag60_5NN,axis=0)
    dag060_6NN=np.amin(cae_runsag60_6NN,axis=0)
    
    dag090_1NN=np.amin(cae_runsag90_1NN,axis=0)
    dag090_2NN=np.amin(cae_runsag90_2NN,axis=0)
    dag090_3NN=np.amin(cae_runsag90_3NN,axis=0)
    dag090_4NN=np.amin(cae_runsag90_4NN,axis=0)
    dag090_5NN=np.amin(cae_runsag90_5NN,axis=0)
    dag090_6NN=np.amin(cae_runsag90_6NN,axis=0)
    
    dag120_1NN=np.amin(cae_runsag120_1NN,axis=0)
    dag120_2NN=np.amin(cae_runsag120_2NN,axis=0)
    dag120_3NN=np.amin(cae_runsag120_3NN,axis=0)
    dag120_4NN=np.amin(cae_runsag120_4NN,axis=0)
    dag120_5NN=np.amin(cae_runsag120_5NN,axis=0)
    dag120_6NN=np.amin(cae_runsag120_6NN,axis=0)
    
    dag180_1NN=np.amin(cae_runsag180_1NN,axis=0)
    dag180_2NN=np.amin(cae_runsag180_2NN,axis=0)
    dag180_3NN=np.amin(cae_runsag180_3NN,axis=0)
    dag180_4NN=np.amin(cae_runsag180_4NN,axis=0)
    dag180_5NN=np.amin(cae_runsag180_5NN,axis=0)
    dag180_6NN=np.amin(cae_runsag180_6NN,axis=0)
    
    ddf030_1NN=np.amin(cae_runsdf30_1NN,axis=0)
    ddf030_2NN=np.amin(cae_runsdf30_2NN,axis=0)
    ddf030_3NN=np.amin(cae_runsdf30_3NN,axis=0)
    
    ddf060_1NN=np.amin(cae_runsdf60_1NN,axis=0)
    ddf060_2NN=np.amin(cae_runsdf60_2NN,axis=0)
    ddf060_3NN=np.amin(cae_runsdf60_3NN,axis=0)
    
    ddf090_1NN=np.amin(cae_runsdf90_1NN,axis=0)
    ddf090_2NN=np.amin(cae_runsdf90_2NN,axis=0)
    ddf090_3NN=np.amin(cae_runsdf90_3NN,axis=0)
    
    ddf120_1NN=np.amin(cae_runsdf120_1NN,axis=0)
    ddf120_2NN=np.amin(cae_runsdf120_2NN,axis=0)
    ddf120_3NN=np.amin(cae_runsdf120_3NN,axis=0)
    
    ddf180_1NN=np.amin(cae_runsdf180_1NN,axis=0)
    ddf180_2NN=np.amin(cae_runsdf180_2NN,axis=0)
    ddf180_3NN=np.amin(cae_runsdf180_3NN,axis=0)
    
    dhrINS_DR=np.amin(cae_runshrINS_DR,axis=0)
    
    dra_1INS_DR=np.amin(cae_runsra_1INS_DR,axis=0)
    dra_2INS_DR=np.amin(cae_runsra_2INS_DR,axis=0)
    
    dcia_1INS_DR=np.amin(cae_runscia_1INS_DR,axis=0)
    dcia_2INS_DR=np.amin(cae_runscia_2INS_DR,axis=0)
    
    
    
    dhrNN=np.amin(cae_runshrNN,axis=0)
    
    dhb_1INS_DR=np.amin(cae_runshb_1INS_DR,axis=0)
    dhb_2INS_DR=np.amin(cae_runshb_2INS_DR,axis=0)
    
    dslr_1INS_DR=np.amin(cae_runsslr_1INS_DR,axis=0)
    dslr_2INS_DR=np.amin(cae_runsslr_2INS_DR,axis=0)
    dslr_3INS_DR=np.amin(cae_runsslr_3INS_DR,axis=0)
    
    dwr_1INS_DR=np.amin(cae_runswr_1INS_DR,axis=0)
    dwr_2INS_DR=np.amin(cae_runswr_2INS_DR,axis=0)
    dwr_3INS_DR=np.amin(cae_runswr_3INS_DR,axis=0)
    
    dag030_1INS_DR=np.amin(cae_runsag30_1INS_DR,axis=0)
    dag030_2INS_DR=np.amin(cae_runsag30_2INS_DR,axis=0)
    dag030_3INS_DR=np.amin(cae_runsag30_3INS_DR,axis=0)
    dag030_4INS_DR=np.amin(cae_runsag30_4INS_DR,axis=0)
    dag030_5INS_DR=np.amin(cae_runsag30_5INS_DR,axis=0)    
    dag030_6INS_DR=np.amin(cae_runsag30_6INS_DR,axis=0)
   
    
    dag060_1INS_DR=np.amin(cae_runsag60_1INS_DR,axis=0)
    dag060_2INS_DR=np.amin(cae_runsag60_2INS_DR,axis=0)    
    dag060_3INS_DR=np.amin(cae_runsag60_3INS_DR,axis=0)    
    dag060_4INS_DR=np.amin(cae_runsag60_4INS_DR,axis=0)
    dag060_5INS_DR=np.amin(cae_runsag60_5INS_DR,axis=0)    
    dag060_6INS_DR=np.amin(cae_runsag60_6INS_DR,axis=0)    

    
    dag090_1INS_DR=np.amin(cae_runsag90_1INS_DR,axis=0)
    dag090_2INS_DR=np.amin(cae_runsag90_2INS_DR,axis=0)    
    dag090_3INS_DR=np.amin(cae_runsag90_3INS_DR,axis=0)
    dag090_4INS_DR=np.amin(cae_runsag90_4INS_DR,axis=0)
    dag090_5INS_DR=np.amin(cae_runsag90_5INS_DR,axis=0)
    dag090_6INS_DR=np.amin(cae_runsag90_6INS_DR,axis=0)    

    
    dag120_1INS_DR=np.amin(cae_runsag120_1INS_DR,axis=0)
    dag120_2INS_DR=np.amin(cae_runsag120_2INS_DR,axis=0)
    dag120_3INS_DR=np.amin(cae_runsag120_3INS_DR,axis=0)
    dag120_4INS_DR=np.amin(cae_runsag120_4INS_DR,axis=0)
    dag120_5INS_DR=np.amin(cae_runsag120_5INS_DR,axis=0)
    dag120_6INS_DR=np.amin(cae_runsag120_6INS_DR,axis=0)

    
    dag180_1INS_DR=np.amin(cae_runsag180_1INS_DR,axis=0)
    dag180_2INS_DR=np.amin(cae_runsag180_2INS_DR,axis=0)
    dag180_3INS_DR=np.amin(cae_runsag180_3INS_DR,axis=0)
    dag180_4INS_DR=np.amin(cae_runsag180_4INS_DR,axis=0)
    dag180_5INS_DR=np.amin(cae_runsag180_5INS_DR,axis=0)
    dag180_6INS_DR=np.amin(cae_runsag180_6INS_DR,axis=0)

    
    ddf030_1INS_DR=np.amin(cae_runsdf30_1INS_DR,axis=0)
    ddf030_2INS_DR=np.amin(cae_runsdf30_2INS_DR,axis=0)    
    ddf030_3INS_DR=np.amin(cae_runsdf30_3INS_DR,axis=0) 
     
    ddf060_1INS_DR=np.amin(cae_runsdf60_1INS_DR,axis=0)
    ddf060_2INS_DR=np.amin(cae_runsdf60_2INS_DR,axis=0)   
    ddf060_3INS_DR=np.amin(cae_runsdf60_3INS_DR,axis=0)  
    
    ddf090_1INS_DR=np.amin(cae_runsdf90_1INS_DR,axis=0)
    ddf090_2INS_DR=np.amin(cae_runsdf90_2INS_DR,axis=0)  
    ddf090_3INS_DR=np.amin(cae_runsdf90_3INS_DR,axis=0) 
    
    ddf120_1INS_DR=np.amin(cae_runsdf120_1INS_DR,axis=0)
    ddf120_2INS_DR=np.amin(cae_runsdf120_2INS_DR,axis=0)   
    ddf120_3INS_DR=np.amin(cae_runsdf120_3INS_DR,axis=0)  
    
    ddf180_1INS_DR=np.amin(cae_runsdf180_1INS_DR,axis=0)
    ddf180_2INS_DR=np.amin(cae_runsdf180_2INS_DR,axis=0)   
    ddf180_3INS_DR=np.amin(cae_runsdf180_3INS_DR,axis=0) 
    
    
    bhrNN=np.reshape(ahrNN,(4,1))  
    braNN=np.concatenate((np.reshape(ara_1NN,(4,1)),np.reshape(ara_2NN,(4,1))),axis=0)  
    bciaNN=np.concatenate((np.reshape(acia_1NN,(4,1)),np.reshape(acia_2NN,(4,1))),axis=0)  
    bhbNN=np.concatenate((np.reshape(ahb_1NN,(4,1)),np.reshape(ahb_2NN,(4,1))),axis=0)  
    bslrNN=np.concatenate((np.reshape(aslr_1NN,(4,1)),np.reshape(aslr_2NN,(4,1)),np.reshape(aslr_3NN,(4,1))),axis=0)  
    bwrNN=np.concatenate((np.reshape(awr_1NN,(4,1)),np.reshape(awr_2NN,(4,1)),np.reshape(awr_3NN,(4,1))),axis=0)  
    b030NN=np.concatenate((np.reshape(aag030_1NN,(4,1)),np.reshape(aag030_2NN,(4,1)),np.reshape(aag030_3NN,(4,1)),np.reshape(aag030_4NN,(4,1)),np.reshape(aag030_5NN,(4,1)),np.reshape(aag030_6NN,(4,1)),np.reshape(adf030_1NN,(4,1)),np.reshape(adf030_2NN,(4,1)),np.reshape(adf030_3NN,(4,1))),axis=0)  
    b060NN=np.concatenate((np.reshape(aag060_1NN,(4,1)),np.reshape(aag060_2NN,(4,1)),np.reshape(aag060_3NN,(4,1)),np.reshape(aag060_4NN,(4,1)),np.reshape(aag060_5NN,(4,1)),np.reshape(aag060_6NN,(4,1)),np.reshape(adf060_1NN,(4,1)),np.reshape(adf060_2NN,(4,1)),np.reshape(adf060_3NN,(4,1))),axis=0) 
    b120NN=np.concatenate((np.reshape(aag120_1NN,(4,1)),np.reshape(aag120_2NN,(4,1)),np.reshape(aag120_3NN,(4,1)),np.reshape(aag120_4NN,(4,1)),np.reshape(aag120_5NN,(4,1)),np.reshape(aag120_6NN,(4,1)),np.reshape(adf120_1NN,(4,1)),np.reshape(adf120_2NN,(4,1)),np.reshape(adf120_3NN,(4,1))),axis=0) 
    b180NN=np.concatenate((np.reshape(aag180_1NN,(4,1)),np.reshape(aag180_2NN,(4,1)),np.reshape(aag180_3NN,(4,1)),np.reshape(aag180_4NN,(4,1)),np.reshape(aag180_5NN,(4,1)),np.reshape(aag180_6NN,(4,1)),np.reshape(adf180_1NN,(4,1)),np.reshape(adf180_2NN,(4,1)),np.reshape(adf180_3NN,(4,1))),axis=0) 
     
    
    bhbINS_DR=np.concatenate((np.reshape(ahb_1INS_DR,(4,1)),np.reshape(ahb_2INS_DR,(4,1))),axis=0)
    bhrINS_DR=np.reshape(ahrINS_DR,(4,1))  
    braINS_DR=np.concatenate((np.reshape(ara_1INS_DR,(4,1)),np.reshape(ara_2INS_DR,(4,1))),axis=0)  
    bciaINS_DR=np.concatenate((np.reshape(acia_1INS_DR,(4,1)),np.reshape(acia_2INS_DR,(4,1))),axis=0)  
    bslrINS_DR=np.concatenate((np.reshape(aslr_1INS_DR,(4,1)),np.reshape(aslr_2INS_DR,(4,1)),np.reshape(aslr_3INS_DR,(4,1))),axis=0)  
    bwrINS_DR=np.concatenate((np.reshape(awr_1INS_DR,(4,1)),np.reshape(awr_2INS_DR,(4,1)),np.reshape(awr_3INS_DR,(4,1))),axis=0)  
    b030INS_DR=np.concatenate((np.reshape(aag030_1INS_DR,(4,1)),np.reshape(aag030_2INS_DR,(4,1)),np.reshape(aag030_3INS_DR,(4,1)),np.reshape(aag030_4INS_DR,(4,1)),np.reshape(aag030_5INS_DR,(4,1)),np.reshape(aag030_6INS_DR,(4,1)),np.reshape(adf030_1INS_DR,(4,1)),np.reshape(adf030_2INS_DR,(4,1)),np.reshape(adf030_3INS_DR,(4,1))),axis=0)  
    b060INS_DR=np.concatenate((np.reshape(aag060_1INS_DR,(4,1)),np.reshape(aag060_2INS_DR,(4,1)),np.reshape(aag060_3INS_DR,(4,1)),np.reshape(aag060_4INS_DR,(4,1)),np.reshape(aag060_5INS_DR,(4,1)),np.reshape(aag060_6INS_DR,(4,1)),np.reshape(adf060_1INS_DR,(4,1)),np.reshape(adf060_2INS_DR,(4,1)),np.reshape(adf060_3INS_DR,(4,1))),axis=0) 
    b120INS_DR=np.concatenate((np.reshape(aag120_1INS_DR,(4,1)),np.reshape(aag120_2INS_DR,(4,1)),np.reshape(aag120_3INS_DR,(4,1)),np.reshape(aag120_4INS_DR,(4,1)),np.reshape(aag120_5INS_DR,(4,1)),np.reshape(aag120_6INS_DR,(4,1)),np.reshape(adf120_1INS_DR,(4,1)),np.reshape(adf120_2INS_DR,(4,1)),np.reshape(adf120_3INS_DR,(4,1))),axis=0)    
    b180INS_DR=np.concatenate((np.reshape(aag180_1INS_DR,(4,1)),np.reshape(aag180_2INS_DR,(4,1)),np.reshape(aag180_3INS_DR,(4,1)),np.reshape(aag180_4INS_DR,(4,1)),np.reshape(aag180_5INS_DR,(4,1)),np.reshape(aag180_6INS_DR,(4,1)),np.reshape(adf180_1INS_DR,(4,1)),np.reshape(adf180_2INS_DR,(4,1)),np.reshape(adf180_3INS_DR,(4,1))),axis=0)    
    
    ehrNN=np.reshape(dhrNN,(4,1))  
    eraNN=np.concatenate((np.reshape(dra_1NN,(4,1)),np.reshape(dra_2NN,(4,1))),axis=0)  
    eciaNN=np.concatenate((np.reshape(dcia_1NN,(4,1)),np.reshape(dcia_2NN,(4,1))),axis=0)  
    ehbNN=np.concatenate((np.reshape(dhb_1NN,(4,1)),np.reshape(dhb_2NN,(4,1))),axis=0)  
    eslrNN=np.concatenate((np.reshape(dslr_1NN,(4,1)),np.reshape(dslr_2NN,(4,1)),np.reshape(dslr_3NN,(4,1))),axis=0)  
    ewrNN=np.concatenate((np.reshape(dwr_1NN,(4,1)),np.reshape(dwr_2NN,(4,1)),np.reshape(dwr_3NN,(4,1))),axis=0)  
    e030NN=np.concatenate((np.reshape(dag030_1NN,(4,1)),np.reshape(dag030_2NN,(4,1)),np.reshape(dag030_3NN,(4,1)),np.reshape(dag030_4NN,(4,1)),np.reshape(dag030_5NN,(4,1)),np.reshape(dag030_6NN,(4,1)),np.reshape(ddf030_1NN,(4,1)),np.reshape(ddf030_2NN,(4,1)),np.reshape(ddf030_3NN,(4,1))),axis=0)  
    e060NN=np.concatenate((np.reshape(dag060_1NN,(4,1)),np.reshape(dag060_2NN,(4,1)),np.reshape(dag060_3NN,(4,1)),np.reshape(dag060_4NN,(4,1)),np.reshape(dag060_5NN,(4,1)),np.reshape(dag060_6NN,(4,1)),np.reshape(ddf060_1NN,(4,1)),np.reshape(ddf060_2NN,(4,1)),np.reshape(ddf060_3NN,(4,1))),axis=0) 
    e120NN=np.concatenate((np.reshape(dag120_1NN,(4,1)),np.reshape(dag120_2NN,(4,1)),np.reshape(dag120_3NN,(4,1)),np.reshape(dag120_4NN,(4,1)),np.reshape(dag120_5NN,(4,1)),np.reshape(dag120_6NN,(4,1)),np.reshape(ddf120_1NN,(4,1)),np.reshape(ddf120_2NN,(4,1)),np.reshape(ddf120_3NN,(4,1))),axis=0) 
    e180NN=np.concatenate((np.reshape(dag180_1NN,(4,1)),np.reshape(dag180_2NN,(4,1)),np.reshape(dag180_3NN,(4,1)),np.reshape(dag180_4NN,(4,1)),np.reshape(dag180_5NN,(4,1)),np.reshape(dag180_6NN,(4,1)),np.reshape(ddf180_1NN,(4,1)),np.reshape(ddf180_2NN,(4,1)),np.reshape(ddf180_3NN,(4,1))),axis=0) 
    
    ehbINS_DR=np.concatenate((np.reshape(dhb_1INS_DR,(4,1)),np.reshape(dhb_2INS_DR,(4,1))),axis=0)      
    ehrINS_DR=np.reshape(dhrINS_DR,(4,1))
    eraINS_DR=np.concatenate((np.reshape(dra_1INS_DR,(4,1)),np.reshape(dra_2INS_DR,(4,1))),axis=0)  
    eciaINS_DR=np.concatenate((np.reshape(dcia_1INS_DR,(4,1)),np.reshape(dcia_2INS_DR,(4,1))),axis=0)  
    eslrINS_DR=np.concatenate((np.reshape(dslr_1INS_DR,(4,1)),np.reshape(dslr_2INS_DR,(4,1)),np.reshape(dslr_3INS_DR,(4,1))),axis=0)  
    ewrINS_DR=np.concatenate((np.reshape(dwr_1INS_DR,(4,1)),np.reshape(dwr_2INS_DR,(4,1)),np.reshape(dwr_3INS_DR,(4,1))),axis=0)  
    e030INS_DR=np.concatenate((np.reshape(dag030_1INS_DR,(4,1)),np.reshape(dag030_2INS_DR,(4,1)),np.reshape(dag030_3INS_DR,(4,1)),np.reshape(dag030_4INS_DR,(4,1)),np.reshape(dag030_5INS_DR,(4,1)),np.reshape(dag030_6INS_DR,(4,1)),np.reshape(ddf030_1INS_DR,(4,1)),np.reshape(ddf030_2INS_DR,(4,1)),np.reshape(ddf030_3INS_DR,(4,1))),axis=0)  
    e060INS_DR=np.concatenate((np.reshape(dag060_1INS_DR,(4,1)),np.reshape(dag060_2INS_DR,(4,1)),np.reshape(dag060_3INS_DR,(4,1)),np.reshape(dag060_4INS_DR,(4,1)),np.reshape(dag060_5INS_DR,(4,1)),np.reshape(dag060_6INS_DR,(4,1)),np.reshape(ddf060_1INS_DR,(4,1)),np.reshape(ddf060_2INS_DR,(4,1)),np.reshape(ddf060_3INS_DR,(4,1))),axis=0) 
    e120INS_DR=np.concatenate((np.reshape(dag120_1INS_DR,(4,1)),np.reshape(dag120_2INS_DR,(4,1)),np.reshape(dag120_3INS_DR,(4,1)),np.reshape(dag120_4INS_DR,(4,1)),np.reshape(dag120_5INS_DR,(4,1)),np.reshape(dag120_6INS_DR,(4,1)),np.reshape(ddf120_1INS_DR,(4,1)),np.reshape(ddf120_2INS_DR,(4,1)),np.reshape(ddf120_3INS_DR,(4,1))),axis=0)     
    e180INS_DR=np.concatenate((np.reshape(dag180_1INS_DR,(4,1)),np.reshape(dag180_2INS_DR,(4,1)),np.reshape(dag180_3INS_DR,(4,1)),np.reshape(dag180_4INS_DR,(4,1)),np.reshape(dag180_5INS_DR,(4,1)),np.reshape(dag180_6INS_DR,(4,1)),np.reshape(ddf180_1INS_DR,(4,1)),np.reshape(ddf180_2INS_DR,(4,1)),np.reshape(ddf180_3INS_DR,(4,1))),axis=0)     
    

    
