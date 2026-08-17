import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import sys
import warnings
warnings.filterwarnings("ignore")

file_path  = str(sys.argv[1] )       #r"D:\Tutorial\Examples\Example.fasta"
print(file_path)

if  file_path.lower().endswith(".fasta"):
    dir_path = file_path.replace(".fasta","")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    data_dict = {}
    with open(file_path) as file:
        for line in file.readlines():
            if line.startswith(">"):
                key = line.replace(">","").strip()
                data_dict[key] = ""
            else:
                data_dict[key]+=line.upper().strip()
    header =[]
    count_A = []
    count_T = []
    count_G = []
    count_C = []
    seqLenth = []
    for key,seq in data_dict.items():
        count_A.append(seq.count("A"))
        count_T.append(seq.count("T"))
        count_G.append(seq.count("G"))
        count_C.append(seq.count("C"))
        seqLenth.append(len(seq))
        header.append(key)

    df = pd.DataFrame({"Header":header,"CountA":count_A,"CountT":count_T,"CountG":count_G,"CountC":count_C,"SeqLenth":seqLenth})
    df["GC_Perc"] =((df["CountG"] + df["CountC"])/df["SeqLenth"])*100

    # download data in Excel
    df.to_excel(os.path.join(dir_path,"data.xlsx"),index=False)  

    plt.figure(figsize=(12,8))
    plt.title("Count Of T")
    sns.barplot(df,x="Header",y ="CountT",palette="viridis")
    plt.savefig(os.path.join(dir_path,"Count_of_T.png"))
else:
    print(f"Please Provide fasta file as input : You Provided ---> {file_path}")
