#!/usr/bin/env python3.7

import re
from pathlib import Path
import subprocess
from subprocess import PIPE, run
import math

#excerptTitle = 'Robert F. Williams, Negroes With Guns :\n'
#excerptTitle = 'How to Be an Adult in Relationships:\n'
#excerptTitle = 'Getting to Maybe:\n'
#excerptTitle = 'The 48 Laws of Power:\n'
#excerptTitle = 'Negroes With Guns:\n'
#excerptTitle = 'Outrageous Openness:\n'
excerptTitle = 'The Subtle Art of Not Giving a F*ck:\n'
#authorsName = 'Tosha Silver'
authorsName = 'Mark Manson'
#authorsName = 'Robert Greene; Joost Elffers'
#authorsName = 'Robert F Williams'

#externalFileToRegexOver = "My Clippings.txt"
externalFileToRegexOver = "mcSMALL.txt"

minumumNumberOfWordsForExcerpt = 10
maxNumberOfWordsForExcerpt = 70
	
numIterations=0

# Open file for regex
externalFile = Path( externalFileToRegexOver ).read_text()
#pattern = re.findall(r'^Negroes With Guns[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
pattern = re.findall(r'^The Subtle Art of Not[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^Getting to Maybe[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^The 48 Laws of Power[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )


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
		
		# This variable I use to keep track of the first tile
		doOnce=True
		
		# This will return a list of strings for paginating as long as they meets the required
		# word(s) length
		if ( self.numberWords()>self.minWrdsOrStr ):
			while ( len ( listOfWords ) ) :
				
				#print (" doOnce ::::: %s" % (doOnce))
				
				# I am checking for the following conditions if this is the first time into the loop and there are more tiles to create after
				# add three dots after
				#if ( doOnce and len ( listOfWords ) >self.maxWrdsOrStr ):
				#	postDots="..."
				#	doOnce=False
					
				#if ( doOnce==False and len ( listOfWords ) >self.maxWrdsOrStr ):
				#	preDots="..."
				#	postDots="..."
				
				#listToReturn.append( preDots + "".join ( listOfWords[ :self.maxWrdsOrStr ] ) + postDots  )
				listToReturn.append( "".join ( listOfWords[ :self.maxWrdsOrStr ] )  )
				del listOfWords[ :self.maxWrdsOrStr ]
				
				# If there is only enough for one exerpt do not add three ...
				#if ( len ( listOfWords ) < self.maxWrdsOrStr ):
					#listToReturn.append( "".join ( listOfWords[ :self.maxWrdsOrStr ] )  )
				#else:
					#listToReturn.append( "".join ( listOfWords[ :self.maxWrdsOrStr ] )  +"...")
				#del listOfWords[ :self.maxWrdsOrStr ]
				
				# Reset variables
				#preDots=""
				#postDots=""
				
			return listToReturn
	
	
	def addLDotsistOfExcerpt4Pagination(self):
		#self.listOfExcerpt4Pagination()
		#print ("TEST TEST ::: %s" % ( self.listOfExcerpt4Pagination() ) )
		print ("TEST TEST ::: %s" % ( len ( self.listOfExcerpt4Pagination() ) ) )
		
		#These varaible stores the pre and post ...
		preDots=""
		postDots=""
		
		# Length of list variable  
		lengthOfList = len ( self.listOfExcerpt4Pagination() ) 
		
		
		# Check the array is longer than one tile
		if (  len ( self.listOfExcerpt4Pagination() ) > 1 ) :
			
			for i in range (lengthOfList) :
			#print ( i, end="")
			#print ( "%s : %s" % ( i, self.listOfExcerpt4Pagination()[i] )  )
				if (i == 0 ):
					print ( self.listOfExcerpt4Pagination()[i] +"..." )
				
				
				
				
			# This is for list of the length 2
			#if (  len ( self.listOfExcerpt4Pagination() ) == 2 ) :
				
			
			# If longer than one tile
			#for copy in self.listOfExcerpt4Pagination() :
				
			
		
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
			
			#mainData.addLDotsistOfExcerpt4Pagination()
			
	if ( mainData.returnOmitted() ):
		listOfOmitted.append ( mainData.returnOmitted() )
	
	# I want return the exerpts with dot here
	mainData.addLDotsistOfExcerpt4Pagination()
	
	#mainData.sumOfTiles()
	#print ( type ( mainData.numExcerptsByWord() ) )
	#mainData.sumOfTiles()

	# Stats
print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle[0:-2] ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

for copy in displayedList:
	pnum+=1
	# This creates a name for the image
	theFileName2 = str (pnum)+".png"
	
	# DIsplay what is being placed on tile
	print ( excerptTitle + copy )
	
	# Add excerpt to the image
	#subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity northwest -pointsize 60 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +30+0 "%s" -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 "%s" %s' % (excerptTitle + copy , str( pnum )+"/"+ str (sumOfExcerpts), authorsName,theFileName2), shell=True )

# Stats	
print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle[0:-2] ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

# Display what was ommited if list is not blank
if (listOfOmitted ):
	print ("The following were OMITTED ::" )
	for copy in listOfOmitted:
		print ( copy , end="")

