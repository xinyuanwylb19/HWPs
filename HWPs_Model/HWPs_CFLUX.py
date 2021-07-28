##########################################################
# Harvested Wood Products Carbon Flux Model (HWPs_CFLUX) #
# Developed by Xinyuan Wei                               #
# Updated 2021/07/15                                     #
# Version 1.0                                            #
##########################################################

import pandas as pd 
import math
import os 
import _Biomass as bs
import _Pulpwood as pl
import _Sawlog as sl
import _Landfill as lf
import _Charcoal as cc
#%% 
##########################################################
# Read harvested wood carbon data.                       #
##########################################################

# Scenario file.
sc='Scenario_4'
directory=os.getcwd()+chr(92)+sc
#print(directory)

# Read the harvested wood data file.
HW_filename=directory+chr(92)+'HWPs_Data.csv'
HW_data=pd.read_csv(HW_filename, sep=',')

# Read the products parameter file.
productsparams_file=directory+chr(92)+'HWPs_CFLUX_Params1.csv'
productsparams=pd.read_csv(productsparams_file, sep=',')

# Read the parameter file.
para_filename=directory+chr(92)+'HWPs_CFLUX_Params2.csv'
params=pd.read_csv(para_filename, sep=',')

#%% 
##########################################################
# Analyzed time period infomation.                       #
##########################################################

# Print the year information.
Year_list=HW_data.Year.unique()
total_yr=len(HW_data)
sy=HW_data['Year'].at[0]
ey=HW_data['Year'].at[total_yr-1]
print('The time period is ', sy,'-',ey,'.')
print(total_yr, 'years in total.')
print('')

#%% 
##########################################################
# Estimate the end use wood products.                    #
##########################################################

print ('Estimating end use wood products...')
print('')
# data_head=list(HW_data.columns)
# print(data_head)

result_arr=[]

for i in range(total_yr):
    temp=[]
    
    # Biomass carbon.
    biochar_pro=round(HW_data['Biomass'].at[i]*productsparams['B_bchar'].at[i])
    ifuel_pro=round(HW_data['Biomass'].at[i]*productsparams['B_ifuel'].at[i])
    rfuel_pro=round(HW_data['Biomass'].at[i]*productsparams['B_rfuel'].at[i])
    
    # Sapwood carbon.
    paper_r=productsparams['R_paper'].at[i]
    
    P_paper=round(HW_data['Pulpwood'].at[i]*productsparams['P_paper'].at[i])
    R_paper=round(P_paper/(1-paper_r)*paper_r)
    paper_pro=P_paper+R_paper
    
    ComB_r=productsparams['R_CB'].at[i]
    P_ComB=round(HW_data['Pulpwood'].at[i]*productsparams['P_CB'].at[i])
    R_ComB=round(P_ComB/(1-ComB_r)*ComB_r)
    ComB_pro=P_ComB+R_ComB
    ComB_BC_pro=ComB_pro*productsparams['ComB_BC'].at[i]
    ComB_HA_pro=ComB_pro*productsparams['ComB_HA'].at[i]
    
    P_PR=round(HW_data['Pulpwood'].at[i]*productsparams['P_PR'].at[i])   
    
    # Sawlog
    lumber_pro=round(HW_data['Sawlog'].at[i]*productsparams['S_Lumber'].at[i])
    veneer_pro=round(HW_data['Sawlog'].at[i]*productsparams['S_Veneer'].at[i])
    
    BC=productsparams['Construction'].at[i]*productsparams['Construction_B'].at[i]
    EC=productsparams['Construction'].at[i]*productsparams['Construction_E'].at[i]
    HA=productsparams['Home_Application'].at[i]
    
    BC_pro=round((lumber_pro+veneer_pro)*BC)+ComB_BC_pro
    EC_pro=round((lumber_pro+veneer_pro)*EC)
    HA_pro=round((lumber_pro+veneer_pro)*HA)+ComB_HA_pro
    
    S_PR=round(HW_data['Sawlog'].at[i]*productsparams['S_PR'].at[i])
    
    PR=P_PR+S_PR
    
    temp.append(HW_data['Year'].at[i])
    temp.append(HW_data['Harveted_Timber'].at[i])
    temp.append(HW_data['Biomass'].at[i])
    temp.append(HW_data['Pulpwood'].at[i])
    temp.append(HW_data['Sawlog'].at[i])
    
    temp.append(biochar_pro)
    temp.append(ifuel_pro)
    temp.append(rfuel_pro)
       
    temp.append(paper_pro)
    temp.append(ComB_pro)
    
    temp.append(lumber_pro)
    temp.append(veneer_pro)
    
    temp.append(BC_pro)
    temp.append(EC_pro)
    temp.append(HA_pro)

    temp.append(PR)
    
    result_arr.append(temp)
  
