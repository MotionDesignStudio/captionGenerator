# captionGenerator
Make Captions From Kindle's 'My Clippings.txt' File And More

Reading is important and I do it frequently.  Sharing my discoveries have become an important process.  Why learn something amazing and not pass it on?  In an attempt to make this easier for myself and others.  I created this script.  Currently it only works with some of Amazon’s Kindles 'My Clippings.txt' text file.  If you know regex you can modify for any text file with a recurring structural delimiter.  

I will add more functionality and restructure the script to use classes.  

Thanks and keep reading to free yourself from yourself.

] Dependencies  [
- imagemagick , python3

] USAGE Version 1.0 [

This variable is the name of the book printed at the top of each excerpt.
excerptTitle = 'The Subtle Art of Not Giving a F*ck:\n'
The trailing \n means place a line break after the title.

This variable >> minumumNumberOfWordsForExcerpt = 10 << sets the minimum number of words for a stand alone except.  It must be less than >> maxNumberOfWordsForExcerpt = 70 << .

This >> externalFileToRegexOver = "My Clippings.txt" << is the name of the text file containing the excerpt(s).

This >> authorsName = 'Mark Manson' << is the name printed at the bottom of each image.

This >> pattern = re.findall(r'^The Subtle Art of Not[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M ) << is the regular express you can modify for any text file with a recurring structural delimiter.  

In the >> example << directory are excerpts from Mark Manson’s book The Subtle Art of Not Giving a F*ck.  These are generated from 'My Clippings.txt' text file.  This file is located on your designated Kindle device for reading.   Its contents are all the excerpts you highlighted from every book.

] IMPORTANT [

… BLAH BLAH … means this except is apart of a larger.  The … before means it is part of the slide before and the trailing … means the next is connected to it.  

… BLAH BLAH means this except is apart of a larger.  The … before means it is part of the slide before.

] EXAMPLE ImageMagick command [

convert bgPapaer.jpg \( -size 950x950 -background "rgba(0,0,0,0)" -font /path/to/font/OpenSans-ExtraBold.ttf -fill "#000000" caption:"$(cat ./temp.txt)" \( +clone -shadow 0x0+0+0 \) +swap -background "rgba(0,0,0,0)" -layers merge +repage \) -gravity center -composite -gravity northwest -pointsize 50 -font /path/to/font/Typoster_ROCK_ON.otf -annotate +30+0 "1/232" -gravity south -pointsize 40 -font /path/to/font/Typoster_ROCK_ON.otf -annotate +0+10 "Robert Greene, Joost Elffers" r2.png

] CONNECT [

https://www.facebook.com/motiondesignstudio/

https://www.youtube.com/motiondesignstudio/

https://www.instagram.com/motiondesignstudio/
