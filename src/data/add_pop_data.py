# The admin data has states labeled by abbreviation, the census population data has states by their full names
# Need to use an abbreviation crosswalk to merge the two datasets

# import libraries
import os
import pandas as pd

# locations
DATA_DIR="/Users/nicolekelly/Documents/imls_library_data_project/imls_library_data_project/data/raw"
OUTPUT_DIR="/Users/nicolekelly/Documents/imls_library_data_project/imls_library_data_project/data/interim"

# read in the admin data (might want to generalize this for later)
admin=pd.read_csv("/Users/nicolekelly/Documents/imls_library_data_project/imls_library_data_project/data/raw/admin_entities_data_2015.csv",sep='|')

# read in the population data
population=pd.read_csv(os.path.join(DATA_DIR,"PEP_2017_PEPANNRES_with_ann.csv"))

# clean and reformat the population data
# use the population estimate as of July 2015 as the closest approximation to the admin data time period
# this might be reconsidered when documentation is examined more closely
population.drop(['GEO.id', 'GEO.id2',  'rescen42010', 'resbase42010',
       'respop72010', 'respop72011', 'respop72012', 'respop72013',
       'respop72014', 'respop72016', 'respop72017'], axis=1, inplace=True)
population.rename(columns={'GEO.display-label': 'state_full', 'respop72015': 'population_201507'}, inplace=True)

# read in the state name to abbrevation crosswalk
state_crosswalk=pd.read_csv(os.path.join(DATA_DIR,"bls_usps_state_abbrev.csv"))

# merge the crosswalk to the population data
population_w_abbrev=population.merge(state_crosswalk,how='left',left_on='state_full', right_on='state_full')

# there are some regional records to remove (these did not match and therefore have NaN for state_abbrev
population_w_abbrev=population_w_abbrev[population_w_abbrev['state_abbrev'].notnull()]

# remove the full name of the state field to prepare for joining
population_w_abbrev.drop('state_full',axis=1,inplace=True)
population_w_abbrev.rename(columns={'state_abbrev':'state'}, inplace=True)

print(len(population_w_abbrev)) # this should be 52 with Puerto Rico and DC; Guam is in admin dataset, might have to add pop manually

# merge the populations into the admin data
admin_w_population=admin.merge(population_w_abbrev,how='left',left_on='state',right_on='state')

# save this dataset as a csv in the interim data folder
admin_w_population.to_csv(os.path.join(OUTPUT_DIR,"admin_entities_data_2015_pop.csv"), sep='|')