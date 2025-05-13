#                            DoD Minerva Project
#                           Shokoufeh Pourshahabi
#                          Step II_FDI Calculation
#                        

import pandas as pd
import numpy as np

FDI =  pd.read_excel('FDI_Inflow_Outflow.xlsx')
FDI = FDI[FDI['Value'] > 0]   # Neglect negative and zero FDI values

def swap_columns(df, col1, col2):
    df_copy = df.copy()  
    df_copy.loc[:, [col1, col2]] = df_copy[[col2, col1]].values
    return df_copy

inflow = FDI[FDI['Direction'] == 'inflow']
outflow = FDI[FDI['Direction'] == 'outflow']

inflow_swap = swap_columns(inflow, 'Reporting Country', 'Partner Country')
outflow_swap = swap_columns(outflow, 'Reporting Country', 'Partner Country')

Total_Inflow = pd.concat([inflow, outflow_swap], ignore_index=True)
Total_Outflow= pd.concat([outflow, inflow_swap], ignore_index=True)

# Drop rows where 'Reporting Country' is the same as 'Partner Country'
Total_Inflow = Total_Inflow[Total_Inflow['Reporting Country'] != Total_Inflow['Partner Country']]
Total_Outflow = Total_Outflow[Total_Outflow['Reporting Country'] != Total_Outflow['Partner Country']]

# Calculate the average of the parallel rows 
Total_Inflow = Total_Inflow.groupby(['Reporting Country', 'Partner Country'], as_index=False)['Value'].mean()
Total_Outflow = Total_Outflow.groupby(['Reporting Country', 'Partner Country'], as_index=False)['Value'].mean()

FDI_couple = pd.concat([Total_Inflow, Total_Outflow], ignore_index=True)
FDI_couple = FDI_couple.sort_values(by='Reporting Country', ascending=True)
FDI_couple = FDI_couple.groupby(['Reporting Country', 'Partner Country'], as_index=False)['Value'].sum()

ReporterList = np.unique(FDI_couple['Reporting Country'])
FDI_couple_ratio = []
for reporter in ReporterList:
    FDI_from = FDI_couple.loc[FDI_couple['Reporting Country'] == reporter, 'Partner Country']
    FDI_value = FDI_couple.loc[FDI_couple['Reporting Country'] == reporter, 'Value']
    Total_FDI = FDI_value.sum()
    for j in range(len(FDI_from)):
        ratio = FDI_value.iloc[j] / Total_FDI if Total_FDI > 0 else 0
        FDI_couple_ratio.append([reporter, FDI_from.iloc[j], ratio])        
                
FDI_couple_ratio_df = pd.DataFrame(FDI_couple_ratio, columns=['Reporting Country', 'Partner Country', 'FDI Ratio'])


with pd.ExcelWriter('FDI_couple_strength.xlsx') as writer:
    Total_Inflow.to_excel(writer, sheet_name='Total_Inflow', index=False)
    Total_Outflow.to_excel(writer, sheet_name='Total_Outflow', index=False)  
    FDI_couple.to_excel(writer, sheet_name='FDI_couple', index=False)
    FDI_couple_ratio_df.to_excel(writer, sheet_name='FDI_couple_ratio', index=False)