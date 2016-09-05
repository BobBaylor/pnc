# pnc
## What is this?
This python script converts an old panasonic IP camera (.PNC file) output to individual .JPG files.
## What are PNC files?
Mid 2000s era Panasonic IP cameras such as the BL-C140A (the one I have) can store a sequence of images to their internal RAM (or SD card, in some models). The sequence can be captured whenever motion is detected or on a time-of-day schedule. The cameras have a web interface and will create a PNC file when you click on the "Download" button while looking at one of the "Buffered Image" tabs. Your browser downloads the .PNC file to wherever your browser downloads things (e.g. /Users/bob/Downloads/) and there it sits, useless unless you open it with the lame Panasonic app.  

Panasonic's [viewer app](http://panasonic.net/pcc/cgi-bin/products/netwkcam/download_other/tbookmarka_m.cgi?mm=2010050617102616) (Windows only) has a primitive UI and no way to save more than one image at a time. I took a look at a PNC file one day (when I was supposed to be doing something else, I'm sure), and noticed that the PNC file appears to be just a bunch of JPEG files stuck on the end of a header.  
## How do I use it?
 * First, you need to "install" it:
   * You need python to use this script. Macs and Linux computers come with python. Windows, not so much. Any python will do, I think, but I've only tested it with 2.7 so if you see a choice of installing 2.something or 3.something, install the 2.something.
  * Put the script (pnc.py) into some folder on your computer. 
  * Edit line 67 to point to the place your browser puts downloads.

 * Then, to run it:
   * open a command shell in the folder that you put pnc.py
   * type `python pnc.py` to put the output (JPEG files) in a folder that's just named with the date and time.
   * type `python pnc.py "some reminder"` to append "some reminder" to the folder name.
  
 * Assuming pnc.py finds a file called JpegData.PNC in the folder on line 67, it will 
   * create a folder named with the current date and time
   * unpack the JPEG images as separate files into the folder it just created
   * move the original JpegData.PNC file into the new folder
  
## Bugs and apologies
 * Some images come out all black. It seldom happens so I haven't bothered to see what's wrong. 
 * It's one the first python scripts I ever wrote, so it's not very ["pythonic"](https://www.python.org/dev/peps/pep-0008/). 
