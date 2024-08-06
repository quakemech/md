#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 
# ******************************************************************************
#
# @file			cardify.py
#
# @brief        Markdown processing tool 
#
# @copyright    Copyright (C) 2024 Barrett Edwards. All rights reserved.
#
# @date         Aug 2024
# @author       Barrett Edwards <thequakemech@gmail.com>
# 
# ******************************************************************************

import os
import subprocess
import argparse
import time
import datetime

# Parse arguments
parser = argparse.ArgumentParser(description='Markdown Processor')

parser.add_argument('filename',             nargs='?',                              help='Filename', default='?')

#input formats
parser.add_argument('-i','--stdin',         required=False, action='store_true',    help='Use STDIN for input')

#output formats
parser.add_argument('-m','--mobi',          required=False, action='store_true',    help='Build doc into mobi format for kindle')
parser.add_argument('-e','--epub',          required=False, action='store_true',    help='Build doc into epub format')
parser.add_argument('-t','--tex',           required=False, action='store_true',    help='Build doc into Latex format')
parser.add_argument('-p','--pdf',           required=False, action='store_true',    help='Build doc into PDF format')

#pandoc options
parser.add_argument('-N','--section-numbers',           required=False, action='store_true',    help='Number Sections')
parser.add_argument('-P','--template',                  required=False, action='store',         help='Tex/epub Template file')
parser.add_argument('-T','--toc-level',                 required=False, action='store',         help='Table of Contents Level')
parser.add_argument('-Z','--margins',                   required=False, action='store',         help='Set margin width in inches')
parser.add_argument('-I','--cover-image',               required=False, action='store',         help='Cover Image File for epub/mobi formats')
parser.add_argument('-r','--resource-path',             required=False, action='store',         help='Resource path')
parser.add_argument('-S','--section-newpage',           required=False, action='store_true',    help='Insert new page before sections')
parser.add_argument('-X','--title-newpage',             required=False, action='store_true',    help='Insert new page after title page')
parser.add_argument('-Y','--body-newpage',              required=False, action='store_true',    help='Insert new page before body')
parser.add_argument('-F','--fancy',                     required=False, action='store_true',    help='Fancy headers and footers')
parser.add_argument('-Q','--figures-tables',            required=False, action='store_true',    help='Create list of figures and tables')
parser.add_argument('-D','--datestamp-today',           required=False, action='store_true',    help="Use Today's date for datestamp")
parser.add_argument('-v','--verbose',                   required=False, action='store_true',    help="Verbose output")

# operational actions
parser.add_argument('-c','--clean',         required=False, action='store_true',    help='Clean up build files')
parser.add_argument('-C','--clean-light',   required=False, action='store_true',    help='Clean up build files but leave output files')
parser.add_argument('-o','--open',          required=False, action='store_true',    help='Open up output file when completed')

options = vars(parser.parse_args())

filename   = options['filename']


# if filename isn't specified find first txt file in directory and try to compile that
if filename == '?':
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            filename = file


# if filename still is no defiend then exit
if filename == '?':
    print("Error: No txt file found. Quitting.")
    quit()


# Get build options
build_mobi = options['mobi']
build_epub = options['epub']
build_tex  = options['tex']
build_pdf  = options['pdf']


# if no build option was specified no clean options then set to build to PDF
if not build_mobi and not build_epub and not build_tex and not build_pdf and not options['clean'] and not options['clean_light']:
    build_pdf = True

# if we are building a mobi format then we have to build the epub version first
if build_mobi:
    build_epub = True



def build_pandoc_cmd():
    
    # Assemble cmd to send to subprocess
    cmd = ['pandoc']
    cmd.append('-s')
    cmd.append('--quiet')
    
    # number sections
    if options['section_numbers']:
        cmd.append('-N')

    # handle template file
    cmd.append('--template')
    if options['template']:
        cmd.append(options['template'])
    else:
        cmd.append(os.path.expanduser('~/bin/mdtemplate.tex'))

    if options['toc_level']:
        cmd.append('--toc')
        cmd.append('--toc-depth')
        cmd.append(options['toc_level'])

    # set margins
    if options['margins']:
        cmd.append('-V')
        cmd.append('geometry:margin=' + options['margins'] + 'in')
    else:
        cmd.append('-V')
        cmd.append('geometry:margin=0.7in')

    if options['resource_path']:
        cmd.append('--resource-path')
        cmd.append(os.path.expanduser(options['resource_path']))
    else: 
        cmd.append('--resource-path')
        cmd.append(os.path.expanduser('~/'))

    if options['section_newpage']:
        cmd.append('-V')
        cmd.append('newpagebeforesection=True')

    if options['title_newpage']:
        cmd.append('-V')
        cmd.append('newpageaftertitlepage=True')

    if options['body_newpage']:
        cmd.append('-V')
        cmd.append('newpagebeforebody=True')

    if options['figures_tables']:
        cmd.append('-V')
        cmd.append('lot=True')
        cmd.append('-V')
        cmd.append('lof=True')

    if options['fancy']:
        cmd.append('-V')
        cmd.append('fancyheaderfooter=True')

    if options['datestamp_today']:
        cmd.append('-V')
        cmd.append('date='+datetime.datetime.now().strftime("%Y-%m-%d"))

    return cmd



