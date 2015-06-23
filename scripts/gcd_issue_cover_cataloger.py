import os
import sys
import xml.etree.cElementTree as ET


IMAGE_SERVER_ADDRESS = "http://img.comicscantina.com/"


class GCDIssueCoverCataloger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.root = ET.Element("comicscantina_db")
        self.doc = ET.SubElement(self.root, "covers")
        self.tree = ET.ElementTree(self.root)

    def get_filepaths(self, directory):
        file_paths = []  # List which will store all of the full filepaths.
                
        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
        return file_paths  # Self-explanatory.

    def run(self):
        # Run the above function and store its results in a variable.
        full_file_paths = self.get_filepaths(file_path)
        
        for full_file_path in full_file_paths:
            for file_ext in ['.png', '.jpeg',  '.jpg',  '.bmp',  '.tiff',  '.jfif','.gif']:
                if full_file_path.endswith(file_ext):
                    self.process(full_file_path)

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
    
    def process(self, file_path):
        # Process the filename to be used for extracting information
        directories = file_path.split("/")
        filename_with_ext = directories[-1]
        filename = filename_with_ext.split(".")
        filename = filename[0]
        id_array = filename.split("_")
        
        # Extract ID information
        issue_id = id_array[0]
        image_type = id_array[1]
        zoom = id_array[2]
        url = IMAGE_SERVER_ADDRESS + filename_with_ext
        
        # Create our Issue
        ET.SubElement(self.doc, "issue", id=issue_id, type=image_type, zoom=zoom, url=url)

        # Save it.
        self.tree.write("cover/issue_catalog.xml")
        print("GCDIssueCoverCataloger: Saved: " + issue_id)

# Example of running this script:
# $ python gcd_issue_cover_cataloger.py /Users/bartlomiejmika/Developer/comicscantina/py-comicscantina/scripts/cover
if __name__ == "__main__":
    os.system('clear;')  # Clear the console text.
    
    # Get the total number of args passed to the demo.py
    total = len(sys.argv)
    if total != 2:
        print("Error: needs to have url passed in of the location issue.xml")
    else:
        file_path = str(sys.argv[1])
        cataloger = GCDIssueCoverCataloger(file_path)
        cataloger.run()
