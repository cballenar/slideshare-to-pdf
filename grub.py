#!/usr/bin/env python

import os
import re
import sys
import lxml
import errno
import socket
import shutil
import six
if six.PY2:
    from urllib import urlretrieve as urllib_urlretrieve
else:
    from urllib.request import urlretrieve as urllib_urlretrieve
    raw_input = input
import urllib
import argparse
import requests
import tempfile
import subprocess
from bs4 import BeautifulSoup
import distutils.spawn

# set default output file name and directory
output_file = ''
output_dir = 'downloads/'
output_format = '.pdf'

socket.setdefaulttimeout(20)

# argument parser
parser = argparse.ArgumentParser(description='A python script to help you back up your SlideShare presentations to PDF.')
parser.add_argument('-q', '--quiet', dest='verbose', action='store_false', default=True, help='Don\'t print status messages to stdout.')
parser.add_argument('-i', '--input', help='SlideShare URL to be processed, e.g.: "http://www.slideshare.net/korlayashwanth/download-disabled-slide-share-ppts-by-authors"')
parser.add_argument('-o', '--output', help='Path where to save the file. It can be a folder or especific file. e.g.: "\\Users\\user\\Desktop\\my-slides.pdf" OR "\\Users\\user\\Desktop\\". Default: "./downloads/slide-name.pdf".')
parser.add_argument('-j', '--jpg', action='store_true', default=False, help='Leave intermediate jpg files. Automatically delete and overwrite old files without prompting for confirmation.')
parser.add_argument('--use_convert', action='store_true', default=False, help='Use \'convert\' command to generate pdf')
args = parser.parse_args()

# get input
if args.input:
    url = args.input
else:
    url = raw_input('Input the SlideShare URL you want to convert: ')

# if output was specified, split path into file name and directory
if args.output:
    output_dir, output_file = os.path.split(args.output)

# check output filename
if output_file == '':
    # build output file name from url
    urlMatch = re.search('(?:[^\/]*\/){3}([A-Za-z0-9-_\.]*)(?:\/)([A-Za-z0-9-_\.]*)', url)
    output_file =  '{}-by-{}{}'.format(urlMatch.group(2), urlMatch.group(1), output_format)
else:
    # check if correct format
    if output_file[-4:] != output_format:
        output_file = '{}{}'.format(output_file, output_format)

# check output directory
if output_dir != '':
    try:
        os.makedirs(output_dir)
    except OSError:
        if not os.path.isdir(output_dir):
            raise

# (re)build output path
output_path = os.path.join(output_dir, output_file)

# make tmp directory
dir_tmp = tempfile.mkdtemp()

# grab slideshare html
if args.verbose:
    print('Reading SlideShare page...')

html = ''
images = None
try:
    html = requests.get(url)
    html.raise_for_status()
except Exception as e:
    # terminate script
    sys.exit('Could not download {}. {}'.format(url, e))
else:
    # read html and get images
    soup = BeautifulSoup(html.text, 'lxml')
    images = soup.find_all('img', attrs={'class': 'slide_image'})

# check if full resolution available
if images[0].has_attr('data-full'):
    # use full resolution
    slide_resolution = 'data-full'
elif images[0].has_attr('data-normal'):
    # else use normal
    slide_resolution = 'data-normal'
else:
    # else terminate
    sys.exit('Could not find slides. Terminating...')

# download slides to tmp directory
downloaded_slides = []
for i, image in enumerate(images, start=1):
    # form slides data
    remote_slide = image[slide_resolution]
    local_slide = os.path.join(dir_tmp, 'slide-{}.jpg'.format(str(i)))

    # download slide
    if args.verbose:
        print('Downloading slide {}...'.format(str(i)))

    try:
        urllib_urlretrieve(remote_slide, filename=local_slide)
    except Exception as e:
        # cleanup and terminate
        shutil.rmtree(dir_tmp)
        sys.exit('Could not download slide-{}. {}'.format(str(i), e))
    else:
        # add to array
        downloaded_slides.append(local_slide)

# combine images into pdf
if args.verbose:
    print('Converting to PDF...')

downloaded_slides_str = ' '.join(sorted(downloaded_slides))
try:
    imagick = 'convert'
    if not args.use_convert:
        # detection of magick command
        if distutils.spawn.find_executable('magick'):
            imagick = 'magick'
            print('\'magick\' is to be used. If \'convert\' is correct one, please set --use_convert') if args.verbose else None
    subprocess.call('{} {} -quality 100 {}'.format(imagick, downloaded_slides_str,  output_path), shell=True)
except Exception as e:
    sys.exit('Could not convert slides to PDF. {}'.format(e))

# copy jpg files if requested
if args.jpg:
    dir_jpg = os.path.join(output_dir, os.path.splitext(output_file)[0])
    if os.path.exists(dir_jpg):
        print('Delete old folder {}'.format(dir_jpg)) if args.verbose else None
        shutil.rmtree(dir_jpg)
    try:
        print('Create new folder and copy files to {}'.format(dir_jpg)) if args.verbose else None
        shutil.copytree(dir_tmp, dir_jpg)
    except Exception as e:
        # cleanup and terminate
        shutil.rmtree(dir_tmp)
        sys.exit('Could not copy intermediate jpg files. {}'.format(e))

# remove tmp directory
shutil.rmtree(dir_tmp)

# check if file was created
if os.path.isfile(output_path):
    if args.verbose:
        print('Your file has been successfully created at {}'.format(output_path))

    sys.exit(0)
else:
    sys.exit('Your file could not be created.')
