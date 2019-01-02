# captionGenerator
Make Captions From Kindle's 'My Clippings.txt' File And More

Reading is important and I do it frequently.  Sharing my discoveries have become an important process.  Why learn something amazing and not pass it on?  In an attempt to make this easier for myself and others.  I created this script.  Currently it only works with some of Amazon’s Kindles 'My Clippings.txt' text file.  If you know regex you can modify for any text file with a recurring structural delimiter.  

I will add more functionality and restructure the script to use classes.  

Thanks and keep reading to free yourself from yourself.

] USAGE [

This variable is the name of the book printed at the top of each excerpt.
excerptTitle = 'The Subtle Art of Not Giving a F*ck:\n'
The trailing \n means place a line break after the title.

This variable >> minumumNumberOfWordsForExcerpt = 10 << sets the minimum number of words for a stand alone except.  It must be less than >> maxNumberOfWordsForExcerpt = 70 << .

This >> externalFile = Path("My Clippings.txt").read_text() << is the name of the text file containing the excerpt(s).

This >> pattern = re.findall(r'^The Subtle Art of Not[\s\S]+?\d{2}:\d{2} [AP]M\s+([^=]+)', externalFile, re.M ) << is the regular express you can modify for any text file with a recurring structural delimiter.  

In the >> example << directory are excerpts from Mark Manson’s book The Subtle Art of Not Giving a F*ck.  These are generated from 'My Clippings.txt' text file.  This file is located on your designated Kindle device fore reading.   Its contents are all the excerpts you highlighted from every book.

] IMPORTANT [

… BLAH BLAH … means this except is apart of a larger.  The … before means it is part of the slide before and the trailing … means the next is connected to it.  

… BLAH BLAH means this except is apart of a larger.  The … before means it is part of the slide before.

] CONNECT [

https://www.facebook.com/motiondesignstudio/

https://www.youtube.com/motiondesignstudio/

https://www.instagram.com/motiondesignstudio/