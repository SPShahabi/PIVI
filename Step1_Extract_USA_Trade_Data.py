#                            DoD Minerva Project
#                           Shokoufeh Pourshahabi
#              Step I_Extract USA Trade Data from large csv files
#                            

import pandas as pd

file_path = input("Please enter the name of the CSV file: ")

chunk_size = 10000
extracted_rows_Reporter = []
extracted_rows_Partner = []

for chunk in pd.read_csv(file_path, chunksize=chunk_size):    
    filtered_rows_Reporter = chunk[chunk['Reporter Code'] == 842]
    extracted_rows_Reporter.append(filtered_rows_Reporter)
    
    filtered_rows_Partner = chunk[(chunk['Partner Code'] == 842)]
    extracted_rows_Partner.append(filtered_rows_Partner)    

extracted_data_Reporter = pd.concat(extracted_rows_Reporter)
extracted_data_Partner = pd.concat(extracted_rows_Partner)

extracted_data_Reporter = extracted_data_Reporter.drop(columns=['Classification', 'Period', 'Period Desc.', 'Aggregate Level' , 'Is Leaf Code' , 'Reporter ISO', 'Partner ISO', 'Qty Unit Code', 'Qty Unit' , 'Qty' , 'Netweight (kg)' , 'Flag'])
extracted_data_Reporter.to_csv('USA_as_Trade_Reporter.csv', index=False)

extracted_data_Partner = extracted_data_Partner.drop(columns=['Classification', 'Period', 'Period Desc.', 'Aggregate Level' , 'Is Leaf Code' , 'Reporter ISO', 'Partner ISO', 'Qty Unit Code', 'Qty Unit' , 'Qty' , 'Netweight (kg)' , 'Flag'])
extracted_data_Partner.to_csv('USA_as_Trade_Partner.csv', index=False)
