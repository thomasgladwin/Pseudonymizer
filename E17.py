# Prep
import pandas as pd

try:
    import nltk
    nltk.download('maxent_ne_chunker_tab')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('words')
except:
    pass # Allow for if downloaded before but currently offline

import os
from nltk.tag import pos_tag
import nltk
import sys
import funcs

def E17(files, file_replace="", output_dir_name="Pseudon"):
    #
    # Identify proper nouns
    #

    if len(file_replace) > 0:
        Replace_DF = pd.read_excel(file_replace, header=None)
    else:
        Replace_DF = None

    dir_name = os.path.dirname(files[0])

    txts = []
    pts = []
    ext_mem = []
    for fn in files:
        print("Reading " + fn)
        txt = funcs.read_file(fn)
        if txt is None:
            print("Cannot read " + fn)
            continue
        if Replace_DF is not None:
            for row0 in Replace_DF.iterrows():
                txt = txt.replace(row0[1][0], row0[1][1])
        basename, ext = os.path.splitext(fn)
        ext_mem.append(ext)
        txts.append(txt)
        tokens = nltk.word_tokenize(txt)
        pos_tags = pos_tag(tokens)
        named_entities = nltk.ne_chunk(pos_tags, binary=True)
        pts.append(named_entities)
    def is_name(el):
        if isinstance(el, nltk.tree.tree.Tree):
            return True
        elif el[1] == "NNP":
            return True
        else:
            return False
    def get_token(el):
        if isinstance(el, nltk.tree.Tree):
            return el[0][0]
        else:
            return el[0]
    proper_nouns = set([get_token(el) for pt in pts for el in pt if is_name(el)])

    #
    # Generate output
    #

    out_dir = dir_name + "/" + output_dir_name
    try:
        os.mkdir(out_dir)
    except:
        pass

    pseudon_dict = {}
    n = 1
    with open(out_dir + "/Pseudon_map.txt", 'w', encoding="utf-8") as f:
        for name0 in proper_nouns:
            pseudon_dict[name0] = "#PSEUDONYM" + str(n) + "#"
            n += 1
            str0 = pseudon_dict[name0] + "\t" + name0
            print(str(n) + " " + str0)
            f.write(str0 + "\n")

    txt_for_prompt = ''
    iFile = 1
    for pt in pts:
        pt_new = []
        for tag in pt:
            if isinstance(tag, nltk.tree.tree.Tree):
                tag = tag[0]
            if tag[0] in proper_nouns and tag[1] == 'NNP':
                print("Replacing: " + tag[0])
                tag = (pseudon_dict[tag[0]], tag[1])
            if ext_mem[iFile-1] == ".xlsx":
                if tag[0] in ["``", "''"]:
                    tag = ("\"", tag[1])
            pt_new.append(tag)
        tokens_new = [tag[0] for tag in pt_new]
        txt_new = ' '.join(tokens_new)
        remove_space_for = ["\'", ",", ".", ":", "\""]
        for r in remove_space_for:
            txt_new = txt_new.replace(" " + r, r)
        print(txt_new)
        fn = out_dir + "/Pseudon" + str(iFile) + ext_mem[iFile - 1]
        funcs.write_file(fn, txt_new)
        txt_for_prompt = txt_for_prompt + "\n#####Document " + str(iFile) + "\n" + txt_new
        iFile = iFile + 1

    out_fn = out_dir + "/PseudonymizedPrompt.txt"
    prompt_define = "Define interviews as the sections of the text below, starting with strings like #####Document 1, #####Document 2, and so on. The label of each interview is this string starting with #####Document. "
    prompt_define = prompt_define + "Define the respondent of a given interview as the person answering questions in that interview."
    prompt_define = prompt_define + "Define codes as abstractions of similar responses given by respondents to similar questions. A codesis a type of idea or attitude that is repeated over respondents. A code representing an attitude should be either positive or negative, not both."
    prompt_define = prompt_define + "Define the importance of codes as a combination of how often they occur and how impactful they are to respondents or the issues they are talking about."
    prompt_define = prompt_define + "Define features of respondents as the ways in which respondents differ from each other, which most efficiently describe the group of respondents. Consider gender, age, job role, or job seniority, for example, but override these examples for more relevant features found in the data."
    prompt_analysis = "Over all interviews, identify a set of codes that represents the most important responses efficiently. Print out the labels of the codes, with for each code two or three examples of quoted responses associated with that code. Other the list of codes by importance."
    prompt_analysis = prompt_analysis + "Generate a table showing which interviews contained responses expressing each code; each column in the table represents a code and each row represents an interview. Place a 0 in a cell of the table if the interview did not express the code and a 1 otherwise."
    prompt_analysis = prompt_analysis + "Identify and report any respondent features that are associated with differences between the likelihood of codes beng expressed."
    prompt_analysis = prompt_analysis + "Ensure your analyses use all the Documents provided, from first to last. Identity the highest number in the document labels: this is the number of documents. Ensure you generate all requested outputs. Do not use any tool calls: perform the analysis yourself. Do a thorough, academic-style analysis."
    txt_for_prompt = prompt_define + txt_for_prompt + prompt_analysis
    funcs.write_file(out_fn, txt_for_prompt)

    return out_dir

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dir_name = sys.argv[1]
    filenames = os.listdir(dir_name)
    out_dir = E17(filenames)
    print("For a start with interview analysis: Upload the generated prompt to Copilot and ask it to: Run the analysis defined in the uploaded file PseudonymizedPrompt.txt.")
    print("Exported files are in " + out_dir + ".")
