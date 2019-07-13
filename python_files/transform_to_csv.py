import json 
import pandas as pd
import numpy as np
from datetime import datetime
import os


def date(__format):
    d = datetime.utcnow()
    return d.strftime(__format)

import_filename = os.path.dirname(__file__) + '/Logs_JSON_EDDN_' + str(date('%Y-%m-%d')) + '.log'
export_filename = os.path.dirname(__file__) + '/cass_csv_data.csv'
df_final = pd.DataFrame(columns=['schemaRef','header','message'])
#open the file
file = open(import_filename, 'r') 
index = 0
for line in file: 
    line_data = json.loads(line)
    df_tmp = pd.DataFrame([[line_data['$schemaRef'], line_data['header'], line_data['message']]], index=[str(index) + '_' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')],columns=['schemaRef','header','message'])
    df_final = df_final.append(df_tmp)
    index += 1
#print(df_final.head(5))
df_final.to_csv(export_filename, encoding='utf-8', index=True, index_label='id' )