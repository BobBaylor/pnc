

import os.path
import sys
import string
import time

def getPhotos(fileIn, outpath,outFNameBase,fileNo,bMoveSrc):
    """The PNC is a panasonic proprietary file format that simple pre-pends a header onto a bunch of
        jpeg images. Extracting the jpegs into usable files is simply a matter of slicing them out -
        each image is a complete jpeg with header, color tables, etc."""

    bLast = ''
    if( False ): # os.path.isdir(outpath) ):
        print "Directory %s already exists. Delete it or choose a different name." % outpath
    else:
        try:
            fileCount = 0
            timeStart = time.time()
            pnc = open(fileIn,"rb")
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
            bytesIn = pnc.read()            # get the entire file
            print "Found %d bytes in %s" % (len(bytesIn), fileIn)
            bLast = '1'         # init it to anything except 0xff
            bFirst = True       # don't close and re-open the first output file
            bInImage = False    # skip the PNC preamble

            fileOut = "%s//%s%04d.jpg" % (outpath,outFNameBase,fileNo)
            image = open(fileOut,"wb")

            for bv in bytesIn:
                if (bLast == b'\xff') and (bv == b'\xd8'):
                    bInImage = True
                    fileOut = "%s//%s%04d.jpg" % (outpath,outFNameBase,fileNo)
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

        except:
            print "Did nothing",
            if not os.path.isfile( fileIn ):
                print "because %s doesn't seem to exist." % (fileIn)
            return False


def main(argv):
    """Application startup: create app and start main loop."""
    if( len(argv) != 2 ):
        print "Usage: %s dirName" % (argv[0])
    else:
        getPhotos("/Users/bob/Downloads/JpegData.PNC",argv[1],'test',0,True)

if __name__ == '__main__':
    main(sys.argv)