if build_tex:
    if options['verbose']:
        print("Building tex")
    
    cmd = build_pandoc_cmd()
    
    # splitout extention from filename in to ['filename', '.txt']
    filename_parts = os.path.splitext(filename)

    # add outfile
    cmd.append('-o')
    cmd.append(filename_parts[0] + '.tex')
    
    # add source file
    cmd.append(filename)

    if options['verbose']:
        print(cmd)
    try:
        rv = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print("pandoc build failed: " + filename + " Return Code: "+str(e.returncode)+" Error Message: "+str(e.output))


if build_pdf:
    if options['verbose']:
        print("Building pdf")
    
    cmd = build_pandoc_cmd()
    
    # splitout extention from filename in to ['filename', '.txt']
    filename_parts = os.path.splitext(filename)
    
    # add outfile
    cmd.append('-o')
    cmd.append(filename_parts[0] + '.pdf')
    cmd.append(filename)

    if options['verbose']:
        print(cmd)
    try:
        rv = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print("pandoc build failed: " + filename + " Return Code: "+str(e.returncode)+" Error Message: "+str(e.output))


if build_epub:
    if options['verbose']:
        print("Building epub")

    # splitout extention from filename in to ['filename', '.txt']
    filename_parts = os.path.splitext(filename)

    # Assemble cmd to send to subprocess
    cmd = ['pandoc']
    cmd.append('-s')

    # handle image file
    if options['cover_image']:
        cmd.append('--epub-cover-image=' + options['cover_image'])

    # handle template file
    if options['template']:
        cmd.append('--epub-stylesheet=' + options['template'])
    else:
        cmd.append('--epub-stylesheet=' + os.path.expanduser('~/bin/mdtemplate.css'))

    #set Table of Contents level
    if options['toc_level']:
        cmd.append('--toc')
        cmd.append('--toc-depth')
        cmd.append(options['toc_level'])

    # Set epub version
    cmd.append('-t')
    cmd.append('epub3')

    # add outfile
    cmd.append('-o')
    cmd.append(filename_parts[0] + '.epub')
    cmd.append(filename)

    if options['verbose']:
        print(cmd)
    try:
        rv = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print("pandoc build failed: " + filename + " Return Code: "+str(e.returncode)+" Error Message: "+str(e.output))



if build_mobi:
    if options['verbose']:
        print("Building mobi")

    # splitout extention from filename in to ['filename', '.txt']
    filename_parts = os.path.splitext(filename)

    # Assemble cmd to send to subprocess
    cmd = ['kindlegen']
    cmd.append(filename_parts[0] + '.epub')

    if options['verbose']:
        print(cmd)
    try:
        rv = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print("kindlegen build failed: " + filename_parts[0] + '.epub' + " Return Code: "+str(e.returncode)+" Error Message: "+str(e.output))




if options['open']:
    if options['verbose']:
        print("Opening")
    # splitout extention from filename in to ['filename', '.txt']
    filename_parts = os.path.splitext(filename)

    extension = filename_parts[1]

    if build_epub:
        extension = '.epub'
    if build_tex:
        extension = '.tex'
    if build_pdf:
        extension = '.pdf'

    cmd = ['open', filename_parts[0] + extension]

    try:
        rv = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print("Open failed: " + filename + " Return Code: "+str(e.returncode)+" Error Message: "+str(e.output))
    time.sleep(2) # add sleep delay so the PDF has a time to open before it is deleted if the user is also running a clean


if options['clean']:
    dirpath = os.path.dirname(filename)
    
    if dirpath == '':
        dirpath = os.getcwd()
    
    for file in os.listdir(dirpath):
        if file.endswith((".tex", ".toc", ".log", ".aux", ".out", "synctex.gz", ".lot", ".lof", ".epub", ".mobi", ".pdf", )):
            os.remove(os.path.join(dirpath, file))


if options['clean_light']:
    dirpath = os.path.dirname(filename)
    
    if dirpath == '':
        dirpath = os.getcwd()
    
    for file in os.listdir(dirpath):
        if file.endswith((".tex", ".toc", ".log", ".aux", ".out", "synctex.gz", ".lot", ".lof")):
            os.remove(os.path.join(dirpath, file))

