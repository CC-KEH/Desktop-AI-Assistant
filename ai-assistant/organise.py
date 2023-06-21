import os

class organiser:
    def organise_files(folder):
        os.listdir(folder)

    def makePath(path):
        st = ""
        for element in path:
            st+=element+'/'
        return st


    def organise(path):
        dir_list = os.listdir(path)
        organise_manner = ['last opened','category']
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        categories = ['audios','documents','programs','applications','images','videos']

        for file in dir_list:
            if('.exe' in file):
                #Add to applications if category is selected
                #OR
                #Add to the month it was last opened.
                pass
            elif('.pdf' or '.docx' or '.xlsx' or '.csv' or '.zip' or 'xls' or '.doc' in file):
                #Add to documents if catergory is selected
                #OR
                #Add to the month it was last opened.
                pass
            elif('.mp4' or '.flv' or'.wmv' in file):
                #Add to videos if catergory is selected
                #OR
                #Add to the month it was last opened.
                pass
            elif('.aac' or '.adt' or '.adts' or '.mp3' or '.aif' or '.aifc' or '.aiff' or '.avi' or '.m4a' or '.wav' or '.wma' in file):
                #Add to audios if catergory is selected
                #OR
                #Add to the month it was last opened.
                pass
            elif('.iso' in file):
                #Add to images if catergory is selected
                #OR
                #Add to the month it was last opened.
                pass
            else:
                #Add to Others if catergory is selected
                #OR
                #Add to the month it was last opened.
                pass

            
        
        