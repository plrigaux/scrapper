#import pandas module
import pandas as pd
import glob

#read the csv file into a dataframe
#df = pd.read_csv("/home/pier/Documents/Cie_taxes/releve.csv", encoding='latin-1', header=0)



# 1. List files to read
source_files = glob.glob('/home/pier/Documents/Cie_taxes/r*.csv')

""" # 2. Convert list of files into list of dataframes
dataframes = []
for filename in source_files:
    df = pd.read_csv(filename, encoding='latin-1') 
   # df.rename(columns={'log2foldchange' : filename}, inplace=True)
    dataframes.append(df)

# 3. Concatenate it
df = pd.concat(dataframes)



df.to_csv("out.csv", sep='\t')
 """

with open('out.csv', 'w') as outfile:
    for filename in source_files:
        with open(filename, encoding='latin-1') as infile:
            for line in infile:
                outfile.write(line)
