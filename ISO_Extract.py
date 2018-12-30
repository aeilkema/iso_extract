#!/usr/bin/env python
#
# ISO_extract post-processing script for NZBGet.
#
# Copyright (C) 2018 J. Aeilkema <aeilkema@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the program.  If not, see <http://www.gnu.org/licenses/>.
#

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                           ###

# Extract all files in a ISO file.
#
# Author: J. Aeilkema (aeilkema@gmail.com).
# License: GPLv3 (http://www.gnu.org/licenses/gpl.html).
# PP-Script Version: 1.1.
#
# NOTE: This script requires Python 2.x to be installed on your system.
#
# NOTE: This script requires 7Zip and a full path for it in the unpack settings (settings -> unpack -> SevenZipCmd) or in 7ZipFullPath in these settings

##############################################################################
### OPTIONS                                                                   ###
# Enable script (yes, no).
#
# Option to enabled / disabled the script.
#Enabled=yes
# Full path to 7Zip.
#
# Set full path or leave empty to use unpack setting (settings -> unpack -> SevenZipCmd).
#7ZipFullPath=
# Only extract if category is in this list.
#
# This option is to prevent extraction for some categories. e.g. 'Games'. Only add categories which you _WANT TO EXTRACT_.
#
#OnlyForCategories=
# Extract iso's without category (yes, no).
#
# What to do if a iso has no category?.
#
#ExtractWithoutCat=no
# Always extract to subdirectory (yes, no).
#
# Always extract the ISO file(s) to a subdirectory, even if not in base download folder (see note).
#
# NOTE: If the extraction directory is equal to the base download folder (settings -> paths -> Destdir), the files will _ALWAYS_ be extracted to a subdirectory with a name of the ISO file, so in that case this setting will be ignored.
#
# NOTE: An archive could contain multiple ISO files, enable to prevent mixing all files.
#SubDirectory=yes
# Delete ISO file(s) after successful extract (yes, no).
#
# Should ISO file(s) be deleted after a successful extract?.
#
# NOTE: If the extraction directory is equal to the base download folder (settings -> paths -> Destdir), the script will _NOT DELETE_ the ISO files(s) (because otherwise it could delete other ISO files).
#DeleteAfterExtract=no
# Enable debug (yes, no).
#
# Option to enable / disable debuging the script, creates some extra messages.
#Debug=no

### NZBGET POST-PROCESSING SCRIPT                                           ###
##############################################################################

# ****** Changelog ******
# Version 1.0: initial release
# Version 1.1: Function: Added category check
#              Options:  ExtractWithoutCat, extract is current category is empty
#                        OnlyForCategories, list of categories to extract

import os
import sys

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_NONE=95
POSTPROCESS_ERROR=94

# Set vars
download_dir=os.environ['NZBPP_DIRECTORY']
path_7zip=os.environ['NZBOP_SEVENZIPCMD']
fullpath7zip=os.environ.get('NZBPO_7ZipFullPath')
DestDir=os.environ['NZBOP_DESTDIR']
script_enabled=os.environ.get('NZBPO_Enabled', 'yes') == 'yes'
debug_enabled=os.environ.get('NZBPO_Debug', 'yes') == 'yes'
extracttosubdir=os.environ.get('NZBPO_SubDirectory', 'yes') == 'yes'
deleteafterextract=os.environ.get('NZBPO_DeleteAfterExtract', 'yes') == 'yes'
SubDirCommand=' -r'
TempOnlyForCategories=os.environ['NZBPO_OnlyForCategories'].replace(' ,',',')
TempOnlyForCategories=TempOnlyForCategories.replace(', ',',')
OnlyForCategories=TempOnlyForCategories.lower().split(',')
CurrentCategory=os.environ['NZBPP_CATEGORY'].lower()
CatInList=CurrentCategory.lower() in OnlyForCategories
ExtractWithoutCat=os.environ.get('NZBPO_ExtractWithoutCat', 'yes') == 'yes'

