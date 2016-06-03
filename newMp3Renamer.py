#! /usr/bin/env python
# newMp3Renamer.py - Renames MP3 files using ID3 data.
# argv is the directory which contains the MP3 files (or the directories that
# contain them).

import shutil, os, re, mutagen
from mutagen.easyid3 import EasyID3
from sys import argv

script, mp3dir = argv

# TODO: walk through folders and subfolders, read MP3 ID3tag, store
# artist/tracknumber into separate variables, create a new filename, check if
# the created filename matches with the actual filename of the file, if it does
# don't touch it, if it doesn't proceed with the renaming. Count the renamed
# files and the not renamed ones, print the output.

renamedCounter = 0
notRenamedCounter = 0


for folder, subfolders, filenames in os.walk(mp3dir):
    for filename in filenames:
        filename = str(os.path.join(os.path.abspath\
                                (folder), filename)).decode('utf-8')
        if filename.endswith('.mp3'):
            filename = os.path.abspath(filename)
            filename = filename.encode('utf-8')
            try:
                fileid3info = EasyID3(filename)
            except (mutagen.id3.ID3NoHeaderError):
                print ('The file %s doesn\'t appear to have '
                       'any ID3 tag information, so it won\'t '
                       'be touched.') % filename
                notRenamedCounter += 1
                continue
            try:
                title = fileid3info['title'][0]
            except KeyError:
                print('There is no ID3 data for the '
                      'title in the file %s') % filename
                notRenamedCounter += 1
                continue
            try:
                trackNumber = fileid3info['tracknumber'][0]
            except KeyError:
                print('There is no ID3 data for the '
                      'track number in the file %s') % filename
                notRenamedCounter += 1
                continue
            if title and trackNumber != None:
                if '/' in trackNumber:
                    trackNumber = trackNumber.split('/')
                    trackNumber = trackNumber[0]
                if len(trackNumber) == 1:
                    trackNumber = '0' + trackNumber
                    x = ['/', '\\']
                    y = ['*', '|']
                    z = [':', ';', '=']
                    for i in x:
                        if i in title:
                            title.replace(i, '-')
                    for i in y:
                        if i in title:
                            title.replace(i, ' ')
                    for i in z:
                        if i in title:
                            title.replace(i, ' - ')
                    if '[' in title:
                        title.replace('[', '(')
                    if ']' in title:
                        title.replace(']', ')')
                    if '"' in title:
                        title.replace('"', "'")
                    newFilename = trackNumber + ' - ' + title + '.mp3'
                    absfilename = os.path.join(os.path.abspath(folder),
                                           newFilename).encode('utf-8')
                    if absfilename == filename:
                        print('The file %s is already correctly '
                              'named.') % absfilename
                        notRenamedCounter += 1
                        continue
                    print ('Renaming %s to %s ...') % (filename,
                                                       absfilename)
                    renamedCounter +=1

#                        shutil.move(filename, absfilename)
print ('A total of %s files were renamed.') % renamedCounter
print ('A total of %s files weren\'t touched.') % notRenamedCounter
