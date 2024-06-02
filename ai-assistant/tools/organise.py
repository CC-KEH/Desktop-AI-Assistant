import os
from tools.utils import *
import shutil
import datetime
from saved_data.constants import *

class Organiser:
    def __init__(self,path):
        self.paths = organise_directories
        
    def categorize(self,parent_path):
        directories = {
        "images": ["jpg", "jpeg", "png", "gif", 'tiff', 'ai', 'indd', 'raw'],
        "videos": ["mp4", "mkv", "avi", 'flv', 'wmv'],
        "documents": ["pdf", "docx", "xlsx", "pptx", 'csv', 'xls', 'doc'],
        "music": ["mp3", "wav", "aac", 'adt', 'adts', 'aif', 'aifc', 'aiff', 'avi', 'm4a', 'wma'],
        "archives": ["zip", "rar"],
        "applications": ['exe'],
        "others": []
        }

        for directory in directories:
            directory_path = os.path.join(parent_path, directory)
            os.makedirs(directory_path, exist_ok=True)

        # Organize the files
        for file_name in os.listdir(parent_path):
            file_path = os.path.join(parent_path, file_name)

            if os.path.isfile(file_path):
                file_extension = file_name.split(".")[-1].lower()

                # Find the appropriate directory for the file type
                found = False
                for directory, extensions in directories.items():
                    if file_extension in extensions:
                        destination = os.path.join(parent_path, directory)
                        shutil.move(file_path, destination)
                        found = True
                        break

                # If the file type is not found, move it to the 'others' directory
                if not found:
                    destination = os.path.join(parent_path, "others")
                    shutil.move(file_path, destination)

        file = open(organised_path, "w")
        file.write(str(datetime.datetime.now()) + "\n")
        file.close()
        
        print("Directory organization completed.")

    def organise(self):
        for directory,path in self.paths.items():
            self.categorize(path)