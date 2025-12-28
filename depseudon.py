import os
import sys
import pandas as pd
import funcs

#
# Reverse pseudonmyzing after having run analyses.
#

def depseudon(filenames, map_fn):
    MapDF = pd.read_csv(map_fn, sep = "\t", header=None)
    Map = {}
    for m in MapDF.iterrows():
        Map[m[1][0]] = m[1][1]
    for analysis_fn_full in filenames:
        analysis_txt = funcs.read_file(analysis_fn_full)
        if analysis_txt is None:
            print("Cannot read " + analysis_fn_full)
            continue
        for pseudonym in Map.keys():
            analysis_txt = analysis_txt.replace(pseudonym, Map[pseudonym])
        base_name, ext = os.path.splitext(analysis_fn_full)
        depseu_fn = base_name + "_depseudonymized" + ext
        funcs.write_file(depseu_fn, analysis_txt)

if __name__ == '__main__':
    analysis_fn = sys.argv[1]
    map_fn = sys.argv[2]
    depseudon((analysis_fn), map_fn)
