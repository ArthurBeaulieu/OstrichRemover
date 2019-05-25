# Python imports
import datetime
import json

# Project imports
from utils.errorEnum import ErrorEnum
from utils.tools import createDirectory


# Generate an JSON file from the albumTesters array
def computeReport(version, folderInfo, albumTesters, errorCounter, purity):
    # Creating output dict object
    now = datetime.datetime.now()
    output = {}
    output['date'] = '{}-{}-{}'.format(now.year, now.month, now.day)
    output['version'] = version
    output['folderInfo'] = _computeFolderInfo(folderInfo, errorCounter, purity)
    output['artists'] = []
    currentArtistName = ''
    currentArtist = {}
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        album = {}
        if currentArtistName != albumPathList[len(albumPathList) - 2]: # Current Artist has changed
            if currentArtist != {}: # Avoid to add the first empty artist when loop starts
                output['artists'].append(currentArtist)
                currentArtist = {}
            currentArtistName = albumPathList[len(albumPathList) - 2]
            currentArtist['name'] = currentArtistName
            currentArtist['albums'] = []
        album['title'] = albumPathList[len(albumPathList) - 1]
        album['errors'] = []
        album['tracks'] = []
        for error in albumTester.errors:
            album['errors'].append(_computeErrors(error.value))
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                track = {}
                track['title'] = trackTester.track.fileName
                track['errors'] = []
                for error in trackTester.errors:
                    track['errors'].append(_computeErrors(error.value))
                album['tracks'].append(track)
        currentArtist['albums'].append(album)
    output['artists'].append(currentArtist)
    return output


# Convert the folderInfo object into a returned dict
def _computeFolderInfo(folderInfo, errorCounter, purity):
    output = {}
    output['name'] = folderInfo.folder
    output['files'] = folderInfo.filesCounter
    output['folders'] = folderInfo.foldersCounter
    output['size'] = folderInfo.folderSize
    output['folders'] = folderInfo.foldersCounter
    output['flacCount'] = folderInfo.flacCounter
    output['mp3Count'] = folderInfo.mp3Counter
    output['flacPercentage'] = folderInfo.flacPercentage
    output['mp3Percentage'] = folderInfo.mp3Percentage
    output['jpgPercentage'] = folderInfo.jpgPercentage
    output['pngPercentage'] = folderInfo.pngPercentage
    output['jpgCount'] = folderInfo.jpgCounter
    output['pngCount'] = folderInfo.pngCounter
    output['artistsCount'] = folderInfo.artistsCounter
    output['albumsCount'] = folderInfo.albumsCounter
    output['tracksCount'] = folderInfo.tracksCounter
    output['coversCount'] = folderInfo.coversCounter
    output['errorsCount'] = errorCounter
    output['possibleErrors'] = (folderInfo.tracksCounter) * len(ErrorEnum)
    output['purity'] = purity
    return output


# Auxilliary, return an error about a given track
def _computeErrors(errorCode):
    output = {
        'errorCode': errorCode,
        'errorValue': ''
    }
    # ErrorCode 00 : Filename release artists doesn't match the artist foldername
    if errorCode == 0:
        output['errorValue'] = "Filename release artists doesn't match the artist foldername"
    # ErrorCode 01 : Filename year doesn't match the album foldername year
    if errorCode == 1:
        output['errorValue'] = "Filename year doesn't match the album foldername year"
    # ErrorCode 02 : Filename album doesn't match the album foldername
    if errorCode == 2:
        output['errorValue'] = "Filename album doesn't match the album foldername"
    # ErrorCode 03 : Filename year doesn't math the track year tag
    if errorCode == 3:
        output['errorValue'] = "Filename year doesn't math the track year tag"
    # ErrorCode 04 : Foldername year doesn't math the track year tag
    if errorCode == 4:
        output['errorValue'] = "Foldername year doesn't math the track year tag"
    # ErrorCode 05 : Filename album doesn't match the track album
    if errorCode == 5:
        output['errorValue'] = "Filename album doesn't match the track album"
    # ErrorCode 06 : Foldername album doesn't match the track album
    if errorCode == 6:
        output['errorValue'] = "Foldername album doesn't match the track album"
    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    if errorCode == 7:
        output['errorValue'] = "Filename disc+track number doesn't match the track disc+track number"
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    if errorCode == 8:
        output['errorValue'] = "Filename artists doesn't match the track artist tag"
    # ErrorCode 09 : Title remix artist doesn't match the track artist
    if errorCode == 9:
        output['errorValue'] = "Title remix artist doesn't match the filename artist"
    # ErrorCode 10 : Filename title doesn't match the track title tag
    if errorCode == 10:
        output['errorValue'] = "Filename title doesn't match the track title tag"
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    if errorCode == 11:
        output['errorValue'] = "Some tag requested by the naming convention aren't filled in track"
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    if errorCode == 12:
        output['errorValue'] = "Performer does not contains both the artist and the featuring artist"
    # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
    if errorCode == 13:
        output['errorValue'] = "Performer does not contains both the artist and the featuring artist"
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    if errorCode == 14:
        output['errorValue'] = "Computed album total track is not equal to the track total track tag"
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    if errorCode == 15:
        output['errorValue'] = "Computed album disc track is not equal to the track disc track tag"
    # ErrorCode 16 : Computed album year is not equal to the track year tag
    if errorCode == 16:
        output['errorValue'] = "Computed album year is not equal to the track year tag"
    # ErrorCode 17 : Year is not the same on all physical files of the album
    if errorCode == 17:
        output['errorValue'] = "Year is not the same on all physical files of the album"
    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    if errorCode == 18:
        output['errorValue'] = "The Filename doesn't follow the naming pattern properly"
    # ErrorCode 19 : Cover is not a 1000x1000 jpg image
    if errorCode == 19:
        output['errorValue'] = "The cover dimensions are incorrect and should be 1000x1000"
    # ErrorCode 20 : Track has no cover
    if errorCode == 20:
        output['errorValue'] = "The cover is missing from the file"
    # ErrorCode 21 : Release artist folder name doesn't match the track album artist tag
    if errorCode == 21:
        output['errorValue'] = "Foldername release artist is not equal to the track album artist tag"
    # ErrorCode 22 : Cover format is not optimized (not jpg)
    if errorCode == 22:
        output['errorValue'] = "The cover should be a jpg file for file size matters"
    # ErrorCode 23 : BPM is not an integer
    if errorCode == 23:
        output['errorValue'] = "The BPM value is not an integer"
    # ErrorCode 24 : Release year is not realistic (< 1900 or > today)
    if errorCode == 24:
        output['errorValue'] = "Year tag can't preceed 1900 or succeed today's year"
    # ErrorCode 25 : Invalid country trigram. Use NATO country notation with 3 capital letters
    if errorCode == 25:
        output['errorValue'] = "Invalid country trigram. Use OTAN country notation with 3 capital letters"
    # ErrorCode 26 : Unexisting country trigram. Check existing NATO values
    if errorCode == 26:
        output['errorValue'] = "The lang tag value doesn't exist in the list given by NATO"
    return output


# Save the output fileYear tag can't preceed 1900 or succeed today's year
def saveReportFile(report):
    createDirectory('output')
    fileName = "MzkOstrichRemover-{}".format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    with open('output/{}.json'.format(fileName), 'w') as file:
        json.dump(report, file, indent=2)

    return output


# Save the output file
def saveReportFile(report):
    createDirectory('output')
    fileName = "MzkOstrichRemover-{}".format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    with open('output/{}.json'.format(fileName), 'w') as file:
        json.dump(report, file, indent=2)
