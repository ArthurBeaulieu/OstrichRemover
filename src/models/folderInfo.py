# Python imports
import os


# The target folder info class
class FolderInfo(object):
    def __init__(self, folderPath):
        self.folder = ''
        self.folderSize = 0
        self.filesCounter = 0
        self.foldersCounter = 0
        self.artistsCounter = 0
        self.albumsCounter = 0
        self.tracksCounter = 0
        self.coversCounter = 0
        self.flacCounter = 0
        self.flacPercentage = 0
        self.mp3Counter = 0
        self.mp3Percentage = 0
        self.pngCounter = 0
        self.pngPercentage = 0
        self.jpgCounter = 0
        self.jpgPercentage = 0
        self._computeFolderInfo(folderPath)

    # Reads the user given folder and store a few informations about it
    def _computeFolderInfo(self, folder):
        self.folder = folder
        rootPathLength = len(folder.split(os.sep))
        # Counting file, folder etc, and computed folder info internals
        for folder, dirnames, filenames in sorted(os.walk(folder)):
            filenames = [f for f in filenames if not f[0] == '.']  # Ignore hidden files
            dirnames[:] = [d for d in dirnames if not d[0] == '.']  # ignore hidden directories
            self.filesCounter += len(filenames)  # Increment file counter
            self.foldersCounter += len(dirnames)  # Increment folder counter
            path = folder.split(os.sep)  # Split root into an array of folders
            # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
            for x in range(rootPathLength - 1):
                path.pop(0)
            # Fill artists and albums counter
            if len(path) == 1 and path[0] != '':
                self.artistsCounter += 1
            elif len(path) == 2:
                self.albumsCounter += 1
            # Analyse files in current folder
            for f in filenames:
                if f[-4:] == '.mp3' or f[-4:] == '.MP3':
                    self.mp3Counter += 1
                elif f[-5:] == '.flac' or f[-5:] == '.FLAC':
                    self.flacCounter += 1
                elif f[-4:] == '.jpg' or f[-4:] == '.JPG':
                    self.jpgCounter += 1
                elif f[-4:] == '.png' or f[-4:] == '.PNG':
                    self.pngCounter += 1
                fp = os.path.join(folder, f)
                self.folderSize += os.path.getsize(fp)  # Increment folder size
        # Compute totals
        self.tracksCounter = self.flacCounter + self.mp3Counter
        self.coversCounter = self.jpgCounter + self.pngCounter
        # Compute files percentages
        if self.tracksCounter > 0:
            self.flacPercentage = round((self.flacCounter / self.tracksCounter * 100), 2)
            self.mp3Percentage = round((self.mp3Counter / self.tracksCounter * 100), 2)
        if self.coversCounter > 0:
            self.pngPercentage = round((self.pngCounter / self.coversCounter * 100), 2)
            self.jpgPercentage = round((self.jpgCounter / self.coversCounter * 100), 2)
