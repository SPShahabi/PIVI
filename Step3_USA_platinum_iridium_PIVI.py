#                            DoD Minerva Project
#                           Shokoufeh Pourshahabi
#              Step III_Potential indirect vulnerability index (PIVI)
#                           USA_platinum_iridium_trade
#                            

import pandas as pd
import numpy as np

n = int (input("Please enter the number of countries/territories: "))

Reporter = pd.read_csv('USA_as_Trade_Reporter.csv', low_memory=False)
Partner = pd.read_csv('USA_as_Trade_Partner.csv', low_memory=False)
FDI_couple_ratio = pd.read_excel('FDI_couple_strength.xlsx', sheet_name='FDI_couple_ratio')

def clean_data(df):
    df = df.copy()
    
    df = df.loc[(df['Trade Flow Code'] != 3) & (df['Trade Flow Code'] != 4)] # Remove Re-Export/Re-Import data
    df = df.loc[df['Trade Value (US$)'] >= 1] # Filter rows based on minimum trade value
    excluded_unclear = ['World', 'Other Asia, nes', 'Areas, nes'] # Remove rows with unclear partners/Reporters
    df = df.loc[~df['Partner'].isin(excluded_unclear)]
    df = df.loc[~df['Reporter'].isin(excluded_unclear)]
    df = df.loc[df['Commodity Code'] != 'TOTAL'] # Remove rows where 'Commodity Code' is 'TOTAL'
    df['Commodity Code'] = pd.to_numeric(df['Commodity Code'], errors='coerce')
    df = df.loc[(df['Commodity Code'] == 711011) | (df['Commodity Code'] == 711019)
                | (df['Commodity Code'] == 711041) | (df['Commodity Code'] == 711049)]

    return df


def swap_columns(df, col1, col2):
    df[[col1, col2]] = df[[col2, col1]].to_numpy()
    return df


# Clean and filter data
Reporter = clean_data(Reporter)
Partner = clean_data(Partner)

# Filter rows for USA import and export
USA_Import_from = Reporter[Reporter['Trade Flow Code'] == 1]
USA_Export_to = Reporter[Reporter['Trade Flow Code'] == 2]
Import_from_USA = Partner[Partner['Trade Flow Code'] == 1]
Export_to_USA = Partner[Partner['Trade Flow Code'] == 2]

Import_from_USA = swap_columns(Import_from_USA, 'Reporter Code', 'Partner Code')
Import_from_USA = swap_columns(Import_from_USA, 'Reporter', 'Partner')
Export_to_USA = swap_columns(Export_to_USA, 'Reporter Code', 'Partner Code')
Export_to_USA = swap_columns(Export_to_USA, 'Reporter', 'Partner')

Total_Import = pd.concat([USA_Import_from, Export_to_USA], ignore_index=True)
Total_Export = pd.concat([USA_Export_to, Import_from_USA], ignore_index=True)

# Drop rows where 'Reporter' is the same as 'Partner'
Total_Import = Total_Import[Total_Import['Reporter'] != Total_Import['Partner']]
Total_Export = Total_Export[Total_Export['Reporter'] != Total_Export['Partner']]

# Calculate the average of the parallel rows 
Total_Import = Total_Import.groupby(['Reporter Code', 'Partner Code', 'Commodity Code'], as_index=False).agg({
    'Reporter': 'first', 'Partner': 'first', 'Commodity': 'first', 'Trade Value (US$)': 'mean'})

Total_Export = Total_Export.groupby(['Reporter Code', 'Partner Code', 'Commodity Code'], as_index=False).agg({
    'Reporter': 'first', 'Partner': 'first', 'Commodity': 'first', 'Trade Value (US$)': 'mean'})

# Calculate Net-Import
Net_Import = pd.merge(Total_Import , Total_Export, on=['Reporter Code', 'Partner Code', 'Commodity Code'],
    suffixes=('_Import', '_Export'), how='outer')
Net_Import['Net Trade Value (US$)'] = Net_Import['Trade Value (US$)_Import'].fillna(0) - Net_Import['Trade Value (US$)_Export'].fillna(0)
Net_Import = Net_Import[Net_Import['Net Trade Value (US$)'] > 0]


# ******************************************************************************
# platinum
Net_Import.loc[Net_Import['Commodity Code'].isin([711011, 711019]), 'Commodity_Import'] = 'platinum'
Net_Import_platinum = Net_Import.loc[(Net_Import['Commodity_Import'] == 'platinum')]

Net_Import_platinum = Net_Import_platinum.groupby(['Reporter Code', 'Partner Code', 'Commodity_Import'], as_index=False).agg({
    'Reporter_Import': 'first', 'Partner_Import': 'first', 'Net Trade Value (US$)': 'sum'})

Total_Import_platinum = Total_Import[Total_Import['Commodity Code'].isin([711011, 711019])]
Total_Import_platinum = Total_Import_platinum ['Trade Value (US$)'].sum()
Total_Export_platinum = Total_Export[Total_Export['Commodity Code'].isin([711011, 711019])]
Total_Export_platinum = Total_Export_platinum ['Trade Value (US$)'].sum()

Net_Import_platinum['Trade Ratio'] = Net_Import_platinum['Net Trade Value (US$)'] / (
    Total_Import_platinum + Total_Export_platinum)

platinum_PIVI = []

# Get unique countries from the 'Partner Country' column in FDI_couple_ratio (these are potential "Investing Countries")
unique_countries = FDI_couple_ratio['Partner Country'].unique()
unique_countries = unique_countries[unique_countries != 'United States']

