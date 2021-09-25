import json

from unidecode import unidecode

if __name__ == '__main__':
    files = ["cong-nghe.txt","doi-song.txt","giai-tri.txt","the-gioi.txt","thoi-su.txt"]
    for file in files:
        with open("train/"+file, "r") as r:
            with open("test.csv", "a",encoding="utf-8") as w:
                w.write('content,label,\n')
                for s in r.readlines():
                    w.write('{},{},\n'.format(s[:-1],file[:-4],))
