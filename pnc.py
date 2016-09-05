#!/usr/bin/env python

import os.path
import sys
import platform
import string
import time
import traceback
import datetime as dt

def getPNCfilename():    
    'determine the OS so we can use the proper path to the PNC data'
    myos = platform.system()    # returns 'Linux', 'Darwin', or 'Windows'
    if 'Windows' in myos:                    # I'm on my Win box
        return 'C:/Users/rab/Downloads/JpegData.PNC'
    elif 'Darwin' in myos:                     # I'm at 260 or 7C
        if 'guys' in platform.node():
            return '/Users/guy/Downloads/JpegData.PNC'
        else:    
            return '/Users/bob/Downloads/JpegData.PNC'
    else:   # I don't know where I am
        print 'where am I?',myos
        return '.'    #perhaps the PNC file is right under my nose


def log_traceback(ex, ex_traceback):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    for x in tb_lines:
        print x


def getPhotos(fileIn, outpath,outFNameBase,fileNo,bMoveSrc):
    """The PNC is a panasonic proprietary file format that simple pre-pends a header onto a bunch of
        jpeg images. Extracting the jpegs into usable files is simply a matter of slicing them out -
        each image is a complete jpeg with header, color tables, etc."""

    bLast = ''
    try:
        fileCount = 0
        timeStart = time.time()
        y = os.path.getmtime(fileIn)
        z = dt.datetime.fromtimestamp(y)
        outpath = ''.join([z.strftime('%Y-%m-%d %H-%M-%S'),outpath])
        pnc = open(fileIn,"rb")
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        bytesIn = pnc.read()            # get the entire file
        print "Found %d bytes in %s" % (len(bytesIn), fileIn)
        bLast = '1'         # init it to anything except 0xff
        bFirst = True       # don't close and re-open the first output file
        bInImage = False    # skip the PNC preamble

        fileOut = os.path.join(outpath,"%s%04d.jpg" % (outFNameBase,fileNo))
        image = open(fileOut,"wb")

        for bv in bytesIn:
            if (bLast == b'\xff') and (bv == b'\xd8'):
                bInImage = True
                fileOut = os.path.join(outpath,"%s%04d.jpg" % (outFNameBase,fileNo))
                if not bFirst:
                    image.close()
                    image = open(fileOut,"wb")
                fileNo += 1
                fileCount += 1
                image.write( b'\xff' ),
                bFirst = False
            if bInImage:
                image.write( bv ),
            bLast = bv

        pnc.close()
        if bMoveSrc:
            os.rename( fileIn, "%s//JpegData.PNC" % (outpath) )
        image.close()
        secs = time.time() - timeStart
        print "Wrote %d files in dir %s in %.2f seconds" % (fileCount, outpath, secs)
        return True

    except (ValueError, IndexError) as err:
        _, _, ex_traceback = sys.exc_info()
        log_traceback(err, ex_traceback)
        if not os.path.isfile( fileIn ):
            print "because %s doesn't seem to exist." % (fileIn)
        print "Did nothing",
        return False


def main(argv):
    tExtra = '' if len(argv) < 2 else argv[1]   # no cmd line arg means create dir based on current time
    getPhotos(getPNCfilename(),tExtra,'garage',0,True)

if __name__ == '__main__':
    main(sys.argv)

