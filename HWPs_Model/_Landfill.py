##########################################################
# Landfill carbon flux module.                           #
# Xinyuan Wei                                            #
# 2021/07/21                                             #
##########################################################
import math
import scipy.integrate as integrate

def Landfill_CFlux(ty,lf_pa,lf_bc,lf_ec,lf_ha,lf_pr,
                   pa1,pa2,bc1,bc2,ec1,ec2,ha1,ha2,pr1,pr2):
    
    # ty:         total years
    # lf_pa:      annual paper carbon disposed to landfill
    # pa1:        paper landfill decay parameter 1
    # pa2:        paper landfill decay parameter 2
    
    landfill_yrC=[]   # Annual landfill.
    landfill_yrA=[]   # Accumulated landfill carbon (carbon pool).
    landfill_yrD=[]   # Annual decayed landfill carbon.
    
    landfill_yrAPa=[] # Accumulated landfill paper carbon.
    landfill_yrDPa=[] # Decayed landfill paper carbon.
    
    landfill_yrABc=[] # Accumulated landfill building construction carbon.
    landfill_yrDBc=[] # Decayed landfill building construction carbon.

    landfill_yrAEc=[] # Accumulated landfill exterior construction carbon.
    landfill_yrDEc=[] # Decayed landfill exterior construction carbon.
    
    landfill_yrAHa=[] # Accumulated landfill home application carbon.
    landfill_yrDHa=[] # Decayed landfill home application carbon.

    landfill_yrAPr=[] # Accumulated landfill processing residuals carbon.
    landfill_yrDPr=[] # Decayed landfill processing residuals carbon.
    
    # Landfill paper decay rate.
    def lpa_d(TSD):
        part1=math.log(TSD)*pa1
        part2=pa2*math.sqrt(2*math.pi)
        return(part1/part2)

    # Landfill building construction decay rate.
    def lbc_d(TSD):
        part1=math.log(TSD)*bc1
        part2=bc2*math.sqrt(2*math.pi)
        return(part1/part2)

    # Landfill exterior construction decay function.
    def lec_d(TSD):
        part1=math.log(TSD)*ec1
        part2=ec2*math.sqrt(2*math.pi)
        return(part1/part2)
    
    # Landfill home application decay function.
    def lha_d(TSD):
        part1=math.log(TSD)*ha1
        part2=ha2*math.sqrt(2*math.pi)
        return(part1/part2)
  
    # Landfill processing residual decay function.
    def lpr_d(TSD):
        part1=math.log(TSD)*pr1
        part2=pr2*math.sqrt(2*math.pi)
        return(part1/part2)

#%%    
##########################################################
# Landfill paper carbon decay.                            #
##########################################################                

