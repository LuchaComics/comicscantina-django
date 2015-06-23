import os
import sys
import xml.sax
import urllib3
from time import sleep
from bs4 import BeautifulSoup
import shutil


LARGE_ZOOM = '4'
MEDIUM_ZOOM = '2'
SMALL_ZOOM = '1'
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2
START_IMPORT_ARTIFICAL_DELAY = 2  # 2 Second delay
DOWNLOAD_IMAGE_ARTIFICAL_DELAY = 1


class GCDIssueCoverDownloader(xml.sax.ContentHandler):
    def __init__(self, start_issue_id):
        xml.sax.ContentHandler.__init__(self)
        self.start_issue_id = start_issue_id
        self.is_id_found = False

    def startElement(self, name, attrs):
        # Detect our issue_id
        if name == 'id':
            self.is_id_found = True

    def endElement(self, name):
        self.is_id_found = False

    def characters(self, content):
        if self.is_id_found:
            if int(content) >= self.start_issue_id:
                self.download_row(content)
            else:
                print("Skipping: " + content)

    def detect_imagetype(self, url):
        if 'png' in url.lower():
            return 'png'
        if 'jpeg' in url.lower():
            return 'jpeg'
        if 'jpg' in url.lower():
            return 'jpg'
        if 'bmp' in url.lower():
            return 'bmp'
        if 'tiff' in url.lower():
            return 'tiff'
        if 'jfif' in url.lower():
            return 'jfif'
        if 'gif' in url.lower():
            return 'gif'
        return 'unknown'
    
    def download_row(self, issue_id):
        # In order to prevent GCD for banning us for hammering their
        # system with our requests, we must add an artifical delay to
        # not raise any red flags.
        sleep(START_IMPORT_ARTIFICAL_DELAY)
        
        #-----------#
        #  Extract  #
        #-----------#
        # Handle making URL calls.
        http = urllib3.PoolManager()
        
        # GCD stores a copy of each image in three zoom levels. 4 is largest, 2
        # is medium and 1 is small.
        zoom_levels = [SMALL_ZOOM, MEDIUM_ZOOM , LARGE_ZOOM]
        
        for zoom in zoom_levels:
            r = http.request('GET', 'http://www.comics.org/issue/'+str(issue_id)+'/cover/'+zoom+'/')
            
            # Only process if a successful result was returned.
            if r.status == 200:
                # Scrap all the image files found on this page.
                soup = BeautifulSoup(r.data)
                images = soup.find_all('img',{'class':'cover_img'})
                
                # Variable controls whether image is primary or alternative.
                # Where 1 = Primary, 2 = Alternative
                file_index = PRIMARY_IMAGE
                
                # Iterate through all the scrapped image elements and save them locally.
                for image in images:
                    url = (image.get("src"))
                    print("Importing: " + url)
                    
                    file_type = self.detect_imagetype(url)
                    file_name = str(issue_id) + '_' + str(file_index) + '_' + zoom
                    file_path = os.path.dirname(os.path.realpath(__file__)) + '/cover/'  + file_name + '.' + file_type
                    
                    #-----------#
                    # Transform #
                    #-----------#
                    # Save the image locally.
                    with http.request('GET', url, preload_content=False) as r, open(file_path, 'wb') as out_file:
                        shutil.copyfileobj(r, out_file)
                    
                    #--------#
                    #  Load  #
                    #--------#
                    # Indicate we are now processing the alternative image
                    # on the next loop.
                    file_index = ALTERNATIVE_IMAGE
            
                    # Add an artifical delay in between downloads to prevent
                    # setting off any red-flags from GCD.
                    sleep(DOWNLOAD_IMAGE_ARTIFICAL_DELAY)


# Example of running this script:
# $ python gcd_issue_cover_downloader.py /Users/bartlomiejmika/Developer/comicscantina/gcd/xml/gcd_issue.xml 0
if __name__ == "__main__":
    os.system('clear;')  # Clear the console text.
    
    # Check to see if the 'cover' directory has been created, if not
    # then lets create it in the current directoty that this script is
    # running in.
    directory = os.path.dirname(os.path.realpath(__file__)) + '/cover'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the total number of args passed to the demo.py
    total = len(sys.argv)
    if total != 3:
        print("Error: needs to have url passed in of the location issue.xml and the start issue_id")
    else:
        file_path = str(sys.argv[1])
        start_issue_id = int(sys.argv[2])
        source = open(file_path)
        xml.sax.parse(source, GCDIssueCoverDownloader(start_issue_id))
