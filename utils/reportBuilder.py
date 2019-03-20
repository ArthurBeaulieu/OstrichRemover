# Python imports
import datetime
import json

# Project imports
from utils.errorEnum import ErrorEnum
from utils.tools import createDirectory


# Generate an JSON file from the albumTesters array
def computeReport(version, folderInfo, albumTesters, errorCounter, purity):
    # Creating output dict object
    output = {}
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
    if errorCode == 0:
        output['errorValue'] = "Filename release artists doesn't match the artist foldername"
    if errorCode == 1:
        output['errorValue'] = "Filename year doesn't match the album foldername year"
    if errorCode == 2:
        output['errorValue'] = "Filename album doesn't match the album foldername"
    if errorCode == 3:
        output['errorValue'] = "Filename year doesn't math the track year tag"
    if errorCode == 4:
        output['errorValue'] = "Foldername year doesn't math the track year tag"
    if errorCode == 5:
        output['errorValue'] = "Filename album doesn't match the track album"
    if errorCode == 6:
        output['errorValue'] = "Foldername album doesn't match the track album"
    if errorCode == 7:
        output['errorValue'] = "Filename disc+track number doesn't match the track disc+track number"
    if errorCode == 8:
        output['errorValue'] = "Filename artists doesn't match the track artist tag"
    if errorCode == 9:
        output['errorValue'] = "Title remix artist doesn't match the filename artist"
    if errorCode == 10:
        output['errorValue'] = "Filename title doesn't match the track title tag"
    if errorCode == 11:
        output['errorValue'] = "Some tag requested by the naming convention aren't filled in track"
    if errorCode == 12:
        output['errorValue'] = "Performer does not contains both the artist and the featuring artist"
    if errorCode == 13:
        output['errorValue'] = "Performer does not contains both the artist and the featuring artist"
    if errorCode == 14:
        output['errorValue'] = "Computed album total track is not equal to the track total track tag"
    if errorCode == 15:
        output['errorValue'] = "Computed album disc track is not equal to the track disc track tag"
    if errorCode == 16:
        output['errorValue'] = "Computed album yeas is not equal to the track year tag"
    if errorCode == 17:
        output['errorValue'] = "Year is not the same on all physical files of the album"
    if errorCode == 18:
        output['errorValue'] = "The Filename doesn't follow the naming pattern properly"
    if errorCode == 19:
        output['errorValue'] = "The cover dimensions are incorrect and should be 1000x1000"
    if errorCode == 20:
        output['errorValue'] = "The cover is missing from the file"
    return output


# Save the output file
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
