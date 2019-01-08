#!/usr/bin/env python3.7

import re
from pathlib import Path
import subprocess
from subprocess import PIPE, run
import math

#excerptTitle = 'Robert F. Williams, Negroes With Guns :\n'
#excerptTitle = 'How to Be an Adult in Relationships:\n'
excerptTitle = 'The Subtle Art of Not Giving a F*ck:\n'
#excerptTitle = 'Negroes With Guns:\n'
#excerptTitle = 'Outrageous Openness:\n'
#authorsName = 'Tosha Silver'
authorsName = 'Mark Manson'
#authorsName = 'Robert F Williams'

externalFileToRegexOver = "My Clippings.txt"
#externalFileToRegexOver = "NWGshare2.txt"

minumumNumberOfWordsForExcerpt = 10
maxNumberOfWordsForExcerpt = 70
	
numIterations=0

# Open file for regex
externalFile = Path( externalFileToRegexOver ).read_text()
#pattern = re.findall(r'^Negroes With Guns[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
pattern = re.findall(r'^The Subtle Art of Not[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )


class MyExcerpt:
	# Initialize instance attributes
	def __init__(self, myCaption, maxWrdsOrStr, minWrdsOrStr):
		self.myCaption = myCaption
		self.maxWrdsOrStr = maxWrdsOrStr
		self.minWrdsOrStr = minWrdsOrStr
		
	
	def numberWords(self):
		# Below regex preserves the formatting such a space between words
		listOfWords = re.findall(r'.*?\s+', self.myCaption) 

		return len ( listOfWords )
	
	def numberOfCharacters(self):
		
		numChars= len ( re.findall(r'\S', self.myCaption) ) 
		return numChars
	
	def numExcerptsByWord (self):

		howManyPages=math.ceil( self.numberWords()/self.maxWrdsOrStr )
		return howManyPages
	
	def numOfUsableExceprts (self):

		if ( self.numberWords()>self.minWrdsOrStr ):
			return True
		else:
			return False
		
	def returnOmitted (self):
		if ( self.numberWords()<self.minWrdsOrStr ):
			#return ( "OMITTING OMITTING : %s" % ( self.myCaption ) )
			return self.myCaption
	
	
	def sumOfTiles (self):
		
		# Test if number of excerpt contains more than minmum number of words
		if (self.numOfUsableExceprts () ) :
			return self.numExcerptsByWord()
		
	def listOfExcerpt4Pagination(self):
		# Below regex preserves the formatting such as space between words
		listOfWords = re.findall(r'.*?\s+', self.myCaption)
		# This list contains all the excerpts text per tile
		listToReturn = []
	
		# This will return a list of strings for paginating as long as they meets the required
		# word length
		if ( self.numberWords()>self.minWrdsOrStr ):
			while ( len ( listOfWords ) ) :
				listToReturn.append( "".join ( listOfWords[ :self.maxWrdsOrStr ] ) )
				del listOfWords[ :self.maxWrdsOrStr ]
			return listToReturn
	
#print ( mainData.numberWords() )
#print ( mainData.numberOfCharacters() )
#print ( mainData.numberOfCharacters() )
#print ( mainData.numExcerptsByWord() )

# Totoal number of excerpt(s) I will print
sumOfExcerpts = 0
# Totoal number of excerpt(s) found in original document
sumPrintable = 0
# This list stores ommited excerpts
listOfOmitted=[]

# Page number
pnum=0

# Build list of excerpts for tiles
displayedList=[]

for excerpt in pattern:
	mainData=MyExcerpt(excerpt, maxNumberOfWordsForExcerpt, minumumNumberOfWordsForExcerpt )
	#print ( mainData.numOfUsableExceprts() )
	#print ( mainData.returnOmitted () )
	#print ( "OMITTING OMITTING : %s" % ( mainData.returnOmitted () )  )
	#sumOfExcerpts+=mainData.sumOfTiles()
	
	# If the value is not None add to the variable sumOfExcerpts
	if ( mainData.sumOfTiles() ):
		sumOfExcerpts+=mainData.sumOfTiles()
	
	# If the value is not None add to the variable sumPrintable
	if ( mainData.numOfUsableExceprts() ):
		sumPrintable+=1
				
	
	# Check that its value is not None
	if ( mainData.listOfExcerpt4Pagination() ):
	
		for copy in  mainData.listOfExcerpt4Pagination() :			
			displayedList.append(copy)
			
	if ( mainData.returnOmitted() ):
		listOfOmitted.append ( mainData.returnOmitted() )
	
	#mainData.sumOfTiles()
	#print ( type ( mainData.numExcerptsByWord() ) )
	#mainData.sumOfTiles()

	# Stats
print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle[0:-2] ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

for copy in displayedList:
	pnum+=1
	# This creates a name for the image
	theFileName2 = str (pnum)+".png"
	
	# DIsplay what is being places on tile
	print ( excerptTitle + copy )
	
	# Add excerpt to the image
	subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity northwest -pointsize 60 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +30+0 "%s" -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 "%s" %s' % (excerptTitle + copy , str( pnum )+"/"+ str (sumOfExcerpts), authorsName,theFileName2), shell=True )

# Stats	
print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle[0:-2] ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

# Display what was ommited if list is not blank
if (listOfOmitted ):
	print ("The following were OMITTED ::" )
	for copy in listOfOmitted:
		print ( copy , end="")
