#!/bin/env python
# -*- coding: utf-8 -*-
"""A CLI tool to extract Soundcraft Show files"""

from __future__ import print_function

__author__ = 'Raphaël Doursenaud'

import argparse
import sys
from base64 import b64decode
from zlib import decompress
from os.path import basename, splitext, join, exists
from os import mkdir

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Extract Soundcraft Show files.")
parser.add_argument('infiles', metavar="INFILE", type=argparse.FileType('r'),
                    default=sys.stdin, nargs='+',
                    help="The show file(s) to extract.")

args = parser.parse_args()

for file in args.infiles:
    print("Processing " + file.name + ", ", end="")

    soup = BeautifulSoup(file, features='xml')
    collection = soup('MHxDFile')
    size = len(collection)
    outfilepath = basename(file.name)

    # Remove extension
    outfilepath = splitext(outfilepath)[0]

    print("found " + str(size) + " files")

    # Prepare output folder
    if not exists(outfilepath):
        mkdir(outfilepath)

    for entry in collection:
        filename = entry['name']

        # Extract only filename from path
        filename = filename.rsplit('\\', 1)[-1]

        print("Processing (decoding & decompressing) " + filename + " in ./" + outfilepath + "/")

        checksum = int(entry['checksum'])
        datalength = int(entry['datalength'])
        contents = entry.contents[0]

        # Base64 decode
        try:
            contents = b64decode(contents, validate=True)
        except TypeError:
            # We're most likely running python 2, let's try without validate
            contents = b64decode(contents)

        # zlib decompress
        contents = decompress(contents)

        # TODO: Validate the data against the checksum when identified

        if len(contents) != datalength:
            raise Exception("Data size missmatch!")

        # Write result to file
        outfile = join(outfilepath, filename)
        if exists(outfile):
            answer = input("File " + outfile + " already exists! Overwrite? [y/N]")
            if not (answer == 'Y' or answer == 'y'):
                print("Skipping…")
                continue
        fh = open(outfile, 'wb')
        fh.write(contents)
        fh.close()