header1=['Year','Harveted_Timber','Biomass','Pulpwood','Sawlog',
         'Biochar','Residential_Fuel','Industry_Fuel',
         'Paper','Composite_Board','Lumber','Veneer',
         'Construction_B','Construction_E','Home_Application','Processing_Residual']

df=pd.DataFrame(data=result_arr)
df.to_csv(directory+chr(92)+'Results_Products.csv',index=False,header=header1)

#%% 
##########################################################
# Read carbon flux parameters.                           #
##########################################################

# Biomass parameters.
cha_pce=params.loc[params['Para_Name']=='cha_pce']['Value'].tolist()[0]
ifw_bur=params.loc[params['Para_Name']=='ifw_bur']['Value'].tolist()[0]                                                                    
rfw_bur=params.loc[params['Para_Name']=='rfw_bur']['Value'].tolist()[0]

# Paper parameters.
pap_dp1=params.loc[params['Para_Name']=='pap_dp1']['Value'].tolist()[0]
pap_dp2=params.loc[params['Para_Name']=='pap_dp2']['Value'].tolist()[0]
pap_dp3=params.loc[params['Para_Name']=='pap_dp3']['Value'].tolist()[0]
pap_rp1=params.loc[params['Para_Name']=='pap_rp1']['Value'].tolist()[0]
pap_rp2=params.loc[params['Para_Name']=='pap_rp2']['Value'].tolist()[0]
                                                                 
# Construction parameters (building and exterior).
bco_dp1=params.loc[params['Para_Name']=='bco_dp1']['Value'].tolist()[0]
bco_dp2=params.loc[params['Para_Name']=='bco_dp2']['Value'].tolist()[0]
bco_dp3=params.loc[params['Para_Name']=='bco_dp3']['Value'].tolist()[0]
bco_rp1=params.loc[params['Para_Name']=='bco_rp1']['Value'].tolist()[0]
bco_rp2=params.loc[params['Para_Name']=='bco_rp2']['Value'].tolist()[0]

eco_dp1=params.loc[params['Para_Name']=='eco_dp1']['Value'].tolist()[0]
eco_dp2=params.loc[params['Para_Name']=='eco_dp2']['Value'].tolist()[0]
eco_dp3=params.loc[params['Para_Name']=='eco_dp3']['Value'].tolist()[0]

# Home application parameters.
hma_dp1=params.loc[params['Para_Name']=='hma_dp1']['Value'].tolist()[0]
hma_dp2=params.loc[params['Para_Name']=='hma_dp2']['Value'].tolist()[0]
hma_dp3=params.loc[params['Para_Name']=='hma_dp3']['Value'].tolist()[0]
hma_rp1=params.loc[params['Para_Name']=='hma_rp1']['Value'].tolist()[0]
hma_rp2=params.loc[params['Para_Name']=='hma_rp2']['Value'].tolist()[0]

# Charcoal parameters.
cha_dc1=params.loc[params['Para_Name']=='cha_dc1']['Value'].tolist()[0]
cha_dc2=params.loc[params['Para_Name']=='cha_dc2']['Value'].tolist()[0]

