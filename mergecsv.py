
import os
import glob
import pandas as pd


def main():
    os.chdir("/home/plr/Downloads/rel")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f, encoding='ISO-8859-3', header=None, quotechar='"', sep=",") for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()
