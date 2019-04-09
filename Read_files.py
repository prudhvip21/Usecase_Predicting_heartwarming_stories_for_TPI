import os
import pandas as pd

basedir = "/Users/Sid/PycharmProjects/NLP_ThePositiveIndia/firstpost"
data = []

for name in os.listdir(basedir):
    if not name.startswith("."):
        dir = basedir + "/" + name + "/"
        for fname in os.listdir(dir):
            fname_main = dir + fname
            with open(fname_main) as f:
                tmp_line = f.readlines()
                for line in tmp_line:
                    main_line_tmp = line[::-1].replace("|","", (line.count("|") - 1))[::-1]
                    main_line = name + "|" + main_line_tmp
                    data.append(main_line.split("|"))

data_df = pd.DataFrame(data, columns=['category', 'heading', 'content'])








