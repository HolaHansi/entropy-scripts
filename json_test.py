import os
import json

os.chdir("ranking_files")

f = open("20090430194925.txt")
line = f.readline

jsonThing = json.dumps(line)
print(jsonThing)
