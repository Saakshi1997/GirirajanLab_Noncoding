# Script to map Sample IDs and obtain family ids + relationship

import pandas as pd 

# Load SFARI csv ( contains family IDs and relationship)
map_df = pd.read_csv("nygc_sfari_id_map.csv", delimiter="," , header =0)
map_df[["Family Id","Relationship"]] = map_df["SFARI ID"].str.split(".", expand = True)

# Changing the column names for consistency.
columns_dict = {"SFARI ID":"SFARI_Id","Repository Id":"SAMPLE","Family Id":"Family_Id","Relationship":"Relationship"}
map_df.rename(columns_dict, axis = 1 , inplace = True)
map_df = map_df.loc[:,["SAMPLE","Family_Id","Relationship"]]
df_grouped = map_df.groupby("Family_Id").size().reset_index(name="count")

# Creating a dictionary from the mapping dataframe
map_dict=map_df.set_index('SAMPLE').T.to_dict('list')

# Load the variant calls (filtered TSV)
variant_df = pd.read_csv("18.7_with_freq.tsv",  delimiter="\t" , header =0)

# Splitting the Annotation string - creating a new column: Anno_Class
variant_df.loc[:,"Anno_Class"]=variant_df.loc[:,"ANN"].str.split("|").str[1]
sub_variant_df = variant_df.loc[:,["SAMPLE","Anno_Class"]]

sub_variant_df["Family_ID"]=sub_variant_df["SAMPLE"].astype(str).map(map_dict)
sub_variant_df[["Family_ID","Relationship"]]= pd.DataFrame(sub_variant_df.Family_ID.tolist(), index= sub_variant_df.index)

# Annotations of interest
required_anno = ['upstream_gene_variant', '5_prime_UTR_variant']

# Proband and sibling pairs.
pro_sib = ["p1","s1"]

final_df = sub_variant_df.loc[(sub_variant_df["Anno_Class"].isin(required_anno)) & sub_variant_df["Relationship"].isin(pro_sib)]
final_df.reset_index(drop=True, inplace=True)
final_df.to_csv("18.8_final.tsv", sep="\t", header = True, index=None)
from IPython import embed; embed()

