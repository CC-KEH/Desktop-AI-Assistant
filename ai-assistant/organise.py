import os
from utils import *
import shutil
import datetime
class Organiser:
    def organise_files(self,folder):
        os.listdir(folder)

    def makePath(path):
        st = ""
        for element in path:
            st+=element+'/'
        return st
    
    def get_last_modified(self,file_path):
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            last_modified = datetime.datetime.fromtimestamp(timestamp)
            month = last_modified.strftime("%B").lower()  # Get the month as a string
            return month
        else:
            return None

    def lastUpdated(self,parent_path):
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']        
        for directory in months:
            directory_path = os.path.join(parent_path,directory)
            os.makedirs(directory_path,exist_ok=True)
        
        for file_name in os.listdir(parent_path):
            file_path = os.path.join(parent_path,file_name)
            last_month = self.get_last_modified(file_path)

            if(last_month in months):
                destination = os.path.join(parent_path,last_month)
                shutil.move(file_path,destination)
                break
    
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

        file = open("organised.txt", "w")
        file.write(str(datetime.datetime.now()) + "\n")
        file.close()
        
        print("Directory organization completed.")

    def organise(self,path,query):
        
        # cdrive\\programs\\documents by converting to string
        
        final_path = self.makePath(path)     
        utils = Utils()
        utils.say('Categories or Last updated?')
        mode = utils.take_command().lower()
        if query==None:
            self.categorize(final_path)
        else:
            if('category' or 'categories' in mode):
                self.categorize(final_path)
            elif('last' or 'opened' in mode):
                self.lastUpdated(final_path)
                
            
        
        