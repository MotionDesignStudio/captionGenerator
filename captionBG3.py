#!/usr/bin/env python3.7

import re
from pathlib import Path
import subprocess
from subprocess import PIPE, run
import math
from shlex import quote
import os
# Use this to process commandline arguments
#import sys, getopt
import argparse


# Test if string is a file or string
def checkIfFileOrString ( whatAmI ):
	return os.path.isfile(whatAmI) 

# Produce a single tile
def singleTile( myString, SauthorsName, SexcerptTitle, StheFileName2, Spnum, SsumOfExcerpts  ):
	print ( myString )
	
	# passed in variables
	authorsName = SauthorsName
	excerptTitle = SexcerptTitle
	theFileName2 = StheFileName2	
	pnum = Spnum
	sumOfExcerpts = SsumOfExcerpts		
	
	# Add excerpt to the image
	subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+60 "%s" -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 "%s" -gravity north -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 %s %s' % ( myString , str( pnum )+"/"+ str (sumOfExcerpts), authorsName, excerptTitle, theFileName2), shell=True )



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
				listToReturn.append( "".join ( listOfWords[ :self.maxWrdsOrStr ] )  )
				del listOfWords[ :self.maxWrdsOrStr ]
				
			return listToReturn
	
	
	def addLDotsistOfExcerpt4Pagination(self):
		listWithDots=[]
		# This stop the error of None text being found and sent for processing
		if ( self.listOfExcerpt4Pagination() ):
				
			# Length of list variable  
			lengthOfList = len ( self.listOfExcerpt4Pagination() ) 

			# Check the array is one in length
			if (  len ( self.listOfExcerpt4Pagination() ) == 1 ) :
				listWithDots.append( self.listOfExcerpt4Pagination()[0] )
		
			# Check the array is two in length
			if (  len ( self.listOfExcerpt4Pagination() ) == 2 ) :
				listWithDots.append(self.listOfExcerpt4Pagination()[0]+"...")
				listWithDots.append( "..."+self.listOfExcerpt4Pagination()[1] )
			
			# Check the array is three in length or greater
			if (  len ( self.listOfExcerpt4Pagination() ) > 2 ) :
				# First position
				#print (self.listOfExcerpt4Pagination()[0]+"...")
				
				listWithDots.append(self.listOfExcerpt4Pagination()[0]+"...")
				
				#print (self.listOfExcerpt4Pagination()[2]+"...")
				
				# I subtract one as to not add trailing three dots
				for i in range (1,lengthOfList-1):
					#print ("..."+self.listOfExcerpt4Pagination()[i]+"...")
					listWithDots.append( "..."+self.listOfExcerpt4Pagination()[i]+"..." )
				
				listWithDots.append(  "..."+self.listOfExcerpt4Pagination()[lengthOfList-1]  )
				#print ("..."+self.listOfExcerpt4Pagination()[lengthOfList-1] )
		return listWithDots