# Loop through each investing country
for investing_country in unique_countries:
    df_intermediary = Net_Import_platinum[Net_Import_platinum['Partner_Import'] != investing_country]
    
    sum_of_value = 0  # Initialize the sum of PIVI for the current investing country
    
    for _, row in df_intermediary.iterrows():
        # Find the FDI ratio corresponding to the investing country and the current intermediary country
        intermediary_country = row['Partner_Import']
        
        # Get the matching FDI Ratio from FDI_couple_ratio for the current intermediary country and investing country
        fdi_match = FDI_couple_ratio[(FDI_couple_ratio['Reporting Country'] == intermediary_country) & 
            (FDI_couple_ratio['Partner Country'] == investing_country)]
        
        # If a match is found, calculate the PIVI for this intermediary country and add to the sum   
        if not fdi_match.empty:
            fdi_ratio = fdi_match['FDI Ratio'].values[0]           
                
            # Ensure the value inside np.log10 is positive
            value = n**2 * row['Trade Ratio'] * fdi_ratio
            sum_of_value += value
                        
            if sum_of_value > 0:
                PIVI = np.log10(sum_of_value)
           
    if PIVI==0:
        PIVI = np.nan                
        
    platinum_PIVI.append([investing_country, PIVI])


platinum_PIVI_df = pd.DataFrame(platinum_PIVI, columns=['Investing Country', 'PIVI'])
        
# Find the critical investing country with the highest sum_of_PIVI
critical_investing_country_platinum = platinum_PIVI_df.loc[platinum_PIVI_df['PIVI'].idxmax(), 'Investing Country']
df_intermediary = Net_Import_platinum[Net_Import_platinum['Partner_Import'] != critical_investing_country_platinum]
rank = pd.DataFrame(columns=['critical_investing_country_platinum','Intermediary', 'value'])

# ******************************************************************************
# iridium
Net_Import.loc[Net_Import['Commodity Code'].isin([711041, 711049]), 'Commodity_Import'] = 'iridium'
Net_Import_iridium = Net_Import.loc[(Net_Import['Commodity_Import'] == 'iridium')]

Net_Import_iridium = Net_Import_iridium.groupby(['Reporter Code', 'Partner Code', 'Commodity_Import'], as_index=False).agg({
    'Reporter_Import': 'first', 'Partner_Import': 'first', 'Net Trade Value (US$)': 'sum'})

Total_Import_iridium = Total_Import[Total_Import['Commodity Code'].isin([711041, 711049])]
Total_Import_iridium = Total_Import_iridium ['Trade Value (US$)'].sum()
Total_Export_iridium = Total_Export[Total_Export['Commodity Code'].isin([711041, 711049])]
Total_Export_iridium = Total_Export_iridium ['Trade Value (US$)'].sum()

Net_Import_iridium['Trade Ratio'] = Net_Import_iridium['Net Trade Value (US$)'] / (
    Total_Import_iridium + Total_Export_iridium)

iridium_PIVI = []

# Get unique countries from the 'Partner Country' column in FDI_couple_ratio (these are potential "Investing Countries")
unique_countries = FDI_couple_ratio['Partner Country'].unique()
unique_countries = unique_countries[unique_countries != 'United States']

# Loop through each investing country
for investing_country in unique_countries:
    df_intermediary = Net_Import_iridium[Net_Import_iridium['Partner_Import'] != investing_country]
    
    sum_of_value = 0  # Initialize the sum of PIVI for the current investing country
    
    for _, row in df_intermediary.iterrows():
        # Find the FDI ratio corresponding to the investing country and the current intermediary country
        intermediary_country = row['Partner_Import']
        
        # Get the matching FDI Ratio from FDI_couple_ratio for the current intermediary country and investing country
        fdi_match = FDI_couple_ratio[(FDI_couple_ratio['Reporting Country'] == intermediary_country) & 
            (FDI_couple_ratio['Partner Country'] == investing_country)]
        
        # If a match is found, calculate the PIVI for this intermediary country and add to the sum   
        if not fdi_match.empty:
            fdi_ratio = fdi_match['FDI Ratio'].values[0]           
                
            # Ensure the value inside np.log10 is positive
            value = n**2 * row['Trade Ratio'] * fdi_ratio
            sum_of_value += value
                        
            if sum_of_value > 0:
                PIVI = np.log10(sum_of_value)
           
    if PIVI==0:
        PIVI = np.nan                
        
    iridium_PIVI.append([investing_country, PIVI])


iridium_PIVI_df = pd.DataFrame(iridium_PIVI, columns=['Investing Country', 'PIVI'])
        
# Find the critical investing country with the highest sum_of_PIVI
critical_investing_country_iridium = iridium_PIVI_df.loc[iridium_PIVI_df['PIVI'].idxmax(), 'Investing Country']
df_intermediary = Net_Import_iridium[Net_Import_iridium['Partner_Import'] != critical_investing_country_iridium]
rank = pd.DataFrame(columns=['critical_investing_country_iridium','Intermediary', 'value'])

# ******************************************************************************

with pd.ExcelWriter('US_platinum_iridium_PIVI.xlsx') as writer:
    Net_Import_platinum.to_excel(writer, sheet_name='Net_Im_platinum', index=False)
    platinum_PIVI_df.to_excel(writer, sheet_name='platinum_PIVI', index=False)
    Net_Import_iridium.to_excel(writer, sheet_name='Net_Im_iridium', index=False)
    iridium_PIVI_df.to_excel(writer, sheet_name='iridium_PIVI', index=False)
