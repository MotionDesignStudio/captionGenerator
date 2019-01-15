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

#excerptTitle = 'Robert F. Williams, Negroes With Guns :\n'
#excerptTitle = 'How to Be an Adult in Relationships:\n'
#excerptTitle = 'Getting to Maybe:\n'
#excerptTitle = 'The 48 Laws of Power:\n'
#excerptTitle = 'Negroes With Guns:\n'
#excerptTitle = 'Outrageous Openness:\n'
#excerptTitle = 'The Subtle Art of Not Giving a F*ck:\n'
#excerptTitle = 'Flow: The Psychology of Optimal Experience'
#excerptTitle = quote('Flow: The Psychology of Optimal Experience')
#excerptTitle = quote('The Matrix as Metaphysics')
#authorsName = 'Tosha Silver'
#authorsName = 'Mark Manson'
#authorsName = 'Robert Greene; Joost Elffers'
#authorsName = 'Robert F Williams'
#authorsName = 'Mihaly Csikszentmihalyi'
#authorsName = 'David J. Chalmers'


authorsName = ''
excerptTitle = ''

#externalFileToRegexOver = "My Clippings.txt"
#externalFileToRegexOver = "smallExample.txt"
externalFileToRegexOver = ""

minumumNumberOfWordsForExcerpt = 10
maxNumberOfWordsForExcerpt = 70
	
numIterations=0

# This is number of second to subtract for creation and modifaction time
# This is used to force Facebook to display the files from 1 to XXX.
enableFacebookTimeStamp=False
startTime =1546300800
adjustedTimeStampBy=1000

# Open file for regex
#externalFile = Path( externalFileToRegexOver ).read_text()

#externalFile = Path( externalFileToRegexOver ).read_text()
externalFile = ""

pattern = ""
#pattern = re.findall(r'^Flow: The Psychology of Optimal Experience[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )

#pattern = re.findall(r'^Negroes With Guns[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^The Subtle Art of Not[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^Flow: The Psychology of Optimal Experience[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^﻿Microsoft Word - matrix[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^Getting to Maybe[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
#pattern = re.findall(r'^The 48 Laws of Power[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )

# Page number
pnum=0

# Totoal number of excerpt(s) I will print
sumOfExcerpts = 0

# The file name
theFileName2 = ""

# Processing commandline arguments

def main (argv):
	print ("Inside Main")

"""

def main (argv):
	inputFileOrCopy=""
	try:
		opts, args = getopt.getopt( argv,"hi:d", ["input="] )
		print ( opts )
		print ( args )
	except getopt.GetoptError:
		print ("Use like this :: ./captionBG3.py 'My Clipping.txt'")
		sys.exit(2)
		
	for opt, arg in opts:
		if opt == "-h":
			print ("Use like this ::::::: ./captionBG3.py 'My Clipping.txt'")
"""

# Tests if string is a file or string
def checkIfFileOrString ( whatAmI ):
	return os.path.isfile(whatAmI) 

# Produce a single tile
def singleTile( myString ):
	print ( myString )
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

def createTiles ():
	# Total number of excerpt(s) found in original document
	sumPrintable = 0
	# This list stores ommited excerpts
	listOfOmitted=[]

	# Build list of excerpts for tiles
	displayedList=[]
	
	print ( "II pattern  ::  ")
	print ( pattern )

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

			# I want to return the exerpts with dots here		
			for copy in mainData.addLDotsistOfExcerpt4Pagination() :			
			#for copy in mainData.listOfExcerpt4Pagination() :			
				displayedList.append(copy)

		if ( mainData.returnOmitted() ):
			listOfOmitted.append ( mainData.returnOmitted() )



		#mainData.sumOfTiles()
		#print ( type ( mainData.numExcerptsByWord() ) )
		#mainData.sumOfTiles()

		
	#print ( "III sumOfExcerpts  ::  "+ sumOfExcerpts )	
		# Stats
	#print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle[0:-2] ,sumOfExcerpts, sumPrintable ), end ="\n\n" )
	print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle ,sumOfExcerpts, sumPrintable ), end ="\n\n" )

	for copy in displayedList:
		pnum+=1
		# This creates a name for the image
		theFileName2 = str (pnum)+".png"

		# Display what is being placed on tile
		#print ( excerptTitle+"\n" + copy )

		# Add excerpt to the image
		#subprocess.call ('convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /home/lex/share/Mo_De_Studio/audio_blog/OpenSans/OpenSans-ExtraBold.ttf -fill "#000000" caption:"%s" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+60 "%s" -gravity south -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 "%s" -gravity north -pointsize 40 -font /home/lex/share/python/ffmpegHelper/fonts/Typoster_ROCK_ON.otf -annotate +0+10 %s %s' % ( copy , str( pnum )+"/"+ str (sumOfExcerpts), authorsName, excerptTitle, theFileName2), shell=True )

		if ( enableFacebookTimeStamp ):
			startTime-=adjustedTimeStampBy
			os.utime(theFileName2 , ( startTime , startTime ))

	# Stats	
	#print ( '"%s" | %s Excerpt(s) Pages | %s From Origin Document' % ( excerptTitle[0:-2] ,sumOfExcerpts, sumPrintable ), end ="\n\n" )
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

	parser.add_argument( "-c", "--caption", help="Add a file or text for caption(s)", required='True', type=str )
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
	#parser.parse_args()
	#print ( args.echo )
	#print ( args.input + " : " + args.input )
	
	#if ( args.caption ):
	#if not args.caption in (None, ''):
		#print ( "Test For File : %s" % (args.caption) )
		#print ( checkIfFileOrString(args.caption) )
	
	#print ( "".join (args.caption.split()  ) )
	
	# Checking if caption has content such as a file or string
	if ( "".join (args.caption.split() ) and "".join (args.authors.split() ) and "".join (args.title.split() ) and "".join (args.excerpt.split() )  ):
		print ("HAS CONTENT : "+ args.authors)
		authorsName = args.authors
		excerptTitle = quote(args.title)
		externalFileToRegexOver = args.caption
		externalFile = Path( externalFileToRegexOver ).read_text()
		pattern = re.findall(r'^'+ args.excerpt +'[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M )
		
		# If the caption variable contains a string 
		if checkIfFileOrString(args.caption) :
			print ("This is a file" )
			createTiles()
		else :
			print ("This is a string")
			theFileName2 = "1.png"
			sumOfExcerpts = args.denominator
			pnum = args.numerator
			singleTile ( args.caption )
	
	#if ( args.dryrun == "t" ):
	#	print ( "DRY RUN BABY" )