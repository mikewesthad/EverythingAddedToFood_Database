import os, random
from bs4 import BeautifulSoup

pathToEafus = os.path.join("..", "eafus_20_06_2014.txt")
additives = []
with open(pathToEafus, "r") as eafusFile:
	eafusFile.next() # Skip the column labels
	for line in eafusFile:
		elements = line.split("|")
		additiveName = elements[2]
		additives.append(additiveName)


html_doc = """
<html>
<head>
</head>
<body>
<p><b>INGREDIENTS:</b></p>
</body>
</html>
"""

soup = BeautifulSoup(html_doc)

additivesString = ""
for i in range(100):
	additiveIndex = random.randint(0, len(additives)-1)
	additive = additives[additiveIndex]
	additivesString += additive.upper() + ", "
additivesString = additivesString[:-2]
soup.p.append(additivesString)

with open("index.html", "w") as htmlFile:
	htmlFile.write(soup.encode())


import subprocess
subprocess.call(["pandoc", "--latex-engine=xelatex", "--template=temp.tex", "-o", "index.pdf", "index.html"])
