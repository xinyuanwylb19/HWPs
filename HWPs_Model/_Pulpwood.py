##########################################################
# Pulpwood carbon flux module                            #
# Xinyuan Wei                                            #
# 2021/07/21                                             #
##########################################################
import scipy.integrate as integrate
import math

##########################################################
# Paper carbon flux module.                              #
##########################################################

def Paper_CFlux (ty,pap_C,dp1,dp2,dp3,rp1,rp2):
    
    # ty:      total years
    # pap_C:   annual paper production
    # dp1:     paper disposal rate parameter 1
    # dp2:     paper disposal rate parameter 2
    # dp3:     paper disposal rate parameter 3 (service life)
    # rp1:     paper recycling rate parameter 1
    # rp2:     paper recycling rate parameter 2

    
    paper_yrC=[]     # Annual paper carbon production.
    paper_yrA=[]     # Current year, the accumulated paper carbon.
    paper_yrD=[]     # Annual paper carbon disposed.
    paper_yrR=[]     # Annual paper carbon recycled.
    paper_yrL=[]     # Annual paper carbon disposed to landfill.
    
    # Annual paper production.
    paper_yrC=pap_C
    
    # Paper disposal rate.
    # TSD: time since production
    def pap_dr(TSP):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp(-dp2*math.pow((TSP-dp3),2)/dp3)
        return(part1*part2)
             
    # Accumulated paper carbon.
    for i in range (ty): 
        # Current year, the accumulated paper carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=pap_C[j]
                lfr=integrate.quad(pap_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
        
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=pap_C[int(i-dp3+j)]
               lfr=integrate.quad(pap_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A
 
        paper_yrA.append(acc_A)       
    
    # Paper carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=pap_C[j]
                dfr=pap_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_D=0
               yr_C=pap_C[int(i-dp3+j)]
               dfr=pap_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D
            
        paper_yrD.append(acc_D)
        
    # Paper carbon recycled.
    for i in range (ty):
        temp_R=0
        # Paper carbon recycling rate.
        prr=math.log(i+rp1)/rp2
        
        # Annual recycled paper carbon.
        temp_R=prr*paper_yrD[i]
        
        paper_yrR.append(temp_R)
        
    # Paper carbon disposed to landfill.
    for i in range (ty):
        temp_L=paper_yrD[i]-paper_yrR[i]
        paper_yrL.append(temp_L)
    
    # Return:
    # annual paper carbon production
    # accumulated paper carbon
    # disposed paper carbon
    # recycled paper carbon
    # disposed paper carbon to landfill
    
    return(paper_yrC,paper_yrA,paper_yrD,paper_yrR,paper_yrL)
