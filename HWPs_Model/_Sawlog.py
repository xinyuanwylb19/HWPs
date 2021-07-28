##########################################################
# Sawlog Carbon flux module.                             #
# Xinyuan Wei                                            #
# 2021/05/11                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
##########################################################
# Building construction carbon flux module.              #
##########################################################

def BConstruction_CFlux (ty,bco_C,dp1,dp2,dp3,rp1,rp2):

    # ty:      total years
    # bco_C:   annual sawlog used to make furniture
    # dp1:     building consctruction disposal rate parameter 1
    # dp2:     building consctruction disposal rate parameter 2
    # dp3:     building consctruction disposal rate parameter 3
    # rp1:     building consctruction recycling rate parameter 1
    # rp2:     building consctruction recycling rate parameter 2
    
    bco_yrC=[] # Annual building construction carbon production.
    bco_yrA=[] # Current year, the accumulated building construction carbon.
    bco_yrD=[] # Annual building construction carbon disposed.
    bco_yrR=[] # Annual building construction carbon recycled.
    bco_yrL=[] # Annual building construction carbon disposed to landfill.

    # Building construction disposal rate.
    def bco_dr(yr):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp((-dp2*math.pow((yr-dp3),2))/dp3)
        return(part1*part2) 
    
    # Annual building construction production. 
    bco_yrC=bco_C
    
    # Accumulated building construction carbon.
    for i in range (ty): 
        # Current year, the accumulated building construction carbon.
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=bco_C.at[j]
                lfr=integrate.quad(bco_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=bco_C.at[int(i-dp3+j)]
               lfr=integrate.quad(bco_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A      
        
        bco_yrA.append(acc_A)       
    
    # Building construction carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=bco_C.at[j]
                dfr=bco_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=bco_C.at[int(i-dp3+j)]
               dfr=bco_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D
   
        bco_yrD.append(acc_D)
        
    # Building construction carbon recycled.
    for i in range (ty):
        temp_R=0
        # Building construction recycling rate.
        bcr=math.log(i+rp1)/rp2
        
        # Annual recycled building construction carbon.
        temp_R=bcr*bco_yrD[i]
        
        bco_yrR.append(temp_R)
        
    # Building construction carbon disposed to landfill.
    for i in range (ty):
        temp_L=bco_yrD[i]-bco_yrR[i]
        bco_yrL.append(temp_L)

    # Return:
    # annual building construction carbon production
    # accumulated building construction carbon
    # disposed building construction carbon
    # recycled building construction carbon
    # disposed building construction carbon to landfill
    
    return(bco_yrC,bco_yrA,bco_yrD,bco_yrR,bco_yrL)

#%%
##########################################################
# Exterior Construction carbon flux module.              #
##########################################################

def EConstruction_CFlux (ty,eco_C,dp1,dp2,dp3):
    
    # ty:       total years
    # eco_C:    annual sawlog used to make furniture
    # dp1:      exterior consctruction disposal rate parameter 1
    # dp2:      exterior consctruction disposal rate parameter 2
    # dp3:      exterior consctruction disposal rate parameter 3
    
    eco_yrC=[] # Annual exterior construction carbon production.
    eco_yrA=[] # Current year, the accumulated exterior construction carbon.
    eco_yrL=[] # Annual exterior construction carbon disposed to landfill.

    # Exterior construction disposal rate.
    def eco_dr(yr):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp((-dp2*math.pow((yr-dp3),2))/dp3)
        return(part1*part2) 

    # Annual exterior construction production. 
    eco_yrC=eco_C
             
    # Accumulated exterior construction carbon.
    for i in range (ty): 
        # Current year, the accumulated exterior carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=eco_C.at[j]
                lfr=integrate.quad(eco_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=eco_C.at[int(i-dp3+j)]
               lfr=integrate.quad(eco_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A      
        
        eco_yrA.append(acc_A)       
    
    # Exterior construction carbon disposed to landfill.
    for i in range (ty):
        acc_L=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_L=0
                yr_C=eco_C.at[j]
                dfr=eco_dr(i-j+1)
                temp_L=yr_C*dfr
                acc_L=acc_L+temp_L
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=eco_C.at[int(i-dp3+j)]
               dfr=eco_dr(dp3-j+1)
               temp_L=yr_C*dfr
               acc_L=acc_L+temp_L
  
        eco_yrL.append(acc_L)
        
    # Return:
    # annual exterior construction carbon production
    # accumulated building construction carbon
    # disposed exterior construction carbon

    return(eco_yrC,eco_yrA,eco_yrL)   

#%%
##########################################################
# Home application carbon flux module.                          #
##########################################################

def HomeA_CFlux (ty,hma_C,dp1,dp2,dp3,rp1,rp2):
    
    # ty:      total years
    # hma_C:   annual sawlog used to make home application
    # dp1:     home application disposal rate parameter 1 
    # dp2:     home application disposal rate parameter 2 
    # dp3:     home application disposal rate parameter 3 (service life)
    # rp1:     home application recycling rate parameter 1
    # rp2:     home application recycling rate parameter 2
    
    hma_yrC=[] # Annual home application carbon production.
    hma_yrA=[] # Current year, the accumulated home application carbon.
    hma_yrD=[] # Annual home application carbon disposed to landfill.
    hma_yrR=[] # Annual home application carbon recycled.
    hma_yrL=[] # Annual home application carbon disposed to landfill.
    
    # Annual home application production.
    hma_yrC=hma_C
    
    # Home application disposal rate.
    # TSD: time since production
    def hma_dr(TSP):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp((-dp2*math.pow((TSP-dp3),2))/dp3)
        return(part1*part2)
             
    # Accumulated home application carbon.
    for i in range (ty): 
        # Current year, the accumulated home application carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=hma_C.at[j]
                lfr=integrate.quad(hma_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=hma_C.at[int(i-dp3+j)]
               lfr=integrate.quad(hma_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A      
        
        hma_yrA.append(acc_A)       
    
    # Home application carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=hma_C.at[j]
                dfr=hma_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D

        if i>dp3:
           for j in range (int(dp3)):
               temp_D=0
               yr_C=hma_C.at[int(i-dp3+j)]
               dfr=hma_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D

        hma_yrD.append(acc_D)
        
    # Home application carbon recycled.
    for i in range (ty):
        # Home application recycling rate.
        har=math.log(i+rp1)/rp2
        
        # Annual recycled home application.
        temp_R=hma_yrD[i]*har
        hma_yrR.append(temp_R)

    # Home application carbon disposed to landfill.
    for i in range (ty):
        temp_L=hma_yrD[i]-hma_yrR[i]
        hma_yrL.append(temp_L) 
             
    # Return:
    # annual home application carbon production
    # accumulated home application carbon
    # disposed home application carbon
    # recycled home application carbon
    # disposed home application carbon to landfill
    return(hma_yrC,hma_yrA,hma_yrD,hma_yrR,hma_yrL)