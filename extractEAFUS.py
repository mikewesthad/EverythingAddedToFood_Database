"""
This script will pull the HTML file for the FDA's EAFUS database and parse it
into a paired down HTML file and into a pipe delimited ("|") text 
representation.  Credit to the FDA for the database, obviously.

What is the EAFUS, you ask?
	It's a list of 3000+ substances that are legally allowed to be added 
	to foods in the United States.  These substances were either directly
	approved by the FDA or are affirmed by the FDA to be "generally
	recognized as safe" (GRAS).
	The table from the EAFUS website contains only five fields from the 
	complete FDA database (PAFA).  They are:
		doctype - Status of toxicology information available
		docnum - PAFA database number for printed information on substance
		mainterm - name of substance
		cas rn or other code - registry number for the substance
		regnum - FDA regulation numbers where the substance appears 
	More information of EAFUS: http://www.fda.gov/Food/IngredientsPackagingLabeling/ucm115326.htm
	More information on GRAS: http://www.fda.gov/food/ingredientspackaginglabeling/gras/default.htm

The parsing of the EAFUS database is based on the current format (HTML and CSS)
of the EAFUS website.  As such, if the styling or content of the site changes,
this code could be rendered obsolete.

___
Copyright (c) 2014 Michael Hadley, mikewesthad.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import bs4
from bs4 import BeautifulSoup
import urllib2, os, time

# Before doing anything, let's timestamp our output files with the current date
# since the FDA updates their site
outputFileName = "eafus_" + time.strftime("%d_%m_%Y") 

# Let's grab the html page that contains the eafus data
eafusUrl = "http://www.accessdata.fda.gov/scripts/fcn/fcnNavigation.cfm?rpt=eafusListing&displayAll=true"
response = urllib2.urlopen(eafusUrl)
html = response.read()

# Let's parse out the table that contains the data
# 	This just dumbly looks for the table that has the CSS class
#	setsort.  Works until they change the style of their page.
soup = BeautifulSoup(html)
eafusTable = soup.find("table", class_="setsort")
with open(outputFileName+".html", "w") as f:
	f.write(eafusTable.encode("utf-8"))


# Create a pipe delimited representation of the eafus html table 
# First row is labels, subsequent rows are data
# 	NOTE: CSV is not an option because some elements of the table contain commas
with open(outputFileName+".txt", "w") as eafusTextFile:

	fileString = ""

	# Pull off the table headers (i.e. column labels) and add to the text file
	tableHeader = eafusTable.thead
	headers = tableHeader.find_all("th")
	rowString = ""
	for header in headers:
		rowString += header.string.strip() + "|"
	rowString = rowString[:-1]
	fileString += rowString + "\n"

	# Pull off each row of the table and add it to the text file
	tableBody = eafusTable.tbody
	rows = tableBody.find_all("tr")
	for row in rows:

		rowString = ""

		# Each row contains multiple elements stored in the html element td (table data)
 		data = row.find_all("td") 

 		for datum in data:

 			# Some elements contain multiple tags within them, so we must iterate through
 			#	Types of elements: hyperlinks, texts, multiple chunks of text separated by line breaks
			for child in datum.children:

				# Plain text elements
				if type(child) == bs4.NavigableString:
					rowString += child.string.strip()

				# Hyperlinks or multiple chunks of text separated with line breaks
				else:
					# Treat line breaks as commas
					if child.name == "br": 
						rowString += ","
					else:
						rowString += child.get_text().strip() 

			rowString += "|"
		rowString = rowString[:-1]
		fileString += rowString + "\n"
	fileString = fileString[:-1]

	eafusTextFile.write(fileString)
