##########################################################
# Charcoal carbon flux module.                           #
# Xinyuan Wei                                            #
# 2021/06/03                                             #
##########################################################

def charcoal_CFlux (ty,char_C,dc1,dc2):
    
    # ty:         total years
    # dc1:        charcoal decay parameter 1
    # dc2:        charcoal decay parameter 2
    
    charcoal_yrA=[]   # Current year, accumulated charcoal carbon.
    charcoal_yrD=[]   # Annual decayed charcoal carbon.
    
    yr_A=0
    
    for i in range (ty):
        
        yr_A=yr_A+char_C.at[i]
        yr_D=yr_A*dc1*dc2
        yr_A=yr_A-yr_D
        
        charcoal_yrA.append(yr_A)
        charcoal_yrD.append(yr_D)
    
    # Return:
    # the charcoal pool size in current year
    # decayed carbon.
    return(charcoal_yrA,charcoal_yrD)        
    