def createTiles ( CTPattern, CTexcerptTitle,  CTmaxNumberOfWordsForExcerpt, CTminumumNumberOfWordsForExcerpt, CTenableFacebookTimeStamp ):
	# Total number of excerpt(s) I will print
	sumOfExcerpts = 0
	
	# The file name
	CTtheFileName2 = ""
	
	# Total number of excerpt(s) found in original document
	sumPrintable = 0
	
	# Page number
	CTpnum=0
	
	# This is number of second to subtract for creation and modifaction time
	# This is used to force Facebook to display the files from 1 to XXX.
	startTime =1546300800
	adjustedTimeStampBy=1000
	
	externalFile = ""
	pattern = ""
	
	# This list stores ommited excerpts
	listOfOmitted=[]

	# Build list of excerpts for tiles
	displayedList=[]
	
	# saving passed variales 
	pattern = CTPattern
	excerptTitle = CTexcerptTitle
	maxNumberOfWordsForExcerpt = CTmaxNumberOfWordsForExcerpt
	minumumNumberOfWordsForExcerpt = CTminumumNumberOfWordsForExcerpt
	enableFacebookTimeStamp = CTenableFacebookTimeStamp
	
	
	for excerpt in pattern:
		mainData=MyExcerpt(excerpt, maxNumberOfWordsForExcerpt, minumumNumberOfWordsForExcerpt )

		# If the value is not None add to the variable sumOfExcerpts
		if ( mainData.sumOfTiles() ):
			sumOfExcerpts+=mainData.sumOfTiles()

		# If the value is not None add to the variable sumPrintable
		if ( mainData.numOfUsableExceprts() ):
			sumPrintable+=1


		# Check that its value is not None
		if ( mainData.listOfExcerpt4Pagination() ):

			# I want to return the exerpts with dots here		
			for copy in mainData.addLDotsistOfExcerpt4Pagination() :		
				displayedList.append(copy)

		if ( mainData.returnOmitted() ):
			listOfOmitted.append ( mainData.returnOmitted() )


	print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

	for copy in displayedList:
		CTpnum+=1
		# This creates a name for the image
		CTtheFileName2 = str (CTpnum)+".png"

		# Display what is being placed on tile
		print ( excerptTitle+"\n" + copy )

		# Add excerpt to the image
		subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+60 "%s" -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 "%s" -gravity north -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 %s %s' % ( copy , str( CTpnum )+"/"+ str (sumOfExcerpts), authorsName, excerptTitle, CTtheFileName2), shell=True )

		if ( enableFacebookTimeStamp == "t" ):
			startTime-=adjustedTimeStampBy
			os.utime(CTtheFileName2 , ( startTime , startTime ))

	# Stats	
	print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

	# Display what was ommited if list is not blank
	if (listOfOmitted ):
		print ("The following were OMITTED ::" )
		for copy in listOfOmitted:
			print ( copy , end="")

# End createTiles ()
			
			
# Initial call to the main function

if __name__ == "__main__":
	#main ( sys.argv[1:] )
	parser = argparse.ArgumentParser( description="This creates images using excerpt(s) from a Kindle 'My Clippings.txt' file or a different file with same structure or a string." )
	excerptTitle = ''
	parser.add_argument( "-c", "--caption", help="Add a file to extract caption or text for caption(s)", required='True', type=str )
	parser.add_argument( "-a", "--authors", help="Author(s) name(s)", required='True', type=str )
	parser.add_argument( "-t", "--title", help="Document title", required='True', type=str )
	parser.add_argument( "-e", "--excerpt", help="Exerpt to search for", required='True', type=str )
	
	parser.add_argument( "-de", "--denominator", help="Starting number for denominator", default=0, type=int )
	parser.add_argument( "-nu", "--numerator", help="Starting number for numerator", default=0, type=int )
	parser.add_argument( "-mi", "--minwords", help="Minumum words per tile, default is 10", default=10, type=int )
	parser.add_argument( "-mx", "--maxwords", help="Max words per tile, default is 70", default=70, type=int )
	parser.add_argument( "-d", "--dryrun", help="Dry run", default="f", type=str, choices=["t","f"] )
	parser.add_argument( "-rt", "--reversetimestamp", help="Reverse timestamps", default="f", type=str, choices=["t","f"] )

	args = parser.parse_args()
	
	authorsName = ""
	excerptTitle = ""
	externalFileToRegexOver = ""
	
	# Page number
	pnum=0
	
	# Checking if caption has content such as a file or string
	if ( "".join (args.caption.split() ) and "".join (args.authors.split() ) and "".join (args.title.split() ) and "".join (args.excerpt.split() )  ):
		#print ("HAS CONTENT : "+ args.authors)
		authorsName = args.authors
		excerptTitle = quote(args.title)
		externalFileToRegexOver = args.caption
		
		# If the caption variable contains a string 
		if checkIfFileOrString(args.caption) :
			
			externalFile = Path( externalFileToRegexOver ).read_text()
			pattern = re.findall(r'^'+ args.excerpt +'[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
			
			createTiles( pattern, excerptTitle, args.maxwords , args.minwords, args.reversetimestamp )
			# Must pass vaiables
		else :
			print ("This is a string")
			theFileName2 = "1.png"
			sumOfExcerpts = args.denominator
			pnum = args.numerator
			singleTile ( args.caption, authorsName, excerptTitle, theFileName2, pnum, sumOfExcerpts  )
			
	
	#if ( args.dryrun == "t" ):
	#	print ( "DRY RUN BABY" )