# Accumulated landfill paper carbon.
    for i in range (ty): 
        acc_A=0  
        if i<=pa2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_pa.at[j]
                fr=abs(integrate.quad(lpa_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>pa2:
           for j in range (int(pa2)):
               temp_A=0
               yr_C=lf_pa.at[int(i-pa2+j)]
               fr=abs(integrate.quad(lpa_d,0,pa2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        landfill_yrAPa.append(acc_A)
        
    # Current year, decayed paper landfill.     
    for i in range (ty):
        
        if i==0:
            yr_D=lf_pa[i]-landfill_yrAPa[i]     
            
        if i>0:
            yr_D=landfill_yrAPa[i-1]+lf_pa[i]-landfill_yrAPa[i]
            
        landfill_yrDPa.append(yr_D)

#%% 
##########################################################
# Landfill building construction carbon decay.            #
##########################################################                 
    # Accumulated landfill building construction carbon.
    for i in range (ty): 
        acc_A=0  
        if i<=bc2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_bc.at[j]
                fr=abs(integrate.quad(lbc_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>bc2:
           for j in range (int(bc2)):
               temp_A=0
               yr_C=lf_bc.at[int(i-bc2+j)]
               fr=abs(integrate.quad(lbc_d,0,bc2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        landfill_yrABc.append(acc_A)
        
    # Current year, decayed builfing construction landfill. 
    for i in range (ty):
        
        if i==0:
            yr_D=lf_bc[i]-landfill_yrABc[i]
          
        if i>0:
            yr_D=landfill_yrABc[i-1]+lf_bc[i]-landfill_yrABc[i]
   
        landfill_yrDBc.append(yr_D)

#%% 
##########################################################
# Landfill exterior construction carbon decay.            #
##########################################################                 
    # Accumulated landfill exterior construction carbon.
    for i in range (ty): 
        acc_A=0  
        if i<=ec2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_ec.at[j]
                fr=abs(integrate.quad(lec_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>ec2:
           for j in range (int(ec2)):
               temp_A=0
               yr_C=lf_ec.at[int(i-ec2+j)]
               fr=abs(integrate.quad(lec_d,0,ec2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      

        landfill_yrAEc.append(acc_A)
        
    # Current year, decayed building construction landfill. 
    for i in range (ty):
        
        if i==0:
            yr_D=lf_ec[i]-landfill_yrAEc[i]
              
        if i>0:
            yr_D=landfill_yrAEc[i-1]+lf_ec[i]-landfill_yrAEc[i]
            
        landfill_yrDEc.append(yr_D)

#%% 
##########################################################
# Landfill home application carbon decay.                 #
##########################################################                 
    # Accumulated landfill home application carbon.
    for i in range (ty): 
        acc_A=0  
        if i<=ha2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_ha.at[j]
                fr=abs(integrate.quad(lha_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>ha2:
           for j in range (int(ha2)):
               temp_A=0
               yr_C=lf_ha.at[int(i-ha2+j)]
               fr=abs(integrate.quad(lha_d,0,ha2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        landfill_yrAHa.append(acc_A)
        
    # Current year, decomposed builfing construction landfill. 
    for i in range (ty):
        
        if i==0:
            yr_D=lf_ha[i]-landfill_yrAHa[i]
        
        if i>0:
            yr_D=landfill_yrAHa[i-1]+lf_ha[i]-landfill_yrAHa[i]
            
        landfill_yrDHa.append(yr_D)

#%% 
##########################################################
# Landfill processing residual carbon decay.             #
##########################################################                 
    # Accumulated landfill processing residual carbon.
    for i in range (ty): 
        acc_A=0  
        if i<=pr2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_pr[j]
                fr=abs(integrate.quad(lpr_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>pr2:
           for j in range (int(pr2)):
               temp_A=0
               yr_C=lf_pr[int(i-pr2+j)]
               fr=abs(integrate.quad(lpr_d,0,pr2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        landfill_yrAPr.append(acc_A)
        
    # Current year, decayed processing residual landfill. 
    for i in range (ty):
        
        if i==0:
            yr_D=lf_pr[i]-landfill_yrAPr[i]
   
        if i>0:
            yr_D=landfill_yrAPr[i-1]+lf_pr[i]-landfill_yrAPr[i]

        landfill_yrDPr.append(yr_D)  
#%%         
    for i in range (ty):
        temp_yrC=lf_pa[i]+lf_bc[i]+lf_ec[i]+lf_ha[i]+lf_pr[i]
    
        temp_yrA=(landfill_yrAPa[i]+landfill_yrABc[i]+landfill_yrAEc[i]
                  +landfill_yrAHa[i]+landfill_yrAPr[i])
    
        temp_yrD=(landfill_yrDPa[i]+landfill_yrDBc[i]+landfill_yrDEc[i]
                  +landfill_yrDHa[i]+landfill_yrDPr[i])
        
        landfill_yrC.append(temp_yrC)
        landfill_yrA.append(temp_yrA)
        landfill_yrD.append(temp_yrD)
    
    # Return:
    # the annual carbon disposed to landfill
    # accumulated landfill carbon
    # annual decayed landfill carbon
    return(landfill_yrC,landfill_yrA,landfill_yrD)