import re
f = open("20091115002350.txt")

lines = f.readlines()
text = ""
for line in lines:
	desc = str((re.split(',', line))[-1])
	if (desc != ""):
		text += str(desc + "*")


text = text.replace("*NO_DESC_ON_PAGE", " ")
text = text.replace("*URL_NOT_IN_ARCHIVE", " ")
text = text.replace("*NO_SNAPSHOT_CLOSE_ENOUGH_IN_TIME", " ")
text = text.replace("\n", " ")

q = open("testForKate.txt", 'w')
q.write(text)
q.close()