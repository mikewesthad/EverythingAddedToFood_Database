Extract "Everything Added to Food in the United States" Database
======================================

extractEAFUS.py will pull the HTML file for the FDA's EAFUS database and parse it into a paired down HTML file and into a pipe delimited ("|") text representation.  Credit to the FDA for the database, obviously.

What is the EAFUS, you ask?

It's a list of 3000+ substances that are legally allowed to be added to foods in the United States.  These substances were either directly approved by the FDA or are affirmed by the FDA to be "generally	recognized as safe" (GRAS). 

The table from the EAFUS website contains only five fields from the complete FDA database (PAFA).  They are:
		doctype - Status of toxicology information available
		docnum - PAFA database number for printed information on substance
		mainterm - name of substance
		cas rn or other code - registry number for the substance
		regnum - FDA regulation numbers where the substance appears 
		
[More information of EAFUS](http://www.fda.gov/Food/IngredientsPackagingLabeling/ucm115326.htm)
[More information on GRAS](http://www.fda.gov/food/ingredientspackaginglabeling/gras/default.htm)

Software dependencies: 

- bs4 (install with pip using: "pip install bs4")