# Landfill parameters.
ldf_pap1=params.loc[params['Para_Name']=='ldf_pap1']['Value'].tolist()[0]
ldf_pap2=params.loc[params['Para_Name']=='ldf_pap2']['Value'].tolist()[0]
ldf_bcp1=params.loc[params['Para_Name']=='ldf_bcp1']['Value'].tolist()[0]
ldf_bcp2=params.loc[params['Para_Name']=='ldf_bcp2']['Value'].tolist()[0]
ldf_ecp1=params.loc[params['Para_Name']=='ldf_ecp1']['Value'].tolist()[0]
ldf_ecp2=params.loc[params['Para_Name']=='ldf_ecp2']['Value'].tolist()[0]
ldf_hap1=params.loc[params['Para_Name']=='ldf_hap1']['Value'].tolist()[0]
ldf_hap2=params.loc[params['Para_Name']=='ldf_hap2']['Value'].tolist()[0]
ldf_prp1=params.loc[params['Para_Name']=='ldf_prp1']['Value'].tolist()[0]
ldf_prp2=params.loc[params['Para_Name']=='ldf_prp2']['Value'].tolist()[0]

# Processing residuals parameters.
pr_rp1=params.loc[params['Para_Name']=='pr_rp1']['Value'].tolist()[0]
pr_rp2=params.loc[params['Para_Name']=='pr_rp2']['Value'].tolist()[0]

#%% 
##########################################################
# Wood products                                          #
##########################################################

# Read the products data.
pd_file=directory+chr(92)+'Results_Products.csv'
pd_data=pd.read_csv(pd_file,sep=',')

bioc_C=pd_data['Biochar']
rfue_C=pd_data['Residential_Fuel'] 
ifue_C=pd_data['Industry_Fuel']

pape_C=pd_data['Paper']
conB_C=pd_data['Construction_B']
conE_C=pd_data['Construction_E']
hmap_C=pd_data['Home_Application']

#%% 
##########################################################
# Main function (products)                               #
##########################################################
def Main_Estimate1 ():
    results=[]
    temp=[]
    
    # Biochar.
    br_results=bs.Biochar_CFlux(total_yr,bioc_C,cha_pce)
    
    # Industrial firewood.
    if_results=bs.IFirewood_CFlux(total_yr,ifue_C,ifw_bur)
    
    # Residential fuel.
    rf_results=bs.RFirewood_CFlux(total_yr,rfue_C,rfw_bur)

    # Paper.
    pa_results=pl.Paper_CFlux(total_yr,pape_C,pap_dp1,pap_dp2,pap_dp3,pap_rp1,pap_rp2)
    
    # Building construction.
    bc_results=sl.BConstruction_CFlux(total_yr,conB_C,bco_dp1,bco_dp2,bco_dp3,bco_rp1,bco_rp2)
    
    # Building exterior.
    ec_results=sl.EConstruction_CFlux(total_yr,conE_C,eco_dp1,eco_dp2,eco_dp3)
    
    # Home application.
    ha_results=sl.HomeA_CFlux(total_yr,hmap_C,hma_dp1,hma_dp2,hma_dp3,hma_rp1,hma_rp2)
    
    for i in range (total_yr):
        
        temp=[]
        temp.append(HW_data['Year'].at[i])
        
        # Biochar
        temp.append(round(br_results[0][i]))
        temp.append(round(br_results[1][i]))
        
        # Industrial and residential firewood.
        temp.append(round(if_results[0][i]))        
        temp.append(round(if_results[1][i]))
        
        temp.append(round(rf_results[0][i]))
        temp.append(round(rf_results[1][i]))
        
        # Paper.
        temp.append(round(pa_results[0][i]))
        temp.append(round(pa_results[1][i]))
        temp.append(round(pa_results[2][i]))
        temp.append(round(pa_results[3][i]))
        temp.append(round(pa_results[4][i]))
        
        # Building and exterior construction.
        temp.append(round(bc_results[0][i]))
        temp.append(round(bc_results[1][i]))
        temp.append(round(bc_results[2][i]))
        temp.append(round(bc_results[3][i]))
        temp.append(round(bc_results[4][i]))

        temp.append(round(ec_results[0][i]))
        temp.append(round(ec_results[1][i]))    
        temp.append(round(ec_results[2][i]))
        
        # Home application
        temp.append(round(ha_results[0][i]))
        temp.append(round(ha_results[1][i]))
        temp.append(round(ha_results[2][i]))
        temp.append(round(ha_results[3][i]))
        temp.append(round(ha_results[4][i]))
        
        results.append(temp)
        
    header2=['Year','Biochar','Biochar_E',
             'IFuelwood_E','IFuelwood_Char','RFuelwood_E','RFuelwood_Char',
             'Paper_C','Paper_A','Paper_D','Paper_R','Paper_L',
             'BC_C','BC_A','BC_D','BC_R','BC_L','EC_C','EC_A','EC_L',
             'HA_C','HA_A','HA_D','HA_R','HA_L']
    df=pd.DataFrame(data=results)
    df.to_csv(directory+chr(92)+'Results_CFlux.csv',index=False,header=header2)
                   
