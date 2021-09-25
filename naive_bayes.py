import os
import re
import json
import math

special_charaters_1 = """[\+\-\,\.\'\“\”\"\(\)\?\:\!\@\#\$\%\^\&\*\[\]\}\{\>\<\…]"""
special_charaters_2 = '''\.+'''
concat_words = ["và", "cũng", "hơn", "nữa", "đó", "theo", "là", "với", "ở", "như", "nên", "do", "thế", 
    "vậy", "những", "tuy", "vì", "vẫn", "thì", "trong", "sau", "của", "rồi", "chi", "lắm", "gì"
]


def process():
    data = {}
    for file in os.listdir('train'):
        label = file.split(".")[0]
        with open('train/'+file, "r") as o:
            for line in o.readlines():
                for word in line.split():
                    data.setdefault(word,{})
                    data[word][label] = data[word].get(label,0) + 1

    with open("data.json", "w", encoding="utf-8") as w:
        json.dump(data, w, ensure_ascii=False)

    with open("data.json", "r") as r:
        print(json.load(r))

def standardize():
    for file in os.listdir('input'):
        with open('input/'+file, "r") as o1:
            lines = o1.readlines()
            for line in lines:
                temp = re.sub(string=line,pattern=special_charaters_1,repl=" ").lower()
                temp = [i if i not in concat_words else " " for i in temp.split()]
                with open('train/'+file, "a") as w:
                    w.write(" ".join(temp)+"\n")

labels = [str(i).split(".")[0] for i in os.listdir('train')]
lines = []
for file in os.listdir('train'):
    with open("train/"+file,"r") as o:
        lines.append(len(o.readlines()))

with open("data.json", "r") as r:
    data = json.load(r)

def getLabel(s):
    s = re.sub(string=s,pattern=special_charaters_1,repl=" ").lower().split()
    words = [len(data) for _ in range(len(labels))]
    for word, val_word in data.items():
        for label, val in val_word.items():
            words[labels.index(label)] += val

    probability = [0.0 for _ in range(len(labels))]
    for i in s:
        for j in range(len(labels)):
            if i in data:
                probability[j] += math.log(data[i].get(labels[j], 0)+1) - math.log(words[j])
            else:
                probability[j] -= math.log(words[j])

    return labels[probability.index(max(probability))]


if __name__ == "__main__":
    # standardize()
    # process()
    # right = 0
    # total = 0
    # with open("thoi-su-2.txt", "r") as o:
    #     for line in o.readlines():
    #         total += 1
    #         if getLabel(line) == "thoi-su":
    #             right += 1
    # print(right/total)
    while(True):
        print(getLabel(input()))

# 0.7357, 0.9786, 0.9482, 1