#!/usr/bin/env python3.7

import re
from pathlib import Path
import subprocess
from subprocess import PIPE, run

#excerptTitle = 'Robert F. Williams, Negroes With Guns :\n'
#excerptTitle = 'How to Be an Adult in Relationships:\n'
excerptTitle = 'The Subtle Art of Not Giving a F*ck:\n'

minumumNumberOfWordsForExcerpt = 10
maxNumberOfWordsForExcerpt = 70
	
numIterations=0

def paginate (theString, myRange, sumOfPages):

	global numIterations
	
	numIterations+=1
	
	counter = 0
	turnToImageString=""
	finalString=excerptTitle
	
	# Keep track of page number
	pgNumber=""
	
	# This tracks if there is more than one page to create for each excerpt and add ... 
	# at the start of the next portion of the excerpt
	numIterationsForDOTS=0
	
	# This find all the words minus punctuation
	#listOfWords = re.findall('\w+', theString)
	
	# Below regex preserves the formatting such a space between words
	listOfWords = re.findall(r'.*?\s+', theString) 
	
	# This splits and preserves the punctuation
	#listOfWords = theString.split()
	for i in listOfWords:
		#print ( i, end="" )
		turnToImageString +=i 
		counter+=1
		if (counter == myRange):
			
			if (numIterationsForDOTS >0):
				finalString+="..."+turnToImageString+"..."
			else:			
				finalString+=turnToImageString+"..."
			
			theFileName = str (numIterations)+".png"
			pgNumber = str ( numIterations )+"/"+str( sumOfPages )
			
			# Print the excerpt to an image
			subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity northeast -pointsize 60 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +30+0 "%s" %s' % (finalString, pgNumber, theFileName), shell=True )
				
			print ( finalString )
			
			# reset counter
			counter = 0
			turnToImageString = ""
			# This variable decide if the next excerpt should have a ... at the begining
			numIterationsForDOTS+=1
			
			numIterations+=1
			
			finalString=excerptTitle

	if (numIterationsForDOTS >0):
		finalString+="..."+turnToImageString
	else:
		finalString+=turnToImageString
	

	theFileName = str (numIterations)+".png"
	
	# This check is the there is only one except and the minumum number of word is in excess of X
	# If it is less then it will omit
	"""
	lengthOfFinalString = re.findall(r'.*?\s+', finalString)
	excerptLength = re.findall(r'.*?\s+', excerptTitle)

	if ( len ( lengthOfFinalString[ len (excerptLength ): ]  )  <  minWordsForExcerpt and numIterationsForDOTS == 0 ):
		print ( "OMITTING OMITTING > %s" % (  finalString ) )	
		#print ( finalString )
	else:		
		print ( finalString )
		"""
	pgNumber = str ( numIterations )+"/"+str( sumOfPages )
	#rint ( pgNumber )
	
	print ( finalString )
	
	subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity northeast -pointsize 60 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +30+0 "%s" %s' % (finalString, pgNumber, theFileName), shell=True )
	

# Count number of pages

def countNumPages ( theString, myRange ):
	numIterationsForPageCount=0
	counter = 0
	
	# Below regex preserves the formatting such a space between words
	listOfWords = re.findall(r'.*?\s+', theString) 
	
	for i in listOfWords:
		counter+=1
		if (counter == myRange):
			numIterationsForPageCount+=1
			# reset counter
			counter = 0
	
	if (counter != 0):
		numIterationsForPageCount+=1
	
	return numIterationsForPageCount
	
	
	
	
# Open file for regex

externalFile = Path("My Clippings.txt").read_text()
#externalFile = Path("NWGshare.txt").read_text()
#externalFile = Path("exTxt.txt").read_text()
	
#pattern = re.findall(r'^Negroes With Guns[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^How to Be an Adult[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
pattern = re.findall(r'^The Subtle Art of Not[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )

sumOfPage=0
# This variable is to show how many excerpts from the original
# document will be used NOT HOW MANY TOTAL FOUND IN THE ORIGINAL DOCUMENT
sumUsedExcerpt=0
for excerpt in pattern:

	# This sets a minimum length of an excert to pass
	if ( len ( re.findall(r'.*?\s+', excerpt ) ) > minumumNumberOfWordsForExcerpt ):
		countNumPages (excerpt, maxNumberOfWordsForExcerpt) 
		sumOfPage+=countNumPages (excerpt, maxNumberOfWordsForExcerpt)
		sumUsedExcerpt+=1

print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % (excerptTitle[0:-2], sumOfPage,  sumUsedExcerpt ),  end="\n\n")
	


for excerpt in pattern:
	
	# This sets a minimum length of an excert to pass
	if ( len ( re.findall(r'.*?\s+', excerpt ) ) > minumumNumberOfWordsForExcerpt ):
		paginate (excerpt, maxNumberOfWordsForExcerpt, sumOfPage )
	else :
		print ( "OMITTING OMITTING : %s" % ( excerpt ) )
	

	
	
	