Main_Estimate1 ()  

#%% 
##########################################################
# Main function 2                                        #
##########################################################
# Read the products data.
CFlux_file=directory+chr(92)+'Results_CFlux.csv'
CFlux_data=pd.read_csv(CFlux_file, sep=',')

# Charcoal.
Biochar_C=CFlux_data['Biochar']   
Ifwchar_C=CFlux_data['IFuelwood_Char']
Rfwchar_C=CFlux_data['RFuelwood_Char']

Tchar=Biochar_C+Ifwchar_C+Rfwchar_C

# Processing residuals recycling.
pr_R=[]
pr_D=[]
for i in range (total_yr):
    prrr=1-math.log(i+pr_rp1)/pr_rp2
    
    temp_Rpr=prrr*pd_data['Processing_Residual'][i]
    temp_Dpr=(1-prrr)*pd_data['Processing_Residual'][i]
    
    pr_R.append(temp_Rpr)
    pr_D.append(temp_Dpr)

# Landfill.
Lf_PA=CFlux_data['Paper_L']                 # Paper
Lf_BC=CFlux_data['BC_L']                    # Building Construction
Lf_EC=CFlux_data['EC_L']                    # Exterior Construction
Lf_HA=CFlux_data['HA_L']                    # Home Application
Lf_PR=pr_D                                  # Processing Residuals

def Main_Estimate2 ():
    
    # Charcoal.
    ch_results=cc.charcoal_CFlux(total_yr,Tchar,cha_dc1,cha_dc2)
    
    # Landfill.
    lf_results=lf.Landfill_CFlux(total_yr,Lf_PA,Lf_BC,Lf_EC,Lf_HA,Lf_PR,
                                 ldf_pap1,ldf_pap2,ldf_bcp1,ldf_bcp2,
                                 ldf_ecp1,ldf_ecp2,ldf_hap1,ldf_hap2,
                                 ldf_prp1,ldf_prp2)
        
    results=[]
    
    for i in range (total_yr):
        temp=[]
        
        # Year.
        temp.append(i)
        
        # Charcoal.
        temp.append(round(ch_results[0][i]))
        temp.append(round(ch_results[1][i]))
        
        # Landfill.
        temp.append(round(lf_results[0][i]))
        temp.append(round(lf_results[1][i]))
        temp.append(round(lf_results[2][i]))
                
        header3=['Year','Charcoal_A','Charcoal_D','Landfill_C',
                 'Landfill_A','Landfill_DC']
        
        results.append(temp)
    
    df=pd.DataFrame(data=results)
    df.to_csv(directory+chr(92)+'Results_Charcoal_Landfill.csv',index=False,header=header3)    

Main_Estimate2 ()