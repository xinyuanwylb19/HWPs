##########################################################
# Biomass Carbon Flux Module                             #
# Xinyuan Wei                                            #
# 2021/7/21                                              #
##########################################################

#%%
##########################################################
# Biochar carbon flux module.                            #
##########################################################

def Biochar_CFlux (ty,bc_data,bc_pce):
    
    # yr:        total years
    # bc_data:   annual biomass used to produce biochar
    # bc_pce:    biochar production efficiency  
    
    biochar_yrC=[]  # Annual biochar carbon production.
    biochar_yrE=[]  # Annual carbon emission to produce biochar.
    
    # Biochar carbon flux.
    for i in range (ty):
        
        # The biochar production.
        yr_C=bc_data.at[i]*(1-bc_pce)
        
        # Annual carbon emission in producing biochar.
        yr_E=bc_data.at[i]*bc_pce
        
        biochar_yrC.append(yr_C)
        biochar_yrE.append(yr_E)
        
    # Return:
    # annual biochar production
    # annual carbon emission in pruducing biochar. 
    return(biochar_yrC,biochar_yrE)
#%%
##########################################################
# Industrial firewood carbon flux module.                #
# The industrial firewood is used up in that year.       # 
# It has charcoal production.                            #
##########################################################

def IFirewood_CFlux (ty,ifw_data,ifw_bur):
    
    # yr:       total years
    # ifw_C:    annual indtustrial firewood carbon
    # ifw_bur:  indtustrial firewood burning efficiency (rest C is charcoal).
    
    ifirewood_yrE=[]  # Annual carbon emission from industrial firewood.
    ifirewood_yrH=[]  # Annual charcoal production from industrial firewood.
    
    for i in range (ty):    
            
        yr_ifC=ifw_data.at[i]
        
        # Annual carbon emission from burned industrial firewood.
        yr_E=yr_ifC*ifw_bur
            
        # Annual burned industrial firewood to charcoal.
        yr_H=yr_ifC*(1-ifw_bur)
            
        ifirewood_yrE.append(yr_E)
        ifirewood_yrH.append(yr_H)
    
    # Return:
    # annual carbon emission
    # annual charcoal production.
    return(ifirewood_yrE,ifirewood_yrH) 
#%%
##########################################################
# Residential firewood carbon flux module.               #
# The residential firewood is used up in that year.      # 
# It does not has charcoal production.                   #
##########################################################

def RFirewood_CFlux (ty,rfw_C,rfw_bur):
    
    rfirewood_yrE=[]  # Annual carbon emission from residential firewood.
    rfirewood_yrH=[]  # Annual charcoal production from residential firewood.
    
    # Annual residential firewood carbon flux.
    for i in range (ty):    
        
        # Annual carbon emission from burned residential firewood.
        yr_E=rfw_C.at[i]*rfw_bur         
        
        # Annual burned residential firewood to charcoal.
        yr_H=rfw_C.at[i]*(1-rfw_bur)
        
        rfirewood_yrE.append(yr_E)
        rfirewood_yrH.append(yr_H)
    
    # Return:
    # annual carbon emission.
    return(rfirewood_yrE,rfirewood_yrH) 