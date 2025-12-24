import os
import sys
import pandas as pd


#
# Reverse pseudonmyzing after having run analyses.
#

def depseudon(filenames, map_fn):
    MapDF = pd.read_csv(map_fn, sep = "\t", header=None)
    Map = {}
    for m in MapDF.iterrows():
        Map[m[1][0]] = m[1][1]
    for analysis_fn_full in filenames:
        with open(analysis_fn_full, 'r', encoding="utf-8") as f:
            analysis_txt = f.read()
        for pseudonym in Map.keys():
            analysis_txt = analysis_txt.replace(pseudonym, Map[pseudonym])
        base_name, ext = os.path.splitext(analysis_fn_full)
        depseu_fn = base_name + "_depseudonymized.txt"
        with open(depseu_fn, 'w', encoding="utf-8") as f:
            f.write(analysis_txt)

if __name__ == '__main__':
    analysis_fn = sys.argv[1]
    map_fn = sys.argv[2]
    depseudon((analysis_fn), map_fn)
