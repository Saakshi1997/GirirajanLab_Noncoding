# Script to map Sample IDs and obtain family ids + relationship

import pandas as pd
import sys

# infile = $./${a}.7_with_freq.tsv
# mapfile = $./nygc_sfari_id_map.csv
# outfile = $./${a}.8_mapped.tsv

infile = sys.argv[1]
mapfile = sys.argv[2]
outfile=sys.argv[3] 

# Load SFARI csv ( contains family IDs and relationship)
map_df = pd.read_csv(mapfile, delimiter="," , header =0)
map_df[["Family Id","Relationship"]] = map_df["SFARI ID"].str.split(".", expand = True)

# Changing the column names for consistency.
columns_dict = {"SFARI ID":"SFARI_Id","Repository Id":"SAMPLE","Family Id":"Family_Id","Relationship":"Relationship"}
map_df.rename(columns_dict, axis = 1 , inplace = True)
map_df = map_df.loc[:,["SAMPLE","Family_Id","Relationship"]]

# Creating a dictionary from the mapping dataframe
map_dict=map_df.set_index('SAMPLE').T.to_dict('list')

# Load the variant calls (filtered TSV)
variant_df = pd.read_csv(infile,  delimiter="\t" , header =0)

# Splitting the Annotation string - creating a new column: Anno_Class
variant_df.loc[:,"Anno_Class"]=variant_df.loc[:,"ANN"].str.split("|").str[1]
sub_variant_df = variant_df.loc[:,["SAMPLE","Anno_Class"]]

sub_variant_df["Family_ID"]=sub_variant_df["SAMPLE"].astype(str).map(map_dict)
sub_variant_df[["Family_ID","Relationship"]]= pd.DataFrame(sub_variant_df.Family_ID.tolist(), index= sub_variant_df.index)

# Annotations of interest
required_anno = ['upstream_gene_variant', '5_prime_UTR_variant', '5_prime_UTR_premature_start_codon_gain_variant','3_prime_UTR_variant']

final_df = sub_variant_df.loc[(sub_variant_df["Anno_Class"].isin(required_anno))]
final_df.reset_index(drop=True, inplace=True)
final_df.to_csv(outfile, sep="\t", header = True, index=None)
#from IPython import embed;embed()


