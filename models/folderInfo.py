import os


# The target folder info class
class FolderInfo:
    def __init__(self, folderPath):
        self.folder = ''
        self.filesCounter = ''
        self.foldersCounter = ''
        self.folderSize = ''
        self.flacCounter = ''
        self.flacPercentage = ''
        self.mp3Counter = ''
        self.mp3Percentage = ''
        self.pngCounter = ''
        self.pngPercentage = ''
        self.jpgCounter = ''
        self.jpgPercentage = ''
        self._computeFolderInfo(folderPath)


    # Reads the user given folder and store a few informations about it
    def _computeFolderInfo(self, folder):
        # Counting file, folder in the given path and computed bytes size
        localRoot = folder
        filesCounter = foldersCounter = folderSize = 0
        mp3Counter = flacCounter = jpgCounter = pngCounter = 0
        for localRoot, dirnames, filenames in os.walk(folder):
            filesCounter += len(filenames) # Increment file counter
            foldersCounter += len(dirnames) # Increment folder counter
            for f in filenames:
                if f[-4:] == '.mp3' or f[-4:] == '.MP3':
                    mp3Counter += 1
                elif f[-5:] == '.flac' or f[-5:] == '.FLAC':
                    flacCounter += 1
                elif f[-4:] == '.jpg' or f[-4:] == '.JPG':
                    jpgCounter += 1
                elif f[-4:] == '.png' or f[-4:] == '.PNG':
                    pngCounter += 1
                fp = os.path.join(localRoot, f)
                folderSize += os.path.getsize(fp) # Increment folder size
        # Compute files percentages
        flacPercentage = mp3Percentage = jpgPercentage = pngPercentage = 0
        if (flacCounter + mp3Counter) > 0:
            flacPercentage = round((flacCounter / (flacCounter + mp3Counter) * 100), 2)
            mp3Percentage = round((mp3Counter / (flacCounter + mp3Counter) * 100), 2)
        if (jpgCounter + pngCounter) > 0:
            pngPercentage = round((pngCounter / (jpgCounter + pngCounter) * 100), 2)
            jpgPercentage = round((jpgCounter / (jpgCounter + pngCounter) * 100), 2)
        # Fill self with those computed variables
        self.folder = folder
        self.filesCounter = filesCounter
        self.foldersCounter = foldersCounter
        self.folderSize = folderSize
        self.flacCounter = flacCounter
        self.flacPercentage = flacPercentage
        self.mp3Counter = mp3Counter
        self.mp3Percentage = mp3Percentage
        self.pngCounter = pngCounter
        self.pngPercentage = pngPercentage
        self.jpgCounter = jpgCounter
        self.jpgPercentage = jpgPercentage
