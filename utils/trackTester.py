from utils.errorEnum import ErrorEnum
from utils.tools import prefixDot, prefixThreeDots, suffixDot, suffixThreeDots, removeSpecialCharFromArray


class TrackTester:
    def __init__(self, track, album):
        self.track = track
        self.album = album
        self.errors = []
        self.errorCounter = 0
        self.missingTags = []
        self.missingTagsCounter = 0
        self.missorderedTag = []
        self.missorderedTagsCounter = 0
        self._testTrackObject()


    # Tests a Track object to check if it is matching the naming convention
    def _testTrackObject(self):
        global orphanCounter
        if len(self.track.fileNameList) < 6: # TypeError : Invalid file name (doesn't comply with the naming convention)
            # TODO handle incorrect list length in ErrorEnum
            #orphanCounter += 1
            #if orphans == True and debug == True:
            #    print('| KO - Filename -> The file \'{}\' isn\'t named following the naming convention. Use MzkOstrichRemover.py --help for informations'.format(track.fileName))
            return
        # Category 1 : Filesystem naming inconsistencies
        self._testFileSystemNaming()
        # Category 2 : Filesystem naming vs ID3 tags inconsistencies
        self._testFileSystemNamingAgainstTags()
        # Category 3 : ID3 tags inconsistencies
        self._testTagsInconsistencies()
        # Category 4 : Track tags coherence with album metrics
        self._testAlbumValuesCoherence()


    # Testing Category 1 : Filesystem naming inconsistencies (see ErrorEnum.py)
    def _testFileSystemNaming(self):
        # ErrorCode 00 : Filename release artists doesn't match the artist foldername
        self._testErrorForErrorCode(ErrorEnum.FILENAME_RELEASE_ARTIST_VS_ARTIST_FOLDERNAME, self.track.fileNameList[0], self.track.pathList[len(self.track.pathList) - 2])
        # ErrorCode 01 : Filename year doesn't match the album foldername year
        self._testErrorForErrorCode(ErrorEnum.FILENAME_YEAR_VS_ALBUM_FOLDERNAME_YEAR, self.track.fileNameList[1], self.track.folderNameList[0])
        # ErrorCode 02 : Filename album doesn't match the album foldername
        self._testErrorForErrorCode(ErrorEnum.FILENAME_ALBUM_VS_ALBUM_FOLDERNAME, self.track.fileNameList[2], self.track.folderNameList[1])


    # Testing Category 2 : Filesystem naming vs ID3 tags inconsistencies (see ErrorEnum.py)
    def _testFileSystemNamingAgainstTags(self):
        # ErrorCode 03 : Filename year doesn't math the track year tag
        self._testErrorForErrorCode(ErrorEnum.FILENAME_YEAR_VS_YEAR_TAG, self.track.fileNameList[1], self.track.year)
        # ErrorCode 04 : Foldername year doesn't math the track year tag
        self._testErrorForErrorCode(ErrorEnum.FOLDERNAME_YEAR_VS_YEAR_TAG, self.track.folderNameList[0], self.track.year)
        # ErrorCode 05 : Filename album doesn't match the track album
        self._testErrorForErrorCode(ErrorEnum.FILENAME_ALBUM_VS_ALBUM_TAG, self.track.fileNameList[2], self.track.albumTitle)
        # ErrorCode 06 : Foldername album doesn't match the track album
        self._testErrorForErrorCode(ErrorEnum.FOLDERNAME_ALBUM_VS_ALBUM_TAG, self.track.folderNameList[1], self.track.albumTitle)
        # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
        discTrackConcat = '{}{:02d}'.format(self.track.discNumber, int(self.track.trackNumber))
        self._testErrorForErrorCode(ErrorEnum.FILENAME_DISC_TRACK_NO_VS_DISC_TRACK_NO_TAG, self.track.fileNameList[3], discTrackConcat)
        # ErrorCode 08 : Filename artists doesn't match the track artist tag
        # ErrorCode 09 : Title remix artist doesn't match the filename artist
        self._testFilenameTrackArtist()
        # ErrorCode 10 : Filename title doesn't match the track title tag
        self._testErrorForErrorCode(ErrorEnum.FILENAME_TITLE_VS_TITLE_TAG, self.track.fileNameList[5].rsplit('.', 1)[0], self.track.title)


    # Testing Category 3 : ID3 tags inconsistencies
    def _testTagsInconsistencies(self):
        # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
        self._testForMissingtags()
        # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
        self._testPerformerComposition()
        # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
        self._testMissorderedTags()


    # Testing Category 4 : Track tags coherence with album metrics
    def _testAlbumValuesCoherence(self):
        # ErrorCode 14 : Computed album total track is not equal to the track total track tag
        if self.track.trackTotal == '' or int(self.track.trackTotal) != self.album.trackTotal:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.ALBUM_TOTAL_TRACK_VS_TRACK_TOTAL_TRACK)
        # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
        if self.track.discTotal == '' or int(self.track.discTotal) != self.album.discTotal:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.ALBUM_DISC_TRACK_VS_TRACK_DISC_TRACK)
        # ErrorCode 16 : Computed album yeas is not equal to the track year tag
        if self.track.year == '' or self.track.year != self.album.year:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.ALBUM_YEAR_VS_TRACK_YEAR)


    def _testFilenameTrackArtist(self):
        if len(self.track.remix) == 0:
            # ErrorCode 08 : Filename artists doesn't match the track artist tag
            self._testArrayErrorForErrorCode(ErrorEnum.FILENAME_ARTIST_VS_ARTIST_TAG, self.track.fileNameList[4].split(', '), self.track.artists)
        else:
            # ErrorCode 09 : Title remix artist doesn't match the filename artist
            self._testErrorForErrorCode(ErrorEnum.FILENAME_ARTIST_VS_REMIX_ARTIST, self.track.fileNameList[4], self.track.remix)


    def _testForMissingtags(self):
        if self.track.title == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Title')
        if len(self.track.artists) == 1 and self.track.artists[0] == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Artists')
        if self.track.albumTitle == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Album')
        if self.track.year == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Year')
        if len(self.track.performers) == 1 and self.track.performers[0] == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Performers')
        if self.track.composers == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Composers')
        if self.track.producer == '':
            self.missingTagsCounter += 1
            self.missingTags.append('Producer')
        if self.track.trackNumber == '':
            self.missingTagsCounter += 1
            self.missingTags.append('TrackNumber')
        if self.track.trackTotal == '':
            self.missingTagsCounter += 1
            self.missingTags.append('TrackTotal')
        if self.track.discNumber == '':
            self.missingTagsCounter += 1
            self.missingTags.append('DiscNumber')
        if self.track.discTotal == '':
            self.missingTagsCounter += 1
            self.missingTags.append('DiscTotal')
        if self.missingTagsCounter > 0:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.MISSING_TAGS)


    def _testPerformerComposition(self):
        # If track has featured artists, we append them to the performer tmp string
        # Sorted comparaison to only test value equality. The artists alphabetic order is tested elswhere
        if len(self.track.performers) != len(self.track.composedPerformer) or sorted(self.track.performers) != sorted(self.track.composedPerformer):
            self.errorCounter += 1
            self.errors.append(ErrorEnum.INCONSISTENT_PERFORMER)


    def _testMissorderedTags(self):
        if sorted(removeSpecialCharFromArray(self.track.artists)) != removeSpecialCharFromArray(self.track.artists):
            self.missorderedTag.append('Artists')
            self.missorderedTagsCounter += 1
        if sorted(removeSpecialCharFromArray(self.track.artists)) != removeSpecialCharFromArray(self.track.fileNameList[4].split(', ')):
            self.missorderedTag.append('Artists')
            self.missorderedTagsCounter += 1
        if sorted(removeSpecialCharFromArray(self.track.performers)) != removeSpecialCharFromArray(self.track.performers):
            self.missorderedTag.append('Performers')
            self.missorderedTagsCounter += 1
        if sorted(removeSpecialCharFromArray(self.track.feat)) != removeSpecialCharFromArray(self.track.feat):
            self.missorderedTag.append('Featuring')
            self.missorderedTagsCounter += 1
        if sorted(removeSpecialCharFromArray(self.track.remix)) != removeSpecialCharFromArray(self.track.remix):
            self.missorderedTag.append('Remixer')
            self.missorderedTagsCounter += 1
        if self.missorderedTagsCounter > 0:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.MISSORDERED_TAGS)


    # Tests a Track on a given topic using an error code as documented in this function
    def _testErrorForErrorCode(self, errorCode, string1, string2):
        if string1 != string2:
            if self._areStringsMatchingWithFoldernameRestrictions(string1, string2) == False:
                self.errorCounter += 1
                self.errors.append(errorCode)


    # Tests a Track on a given topic using an error code as documented in this function
    def _testArrayErrorForErrorCode(self, errorCode, array1, array2):
        if len(array1) != len(array2):
            self.errorCounter += 1
            self.errors.append(errorCode)
            return

        for item1, item2 in zip(array1, array2):
            if item1 != item2:
                if self._areStringsMatchingWithFoldernameRestrictions(item1, item2) == False:
                    self.errorCounter += 1
                    self.errors.append(errorCode)
                    return


    # Test if the character that do not match in string are forbidden on some OS. string1 is from the filename, string2 is from the tags
    def _areStringsMatchingWithFoldernameRestrictions(self, string1, string2):
        list1 = list(string1)
        list2 = list(string2)
        if len(list1) != len(list2):
            if prefixDot(list1) == True or prefixThreeDots(list1) == True or suffixDot(list1) == True or suffixThreeDots(list1) == True:
                return True
            if prefixDot(list2) == True or prefixThreeDots(list2) == True or suffixDot(list2) == True or suffixThreeDots(list2) == True:
                return True
            else:
                return False
        else:
          # Checking first that the differents char are bc of an illegal symbol
          forbiddenChars = ['*', '/', '\\', ':', ';', '?', '<', '>', '\"', '|']
          for x in range(0, len(list1)):
              if list1[x] != list2[x]:
                  if list1[x] == '-': # Forbidden char must have been replaced with a -, return False otherwise (char are differents for no valuable reasons)
                      if list2[x] not in forbiddenChars:
                          return False
                  else:
                      return False
          return True
