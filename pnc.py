#!/usr/bin/env python
"""  PNC.PY slices out the images in an old panasonic IP cam file
"""
import os.path
import shutil
import sys
import platform
import time
import traceback
import datetime as dt

def get_pnc_file_name():
    """determine the OS so we can use the proper path to the PNC data"""
    myos = platform.system()    # returns 'Linux', 'Darwin', or 'Windows'
    if 'Windows' in myos:                    # I'm on my Win box
        return r'C:/Users/rab/Downloads/JpegData.PNC'
    elif 'Darwin' in myos:                     # I'm at 260 or 7C
        if 'guys' in platform.node():
            return r'/Users/guy/Downloads/JpegData.PNC'
        elif 'MacBook' in platform.node():
            return r'/Users/bobbaylor/Downloads/JpegData.PNC'
        return r'/Users/bob/Downloads/JpegData.PNC'
    print('where am I?', myos)
    return '.'    #perhaps the PNC file is right under my nose


def log_traceback(ex, ex_traceback):
    """ format exception traceback"""
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    for one_line in tb_lines:
        print(one_line)


def make_output_dir(file_in, text_extra):
    """ create the ouput dir """
    time_file = os.path.getmtime(file_in)
    date_time_file = dt.datetime.fromtimestamp(time_file)
    out_dir = ''.join([date_time_file.strftime('%Y-%m-%d %H-%M-%S'), text_extra])
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    return out_dir

def get_pnc_bytes(file_in):
    """ read in the raw file """
    pnc_file = open(file_in, "rb")
    bytes_in = pnc_file.read()            # get the entire file
    pnc_file.close()
    print ("Found %d bytes in %s" % (len(bytes_in), file_in))
    return bytes_in

def get_photos(file_in, text_extra, out_file_name_base, b_move_src):
    """The PNC is a panasonic proprietary file format that simple pre-pends a header onto a bunch of
        jpeg images. Extracting the jpegs into usable files is simply a matter of slicing them out -
        each image is a complete jpeg with header, color tables, etc."""
    # I use abot 16 locals but pylint says 15 max
    #pylint: disable=too-many-locals
    byte_last = ''
    try:
        out_dir = make_output_dir(file_in, text_extra)
        bytes_in = get_pnc_bytes(file_in)
        # print('bytes_in = ',len(bytes_in),type(bytes_in),type(bytes_in[0]))
        # print(' '.join(['%02X'%c for c in bytes_in[:16]]))
        byte_last = 1             # init it to anything except 0xff
        b_first_time = True       # don't close and re-open the first output file
        b_in_image = False    # skip the PNC preamble
        file_count = 0
        file_out = os.path.join(out_dir, "%s%04d.jpg" % (out_file_name_base, file_count))
        image = open(file_out, "wb")
        # byte_ff = bytearray([0xff])
        # byte_d8 = bytearray([0xd8])
        for byte_val in bytes_in:
            # if (byte_last == byte_ff) and (byte_val == byte_d8):
            if (byte_last == 0xff) and (byte_val == 0xd8):
                b_in_image = True
                file_out = os.path.join(out_dir, "%s%04d.jpg" % (out_file_name_base, file_count))
                if not b_first_time:
                    image.close()
                    image = open(file_out, "wb")
                file_count += 1
                image.write(bytearray([0xff]))
                b_first_time = False
            if b_in_image:
                # print('%02X'%byte_val)
                image.write(bytearray([byte_val]))
                # return
            byte_last = byte_val

        if b_move_src:
            shutil.move(file_in, "%s//JpegData.PNC"%out_dir)
        image.close()
        return True, file_count, out_dir
    # except (ValueError, IndexError, WindowsError) as err:
    except Exception as err:
        _, _, ex_traceback = sys.exc_info()
        log_traceback(err, ex_traceback)
        if not os.path.isfile(file_in):
            print ("FAILURE because %s doesn't seem to exist."%(file_in))
        print ("Did nothing",)
        return False, 0, "<blank>"


def main(argv):
    """ no cmd line arg means create dir based on current time """
    text_extra = '' if len(argv) < 2 else argv[1]
    time_start = time.time()
    _, file_count, out_dir = get_photos(get_pnc_file_name(), text_extra, 'garage', True)
    secs = time.time() - time_start
    print ("Wrote %d files in dir %s in %.2f seconds"%(file_count, out_dir, secs))

if __name__ == '__main__':
    main(sys.argv)
