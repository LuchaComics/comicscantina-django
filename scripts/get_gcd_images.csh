#!/bin/csh
#------------------------------------------------------------------------------#
# get_gcd_images.csh                                                           #
#------------------------------------------------------------------------------#
# By: Bartlomiej Mika
# Date: May, 4th, 2015
#

# Clear all text on the screen
clear;

# Turn on virtual environment
cd /home/comicsc/web/http://img.comicscantina.com
source /home/comicsc/web/http://img.comicscantina.com/env/bin/activate

# Run command
cd /home/comicsc/web/http://img.comicscantina.com/etl
python gcd_issue_cover_downloader.py /home/comicsc/web/img.comicscantina.com/etl/xml

# Turn off virtual environment
deactivate