if debug_enabled:
    print('[INFO] Categories to extract = %s ' % OnlyForCategories)
    print('[INFO] Current category = %s ' % CurrentCategory)
    print('[INFO] Current category is in list to extract = %s ' % CatInList)
    print('[INFO] Extract if there is no category = %s ' % ExtractWithoutCat)

if CurrentCategory:
    if not CatInList:
        print('[INFO] ISO file is not a category which is in the list of categories to extract, exitting...')
        sys.exit(POSTPROCESS_NONE)
else:
    if not ExtractWithoutCat:
        print('[INFO] ISO file has no category and option ExtractWithoutCat is not yes, exitting...')
        sys.exit(POSTPROCESS_NONE)

# Check if directory still exist (for post-process again)
if not os.path.exists(os.environ['NZBPP_DIRECTORY']):
    print('[ERROR] Destination directory %s doesn\'t exist, exiting' % os.environ['NZBPP_DIRECTORY'])
    sys.exit(POSTPROCESS_NONE)

# Check par and unpack status for errors
if os.environ['NZBPP_PARSTATUS'] == '1' or os.environ['NZBPP_PARSTATUS'] == '4' or os.environ['NZBPP_UNPACKSTATUS'] == '1':
    print('[ERROR] Download of "%s" has failed, exiting' % (os.environ['NZBPP_NZBNAME']))
    sys.exit(POSTPROCESS_NONE)

if debug_enabled:
    print('[INFO] Download directory for file = %s ' % download_dir)
    print('[INFO] 7Zip full path from unpack = %s' % path_7zip)
    print('[INFO] 7Zip full path from iso_extract = %s' % fullpath7zip)
    print('[INFO] Default nzbget download path = %s' % DestDir)

# Exit if not enabled
if not script_enabled:
    print('[INFO] ISO-Extract disabled in settings, exiting...')
    sys.exit(POSTPROCESS_NONE)       

if not os.path.exists(path_7zip):
    if os.path.exists(fullpath7zip):
        if debug_enabled:
            print('[INFO] Using 7ZipFullPath for 7Zip path')
        path_7zip = fullpath7zip
    else:
        print('[ERROR] 7Zip not found!, please correct unpack settings for 7Zip (settings -> unpack -> SevenZipCmd) or set 7ZipFullPath in ISO_Extract settings')
        sys.exit(POSTPROCESS_ERROR)
else:
    if debug_enabled:
        print('[INFO] Using SevenZipCmd for 7Zip path')

# Prep for extract of iso's
os.chdir(download_dir)
import subprocess

# Set 7zip extract to subdirectory if set options
if extracttosubdir:
    SubDirCommand = ' -r -o*'

# Force exctract to subdirectory if workingdirectoty is base download folder
if DestDir == download_dir:
    print('[INFO] Force use subdirectory for extract: directory is base download directory')
    SubDirCommand = ' -o*'

# Make command string
Extractcommand = path_7zip + ' x ' + download_dir + '/*.iso -y' + SubDirCommand

if debug_enabled:
    print('[INFO] Command for extract = ' + Extractcommand)

# try to extract files
result = subprocess.Popen(Extractcommand, shell=True)

# Wait for extract and check for results
if result.wait() != 0:
    print('[ERROR] 7Zip extraction: failed')
    sys.exit(POSTPROCESS_ERROR)
else:
    print('[DETAIL] 7Zip extraction: success')
    if deleteafterextract:
        import glob
        print('[INFO] Deleting ISO file(s)')
        if DestDir != download_dir:
            fileList = glob.glob(download_dir + '/*.iso')
            for filePath in fileList:
                try:
                    os.remove(filePath)
                except:
                    print("[ERROR] failed to delete file: ", filePath)
                    sys.exit(POSTPROCESS_ERROR)
        else:
            print('[WARNING] Did not delete ISO file(s): files are not in a seperate directoy (are in base download directory (see settings -> paths -> Destdir)), this could be dangerous')
    sys.exit(POSTPROCESS_SUCCESS)
