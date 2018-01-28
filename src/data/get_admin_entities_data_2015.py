# -*- coding: utf-8 -*-
import os
import pandas as pd

# general location of the data on IMLS
SOURCE_DOMAIN="https://data.imls.gov/resource/"
# this dataset is: 'Library Systems: FY 2015 Public Libraries Survey (Administrative Entities Data)', 
# more info available in refs folder
DATASET_IDENTIFIER="b457-cwyz"
APP_TOKEN="PoKK1H1uMQJgMryEJ7vCUKaEl"

# output location
OUTPUT_DIR="/Users/nicolekelly/Documents/imls_library_data_project/imls_library_data_project/data/raw"

# there are <10,000 rows in the data
limit="10000"

# create URL
url=SOURCE_DOMAIN+DATASET_IDENTIFIER+".json"+"?"+"$order=:id"+"&"+"$limit="+limit+"&"+"$$app_token="+APP_TOKEN

# read in data from json into dataframe (might want to leave as source
admin_entities_data_2015=pd.read_json(url)

# save data as csv (this might not be the best way to do it, but it works)
admin_entities_data_2015.to_csv(os.path.join(OUTPUT_DIR,"admin_entities_data_2015.csv"),sep='|',index=False)
